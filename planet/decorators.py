from functools import wraps
from flask import request, make_response

from planet.models import Company
from planet.models import Person


def validateCompany(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        company_id = kwargs.get("company_id", None)
        obj = Company.query.get(company_id)

        if obj is None:
            return make_response("Company doesn't exist", 400)

        kwargs["obj"] = obj
        return f(*args, **kwargs)

    return decorated


def validatePerson(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        person_id = kwargs.get("person_id", None)
        obj = Person.query.get(person_id)

        if obj is None:
            return make_response("Person doesn't exist", 400)

        kwargs["obj"] = obj
        return f(*args, **kwargs)

    return decorated
