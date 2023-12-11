from abc import ABC, abstractmethod
from typing import Any

# Classes to be implemented by users for integrating with workload generator


class TaskGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_task(self):
        raise NotImplementedError()


class DataPartitionGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_data_partition(self):
        raise NotImplementedError()


class EngineHook(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, query: Any):
        raise NotImplementedError()

    @abstractmethod
    def add_data_partition(self, partition_id, partition: Any):
        raise NotImplementedError()
