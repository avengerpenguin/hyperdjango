import os
from django.conf import settings
import django
from django.conf.urls import url, re_path
import hyperdjango


def pytest_configure():
    settings.configure(
        ROOT_URLCONF='tests.app',
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
        INSTALLED_APPS=[
            'hyperdjango',
            'tests',
        ],
        DEBUG=True,
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
    )
    django.setup()
