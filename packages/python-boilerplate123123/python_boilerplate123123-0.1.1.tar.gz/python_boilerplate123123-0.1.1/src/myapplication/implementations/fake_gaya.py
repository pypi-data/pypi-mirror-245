
from myapplication.core.mushroomdb import gaia, mycelium

class FakeGaia(gaia.Gaia):

    def __init__(self):
        # Initialize mock data structures or database connection
        self.mycelia = {}

    def create_mycelium(self, table_name, schema) -> mycelium.Mycelium:
        # Create mock mycelium data structure or simulate database creation
        self.mycelia[table_name] = mycelium.Mycelium(table_name,schema)

        return self.mycelia[table_name]

    def get_mycelium(self, table_name) -> mycelium.Mycelium:
        # Retrieve mock mycelium data structure or simulate database retrieval
        if table_name in self.mycelia:
            return self.mycelia[table_name]
        else:
            raise KeyError(f"Mycelium table '{table_name}' not found")
