import json
from planet import app, db

from planet.models import Company
from planet.models import Person


@app.cli.command("db_seed")
def db_seed():

    try:
        with open("./resources/companies.json") as json_file:
            companies = json.load(json_file)

            for company in companies:
                company = Company(name=company["company"])
                db.session.add(company)

        db.session.flush()

        with open("./resources/people.json") as json_file:
            persons = json.load(json_file)

            rows = [
                "guid",
                "age",
                "name",
                "gender",
                "company_id",
                "email",
                "phone",
                "address",
            ]

            for person in persons:
                kwargs = {}
                for row in rows:
                    kwargs[row] = person.get(row, None)

                attrs = set(person.keys()) - set(rows)
                attrs.remove("friends")
                attrs.remove("index")
                attributes = {}
                for attr in attrs:
                    attributes[attr] = person.get(attr)

                person = Person(id=person.get("index"), attributes=attributes, **kwargs)
                db.session.add(person)
                db.session.flush()

            # prefer to use db.execute instead of inserting a person
            # thru a friends per object since it's faster.
            for person in persons:
                for friend in person["friends"]:
                    if person["index"] != friend["index"]:
                        db.session.execute(
                            "INSERT INTO user_friend VALUES({}, {})".format(
                                person["index"], friend["index"]
                            )
                        )

            db.session.commit()

    except Exception as e:
        print(e)


@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
