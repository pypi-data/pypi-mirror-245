
from typing import List
from myapplication.core.mushroomdb import body

class Mycelium:

    __body_list = []

    def __init__(self, name, schema):
        self.name = name
        self.schema = schema

    def insert(self, body: body.Body):
       self.__body_list.append(body)

    def drop(self):
        self.__body_list = []

    def search(self, search_term) -> List[body.Body]:
        # Return a list of bodies that match the search term
        filtered = [body1 for body1 in self.__body_list if search_term in body1.get_data().values()]
        return filtered

    