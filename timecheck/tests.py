import datetime as dt
from django.utils.timezone import make_aware
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from example_app.models import Post
from timecheck.settings import conf
from timecheck.utils import fmt_dt, parse_dt


class TimeCheckTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.now = parse_dt("2024-01-01T12:00:00Z")
        self.later = parse_dt("2024-01-02T12:00:00Z")
        self.earlier = parse_dt("2024-01-01T11:00:00Z")

    def test_get_client_is_newer(self):
        client_time = fmt_dt(self.later)
        response = self.client.get("/", HTTP_LASTUPDATED=client_time)
        self.assertEqual(response.status_code, conf["noupdate_code"])

    def test_get_client_is_older(self):
        client_time = fmt_dt(self.earlier)
        response = self.client.get("/", HTTP_LASTUPDATED=client_time)
        self.assertEqual(response.status_code, 200)

    def test_get_client_is_equal(self):
        client_time = fmt_dt(self.now)
        response = self.client.get("/", HTTP_LASTUPDATED=client_time)
        self.assertEqual(response.status_code, conf["noupdate_code"])

    def test_put_client_is_newer(self):
        client_time = fmt_dt(self.later)
        response = self.client.put(
            "/",
            {
                "id": 1,
                "lastUpdated": client_time,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_put_client_is_older(self):
        client_time = fmt_dt(self.earlier)
        response = self.client.put(
            "/",
            {"lastUpdated": client_time},
            format="json",
        )
        self.assertEqual(response.status_code, conf["noupdate_code"])

    def test_put_client_is_equal(self):
        client_time = fmt_dt(self.now)
        response = self.client.put(
            "/",
            {"lastUpdated": client_time},
            format="json",
        )
        self.assertEqual(response.status_code, conf["noupdate_code"])
