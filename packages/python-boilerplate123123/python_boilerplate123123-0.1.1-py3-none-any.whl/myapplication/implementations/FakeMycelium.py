from core.mushroomdb import  Body, Mycelium, Gaia
from core.mushroomdb import Body, Mycelium, Gaia
from typing import List

class FakeMycelium(Gaia):

    def __init__(self, name, schema):
        self.name = name
        self.schema = schema

    def insert(self, body: Body):
        pass

    def drop(self):
        pass

    def search(self, search_term) -> List[Body]:
        pass    