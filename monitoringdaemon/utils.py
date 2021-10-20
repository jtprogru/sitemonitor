"""Application utils module."""
from pprint import pprint
from dependency_injector.providers import Configuration


def monitors_discovery(cfg: Configuration) -> list:
    """Discovery all monitors."""
    dumped_obj = cfg.provides
    print("#" * 45)
    pprint(dumped_obj)
    print("#" * 45)
