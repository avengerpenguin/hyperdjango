from django.conf import settings


def pytest_configure():
    settings.configure(
        ROOT_URLCONF="tests.app",
        MIDDLEWARE_CLASSES=(
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ),
        INSTALLED_APPS=[
            "hyperdjango",
            "tests",
        ],
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
    )
