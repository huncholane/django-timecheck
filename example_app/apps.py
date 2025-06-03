from django.apps import AppConfig
from django.core.management import call_command
from django.db.models.signals import post_migrate


class ExampleAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "example_app"

    def ready(self):
        print("HELLO")
        post_migrate.connect(load_fixtures, sender=self)


def load_fixtures(**_):
    print("Making init data")
    call_command("loaddata", "initial_data", app_label="example_app", verbosity=0)
