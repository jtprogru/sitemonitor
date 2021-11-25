import pytest

from monitoringdaemon.containers import ApplicationContainer


@pytest.fixture
def container():
    container = ApplicationContainer()
    container.config.from_dict(
        {
            "log": {
                "level": "INFO",
                "formant": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            },
            "monitors": {
                "example": {
                    "method": "GET",
                    "url": "http://fake-example.com",
                    "timeout": 1,
                    "check_every": 5,
                },
                "httpbin": {
                    "method": "GET",
                    "url": "https://fake-httpbin.org/get",
                    "timeout": 1,
                    "check_every": 5,
                },
            },
        }
    )
    return container
