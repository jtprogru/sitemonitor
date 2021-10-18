"""Tests module."""

import asyncio
import dataclasses
from unittest import mock

import pytest

from .containers import ApplicationContainer


@dataclasses.dataclass
class RequestStub:
    status: int
    content_length: int


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
                    "check_every": 1,
                },
                "httpbin": {
                    "method": "GET",
                    "url": "https://fake-httpbin.org/get",
                    "timeout": 1,
                    "check_every": 1,
                },
            },
        }
    )
    return container


@pytest.mark.asyncio
async def test_example_monitor(container, caplog):
    caplog.set_level("INFO")

    http_client_mock = mock.AsyncMock()
    http_client_mock.request.return_value = RequestStub(
        status=200,
        content_length=635,
    )

    with container.http_client.override(http_client_mock):
        example_monitor = container.example_monitor()
        await example_monitor.check()

    assert "http://fake-example.com" in caplog.text
    assert "response code: 200" in caplog.text
    assert "content length: 635" in caplog.text


@pytest.mark.asyncio
async def test_dispatcher(container, caplog, event_loop):
    caplog.set_level("INFO")

    example_monitor_mock = mock.AsyncMock()
    httpbin_monitor_mock = mock.AsyncMock()

    with container.example_monitor.override(
        example_monitor_mock
    ), container.httpbin_monitor.override(httpbin_monitor_mock):

        dispatcher = container.dispatcher()
        event_loop.create_task(dispatcher.start())
        await asyncio.sleep(0.1)
        dispatcher.stop()

    assert example_monitor_mock.check.called
    assert httpbin_monitor_mock.check.called
