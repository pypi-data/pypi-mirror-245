from typing import List
from loguru import logger
from itertools import count
from wlgenlib.core.resourcemanager import LastItem


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
        initial_task_ids = []
        for _ in range(int(self.config.tasks.initial_num)):
            initial_task_ids.append(task_id)
            task_id = next(self.task_count)
        # Feed all initial tasks at once as a batch
        self.task(initial_task_ids)
        logger.debug("Done producing all the initial tasks.")

        while self.config.tasks.max_num > task_id:
            # No task can arrive after the end of the simulation
            # so we force them to appear right before the end of the last block
            task_arrival_interval = (
                0
                if self.resource_manager.block_production_terminated.triggered
                else self.rng.exponential(1 / self.config.tasks.avg_num_tasks_per_block)
            )
            # Feed all online tasks one by one
            self.task([task_id])
            yield self.env.timeout(task_arrival_interval)
            task_id = next(self.task_count)

        self.resource_manager.task_production_terminated.succeed()
        self.resource_manager.new_tasks_queue.put(LastItem())

        logger.info(
            f"Done generating tasks at time {self.env.now}. Current count is: {task_id}"
        )

    def task(self, task_ids: List[int]) -> None:
        """Task behavior. Sets its own demand, notifies resource manager of its existence"""
        
        batch = [self.task_generator.create_task() for _ in task_ids]
        logger.debug(f"Batch: {task_ids} generated at {self.env.now}. Name: {batch}")
        self.resource_manager.new_tasks_queue.put(batch)
