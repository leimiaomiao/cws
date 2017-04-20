from mongoengine import *

connect("corpus")


class Candidate(Document):
    word = StringField()
    count = IntField()
    left_set = MapField(field=StringField())
    right_set = MapField(field=StringField())

    @classmethod
    def rtrv_one(cls, **kwargs):
        try:
            obj = cls.objects.get(**kwargs)
        except DoesNotExist:
            obj = None
        return obj

    @classmethod
    def rtrv_all(cls, **kwargs):
        return cls.objects(**kwargs)

    def inner_solid_degree(self):
        pass

    def outer_free_degree(self):
        pass
