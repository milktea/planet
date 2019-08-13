from planet.tests import TestBase
from planet.models import Company
from planet.models import Person
from planet import db

import json


class PersonTest(TestBase):
    def test_add_person(self):
        self.add_company_data()

        self.add_person_data()
        db.session.commit()

        person = Person.query.first()
        assert person.name == "One"

    def test_get_person(self):
        self.add_company_data()

        self.add_person_data()
        db.session.commit()

        resp = self.app.get("/persons/1")
        assert resp.status_code == 200

        resp_data = json.loads(resp.data)
        assert resp_data["username"] == "carmellalambert"

        # expected result: age is a string
        assert resp_data["age"] == "61"

        assert resp_data["vegetables"] == []
        assert resp_data["fruits"] == ["orange", "apple", "banana", "strawberry"]

    def test_get_person_no_attributes(self):
        self.add_company_data()

        data = {
            "guid": "One",
            "name": "One",
            "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
            "gender": "female",
            "age": 61,
            "email": "carmellalambert@earthmark.com",
            "phone": "+1 (910) 567-3630",
            "company_id": 1,
        }

        person = Person(**data)
        db.session.add(person)

        db.session.commit()

        resp = self.app.get("/persons/1")
        assert resp.status_code == 200

        resp_data = json.loads(resp.data)
        assert resp_data["username"] == "carmellalambert"

        # expected result: age is a string
        assert resp_data["age"] == "61"

        assert resp_data["vegetables"] == []
        assert resp_data["fruits"] == []

    def test_get_person_email_is_none(self):
        self.add_company_data()

        data = {
            "guid": "One",
            "name": "One",
            "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
            "gender": "female",
            "age": 61,
            "phone": "+1 (910) 567-3630",
            "company_id": 1,
        }

        person = Person(**data)
        db.session.add(person)

        db.session.commit()

        resp = self.app.get("/persons/1")
        assert resp.status_code == 200

        resp_data = json.loads(resp.data)
        # set person name as username if email is none
        assert resp_data["username"] == "One"

        # expected result: age is a string
        assert resp_data["age"] == "61"

        assert resp_data["vegetables"] == []
        assert resp_data["fruits"] == []

    def test_get_person_not_existing(self):
        resp = self.app.get("/persons/1")
        assert resp.status_code == 400
        assert resp.data == b"Person doesn't exist"

    def test_get_person_mutual_friends_person_not_existing(self):
        resp = self.app.get("/persons/1/mutual_friends/2")
        assert resp.status_code == 400
        assert resp.data == b"Person doesn't exist"

    def test_get_person_mutual_friends_friend_not_existing(self):
        self.add_company_data()

        self.add_person_data()
        db.session.commit()

        resp = self.app.get("/persons/1/mutual_friends/2")
        assert resp.status_code == 400
        assert resp.data == b"Friend doesn't exist"

    def test_get_person_mutual_friends(self):
        self.add_company_data()

        person1 = self.add_person_data()
        person2 = self.add_person_data(name="Two")
        person3 = self.add_person_data(name="Three")
        db.session.flush()

        person1.friends = [person3]
        person2.friends = [person3]
        db.session.commit()

        resp = self.app.get("/persons/1/mutual_friends/2")
        assert resp.status_code == 200

        result = json.loads(resp.data)["result"]
        assert result["friend"]["name"] == "Two"
        assert result["person"]["name"] == "One"
        assert len(result["mutual_friends"]) == 1
        assert result["mutual_friends"][0]["name"] == "Three"

    def test_get_person_mutual_friends_same_mutual_friends_id_but_is_dead(self):
        self.add_company_data()

        person1 = self.add_person_data()
        person2 = self.add_person_data(name="Two")
        person3 = self.add_person_data(has_died=True, name="Three")
        db.session.flush()

        person1.friends = [person3]
        person2.friends = [person3]
        db.session.commit()

        resp = self.app.get("/persons/1/mutual_friends/2")
        assert resp.status_code == 200

        result = json.loads(resp.data)["result"]
        assert result["friend"]["name"] == "Two"
        assert result["person"]["name"] == "One"
        assert result["mutual_friends"] == []

    def test_get_person_mutual_friends_same_mutual_friends_id_but_eyes_not_brown(self):
        self.add_company_data()

        person1 = self.add_person_data()
        person2 = self.add_person_data(name="Two")
        person3 = self.add_person_data(eye_color="blue", name="Three")
        db.session.flush()

        person1.friends = [person3]
        person2.friends = [person3]
        db.session.commit()

        resp = self.app.get("/persons/1/mutual_friends/2")
        assert resp.status_code == 200

        result = json.loads(resp.data)["result"]
        assert result["friend"]["name"] == "Two"
        assert result["person"]["name"] == "One"
        assert result["mutual_friends"] == []

    def test_get_person_mutual_friends_same_mutual_friends_id_eyes_color_all_capital(
        self
    ):
        self.add_company_data()

        person1 = self.add_person_data()
        person2 = self.add_person_data(name="Two")
        person3 = self.add_person_data(eye_color="BROWN", name="Three")
        db.session.flush()

        person1.friends = [person3]
        person2.friends = [person3]
        db.session.commit()

        resp = self.app.get("/persons/1/mutual_friends/2")
        assert resp.status_code == 200

        result = json.loads(resp.data)["result"]
        assert result["friend"]["name"] == "Two"
        assert result["person"]["name"] == "One"
        assert result["mutual_friends"][0]["name"] == "Three"
