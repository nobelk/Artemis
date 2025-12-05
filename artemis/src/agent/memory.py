from abc import ABC, abstractmethod

class Memory(ABC):
    @abstractmethod
    def recall(self):
        pass

    @abstractmethod
    def put(self):
        pass
