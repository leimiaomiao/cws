from mongoengine import *

connect("corpus")


class Candidate(Document):
    word = StringField()
    count = IntField()
    left_set = MapField(field=StringField())
    right_set = MapField(field=StringField())

    def rtrv_one(self, **kwargs):
        try:
            obj = self.__objects.get(**kwargs)
        except DoesNotExist:
            obj = None
        return obj

    def rtrv_all(self, **kwargs):
        return self.__objects(**kwargs)

    def inner_solid_degree(self):
        pass

    def outer_free_degree(self):
        pass
