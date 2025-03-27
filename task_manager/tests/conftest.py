import pytest

@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    from django.core.management import call_command
    with django_db_blocker.unblock():
        call_command('migrate')
