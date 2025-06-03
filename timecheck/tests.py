import datetime as dt
from rest_framework.test import APIClient
from django.test import TestCase
from example_app.models import Post
from timecheck.settings import conf


def fmt_dt(t: dt.datetime):
    return dt.datetime.strftime(t, conf["dt_fmt"])


class TimeCheckTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.now = dt.datetime.now(dt.UTC)
        self.earlier = self.now - dt.timedelta(seconds=4)
        self.later = self.now + dt.timedelta(seconds=4)
        Post.objects.create(lastUpdated=self.now, text="Test")

    def test_get_client_is_newer(self):
        client_time = fmt_dt(self.later)
        conf["raise_exception"] = True
        response = self.client.get("/", HTTP_LASTUPDATED=client_time)
        self.assertEqual(response.status_code, conf["noupdate_code"])
        conf["raise_exception"] = False
        response = self.client.get("/", HTTP_LASTUPDATED=client_time)
        self.assertEqual(response.status_code, 200)

    def test_get_client_is_older(self):
        client_time = fmt_dt(self.earlier)
        response = self.client.get("/", HTTP_LASTUPDATED=client_time)
        conf["raise_exception"] = True
        self.assertEqual(response.status_code, 200)

    def test_get_client_is_equal(self):
        client_time = fmt_dt(self.now)
        response = self.client.get("/", HTTP_LASTUPDATED=client_time)
        conf["raise_exception"] = True
        self.assertEqual(response.status_code, conf["noupdate_code"])

    def test_put_client_is_newer(self):
        client_time = fmt_dt(self.later)
        conf["raise_exception"] = True
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
        conf["raise_exception"] = True
        response = self.client.put(
            "/",
            {"lastUpdated": client_time},
            format="json",
        )
        self.assertEqual(response.status_code, conf["noupdate_code"])
        conf["raise_exception"] = False
        response = self.client.put(
            "/",
            {"lastUpdated": client_time},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_put_client_is_equal(self):
        client_time = fmt_dt(self.now)
        conf["raise_exception"] = True
        response = self.client.put(
            "/",
            {"lastUpdated": client_time},
            format="json",
        )
        self.assertEqual(response.status_code, conf["noupdate_code"])
