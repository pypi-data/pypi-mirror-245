import simpy
from loguru import logger


class LastItem:
    def __init__(self):
        return


class ResourceManager:
    """
    Manages blocks and tasks arrival
    """

    def __init__(
        self, environment, engine_hook, task_generator, block_generator, config
    ):
        self.env = environment
        self.config = config

        self.engine_hook = engine_hook
        self.task_generator = task_generator
        self.block_generator = block_generator

        # # To store the incoming tasks and blocks
        self.new_tasks_queue = simpy.Store(self.env)
        self.new_blocks_queue = simpy.Store(self.env)

        self.blocks_initialized = self.env.event()

        # Stopping conditions
        self.block_production_terminated = self.env.event()
        self.task_production_terminated = self.env.event()
        self.block_consumption_terminated = self.env.event()
        self.task_consumption_terminated = self.env.event()

    def start(self):
        self.daemon_clock = self.env.process(self.daemon_clock())

        self.env.process(self.block_consumer())
        self.env.process(self.task_consumer())

        # Termination conditions
        yield self.block_production_terminated
        yield self.task_production_terminated
        yield self.block_consumption_terminated
        yield self.task_consumption_terminated
        self.daemon_clock.interrupt()
        logger.info(f"Terminating the simulation at {self.env.now}. Closing...")

    def daemon_clock(self):
        while True:
            try:
                yield self.env.timeout(1)
                logger.info(f"Simulation Time is: {self.env.now}")
            except simpy.Interrupt as i:
                return

    def block_consumer(self):
        while True:
            block_message = yield self.new_blocks_queue.get()

            if isinstance(block_message, LastItem):
                logger.info("Done consuming blocks.")
                self.block_consumption_terminated.succeed()
                return

            block_id, block = block_message
            self.engine_hook.add_data_partition(block_id, block)

            if self.config.blocks.initial_num == block_id + 1:
                self.blocks_initialized.succeed()

    def task_consumer(self):
        while True:
            task_message = yield self.new_tasks_queue.get()

            if isinstance(task_message, LastItem):
                logger.info("Done consuming tasks")
                self.task_consumption_terminated.succeed()
                return

            batch = task_message
            self.engine_hook.evaluate(batch)
