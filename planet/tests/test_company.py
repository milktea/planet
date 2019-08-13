from planet.tests import TestBase
from planet.models import Company
from planet.models import Person
from planet import db

import json


class CompanyTest(TestBase):
    def test_add_company(self):
        self.add_company_data()
        db.session.commit()

        company = Company.query.first()
        assert company.name == "Acme"

    def test_get_company_employees_company_not_existing(self):
        resp = self.app.get("/companies/1/employees")
        assert resp.status_code == 400
        assert resp.data == b"Company doesn't exist"

    def test_get_company_employees_no_employees(self):
        self.add_company_data()
        db.session.commit()

        resp = self.app.get("/companies/1/employees")
        assert resp.status_code == 200
        assert json.loads(resp.data)["result"] == []

    def test_get_company_employees_with_employee(self):
        self.add_company_data()

        self.add_person_data()
        db.session.commit()

        resp = self.app.get("/companies/1/employees")
        assert resp.status_code == 200

        result = json.loads(resp.data)["result"]
        assert len(result) == 1

        person1 = result[0]
        assert person1["name"] == "One"
