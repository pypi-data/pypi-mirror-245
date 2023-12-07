from abc import ABC, abstractmethod


class CloudController(ABC):
    @abstractmethod
    def scale_default_ng(self, node_count: int):
        pass
