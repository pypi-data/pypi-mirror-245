from loguru import logger
from itertools import count
from wlgen.core.resourcemanager import LastItem


class Tasks:
    """Model task arrival rate and privacy demands."""

    def __init__(self, environment, resource_manager, rng):
        self.rng = rng
        self.env = environment
        self.config = resource_manager.config
        self.resource_manager = resource_manager
        self.task_generator = self.resource_manager.task_generator
        self.task_count = count()

        logger.info("Poisson sampling.")
        assert self.config.tasks.max_num is not None

        self.env.process(self.task_producer())

    def task_producer(self) -> None:
        """Generate tasks."""

        # Wait till blocks initialization is completed
        yield self.resource_manager.blocks_initialized

        task_id = next(self.task_count)

        # Produce initial tasks
        for _ in range(self.config.tasks.initial_num):
            self.task(task_id)
            task_id = next(self.task_count)
        logger.debug("Done producing all the initial tasks.")

        while self.config.tasks.max_num > task_id:
            # No task can arrive after the end of the simulation
            # so we force them to appear right before the end of the last block
            task_arrival_interval = (
                0
                if self.resource_manager.block_production_terminated.triggered
                else self.rng.exponential(1 / self.config.tasks.avg_num_tasks_per_block)
            )

            self.task(task_id)
            yield self.env.timeout(task_arrival_interval)
            task_id = next(self.task_count)

        self.resource_manager.task_production_terminated.succeed()
        self.resource_manager.new_tasks_queue.put(LastItem())

        logger.info(
            f"Done generating tasks at time {self.env.now}. Current count is: {task_id}"
        )

    def task(self, task_id: int) -> None:
        """Task behavior. Sets its own demand, notifies resource manager of its existence"""
        task = self.task_generator.create_task()

        logger.debug(f"Task: {task_id} generated at {self.env.now}. Name: {task}")
        self.resource_manager.new_tasks_queue.put(task)
