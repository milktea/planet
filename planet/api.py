from flask import jsonify, make_response, request
from collections import defaultdict

from planet import app, db
from planet.models import Person
from .decorators import validateCompany
from .decorators import validatePerson


@app.route("/companies/<int:company_id>/employees", methods=["GET"])
@validateCompany
def get_company_employees(company_id, obj):
    """ 
        Given a company, the API needs to return all their employees.
        Provide the appropriate solution if the company does not have any employees.

        Return employees based on company id
    """

    return jsonify({"result": [x.serialise for x in obj.employees]})


@app.route("/persons/<int:person_id>", methods=["GET"])
@validatePerson
def get_person(person_id, obj):
    """
        Given 1 people, provide a list of fruits and vegetables they like. 
        This endpoint must respect this interface for the output: 
        `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

        Return person info (username, age, fave fruits and vegetables) based on id
    """

    return jsonify(
        {
            "username": obj.email.split("@")[0] if obj.email and "@" in obj.email else obj.name,
            "age": str(obj.age),
            "fruits": obj.favourite_fruits,
            "vegetables": obj.favourite_vegetables,
        }
    )


@app.route("/persons/<int:person_id>/mutual_friends/<int:friend_id>", methods=["GET"])
@validatePerson
def get_person_friends(person_id, friend_id, obj):
    """
        Given 2 people, provide their information (Name, Age, Address, phone) 
        and the list of their friends in common which have brown eyes and are still alive.

        ex:
        /persons/1/mutual_friends/2
        where 1 is the id of the first person
        and 2 is the id of the second person
    """

    friend_obj = Person.query.get(friend_id)
    if friend_obj is None:
        return make_response("Friend doesn't exist", 400)

    mutual_friends = obj.get_mutual_friends(friend_obj)

    return jsonify(
        {
            "result": {
                "person": obj.serialise,
                "friend": friend_obj.serialise,
                "mutual_friends": [x.serialise for x in mutual_friends],
            }
        }
    )
