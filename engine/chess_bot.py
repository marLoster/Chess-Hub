from abc import ABC, abstractmethod


class ChessBot(ABC):
    def __init__(self, model_location):
        self.model_location = model_location

    @abstractmethod
    def get_move(self, board, color):
        pass
