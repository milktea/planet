from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
    Index,
    and_,
    Enum,
    Table,
    Boolean,
    func,
)
from sqlalchemy.sql import cast
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.dialects.postgresql.json import JSONB
import json

from planet import db

FRUITS = ["apple", "strawberry", "orange", "banana"]
VEGETABLES = ["beetroot", "celery", "carrot", "cucumber"]

__all__ = ["Company", "Person"]

db.create_all()

user_friend = Table(
    "user_friend",
    db.Model.metadata,
    Column("userid", Integer, ForeignKey("persons.id")),
    Column("friendid", Integer, ForeignKey("persons.id")),
    UniqueConstraint("userid", "friendid", name="user_friend_unique"),
)


class Company(db.Model):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    employees = relationship("Person", backref="companies")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Company {}>".format(self.name)


class Person(db.Model):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    guid = Column(Text, unique=True)
    name = Column(Text, nullable=False)
    address = Column(Text)
    age = Column(Integer)
    email = Column(Text)
    phone = Column(Text)
    gender = Column("gender", Enum("male", "female", name="genders"), nullable=False)

    attributes = Column(MutableDict.as_mutable(JSONB), default={}, nullable=False)

    company_id = Column(
        "companyid", Integer, ForeignKey(Company.id, name="persons_companyid_fkey")
    )

    friends = relationship(
        "Person",
        secondary=user_friend,
        primaryjoin=id == user_friend.c.userid,
        secondaryjoin=id == user_friend.c.friendid,
        lazy="dynamic",
    )

    @hybrid_property
    def eye_color(self):
        return self.attributes["eyeColor"]

    @eye_color.expression
    def eye_color(cls):
        return func.lower(cls.attributes["eyeColor"].astext)

    @hybrid_property
    def has_died(self):
        return self.attributes["has_died"]

    @has_died.expression
    def has_died(cls):
        return cls.attributes["has_died"].astext.cast(Boolean)

    @hybrid_property
    def favourite_fruits(self):
        favourite_fruits = []
        if self.attributes:
            for food in self.attributes["favouriteFood"]:
                if food in FRUITS:
                    favourite_fruits.append(food)

        return favourite_fruits

    @hybrid_property
    def favourite_vegetables(self):
        favourite_vegetables = []
        if self.attributes:
            for food in self.attributes["favouriteFood"]:
                if food in VEGETABLES:
                    favourite_vegetables.append(food)

        return favourite_vegetables

    @hybrid_method
    def get_mutual_friends(self, friend_obj):
        filters = dict(eye_color="brown", has_died=False)
        person1_friends = self.friends.filter_by(**filters)
        person2_friends = friend_obj.friends.filter_by(**filters)

        return person1_friends.intersect(person2_friends)

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Person {}>".format(self.id)

    @property
    def serialise(self):
        return {
            key: getattr(self, key) for key in ["name", "age", "address", "phone"]
        }
