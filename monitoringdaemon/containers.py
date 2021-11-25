"""Application containers module."""

import logging
import sys

from dependency_injector import containers, providers

from . import dispatcher, http, monitors


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration()

    configure_logging = providers.Callable(
        logging.basicConfig,
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.format,
    )

    http_client = providers.Factory(http.HttpClient)

    jtprogru_monitor = providers.Factory(
        monitors.HttpMonitor,
        http_client=http_client,
        options=config.monitors.jtprogru,
    )

    savinmiru_monitor = providers.Factory(
        monitors.HttpMonitor,
        http_client=http_client,
        options=config.monitors.savinmiru,
    )

    advru_monitor = providers.Factory(
        monitors.HttpMonitor,
        http_client=http_client,
        options=config.monitors.advru,
    )

    advwecom_monitor = providers.Factory(
        monitors.HttpMonitor,
        http_client=http_client,
        options=config.monitors.advwecom,
    )

    httpbin_monitor = providers.Factory(
        monitors.HttpMonitor,
        http_client=http_client,
        options=config.monitors.httpbin,
    )

    example_monitor = providers.Factory(
        monitors.HttpMonitor,
        http_client=http_client,
        options=config.monitors.example,
    )

    dispatcher = providers.Factory(
        dispatcher.Dispatcher,
        monitors=providers.List(
            jtprogru_monitor,
            savinmiru_monitor,
            advru_monitor,
            advwecom_monitor,
            httpbin_monitor,
        ),
    )
