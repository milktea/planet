#!flask/bin/python
from unittest import TestCase

from planet import app, db
from planet.models import Company
from planet.models import Person

TEST_DATABASE_URI = "postgresql://localhost:5432/planet_test"

class TestBase(TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = TEST_DATABASE_URI

        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def add_company_data(self):
        company = Company(name="Acme")
        db.session.add(company)
        db.session.flush()

        return company

    def add_person_data(self, has_died=False, eye_color="brown", name="One"):
        data = {
            "guid": name,
            "name": name,
            "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
            "gender": "female",
            "age": 61,
            "email": "carmellalambert@earthmark.com",
            "phone": "+1 (910) 567-3630",
            "company_id": 1,
            "attributes": {
                "_id": "595eeb9b96d80a5bc7afb106",
                "index": 0,
                "has_died": has_died,
                "balance": "$2,418.59",
                "picture": "http://placehold.it/32x32",
                "age": 61,
                "eyeColor": eye_color,
                "company_id": 1,
                "email": "carmellalambert@earthmark.com",
                "phone": "+1 (910) 567-3630",
                "about": "Non duis dolore ad enim. Est id reprehenderit cupidatat tempor excepteur. Cupidatat labore incididunt nostrud exercitation ullamco reprehenderit dolor eiusmod sit exercitation est. Voluptate consectetur est fugiat magna do laborum sit officia aliqua magna sunt. Culpa labore dolore reprehenderit sunt qui tempor minim sint tempor in ex. Ipsum aliquip ex cillum voluptate culpa qui ullamco exercitation tempor do do non ea sit. Occaecat laboris id occaecat incididunt non cupidatat sit et aliquip.\r\n",
                "registered": "2016-07-13T12:29:07 -10:00",
                "tags": [
                    "id",
                    "quis",
                    "ullamco",
                    "consequat",
                    "laborum",
                    "sint",
                    "velit",
                ],
                "greeting": "Hello, Carmella Lambert! You have 6 unread messages.",
                "favouriteFood": ["orange", "apple", "banana", "strawberry"],
            },
        }

        person = Person(**data)
        db.session.add(person)

        return person


if __name__ == "__main__":
    unittest.main()
