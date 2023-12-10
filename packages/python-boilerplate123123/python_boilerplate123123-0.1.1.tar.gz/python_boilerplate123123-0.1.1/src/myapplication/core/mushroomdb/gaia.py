from abc import abstractmethod
from myapplication.core.mushroomdb import mycelium

class Gaia:

    def __init__(self):
        # Initialize database connection
        pass

    @abstractmethod
    def create_mycelium(self, table_name, schema) -> mycelium.Mycelium:
        pass
    @abstractmethod
    def get_mycelium(self, table_name) -> mycelium.Mycelium:
        pass

        