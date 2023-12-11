import pytest
from pydantic import RootModel
from pykit import validation
from pykit.map import MapUtils

from orwynn.app import AppMode
from orwynn.apprc.apprc import AppRc
from orwynn.boot import Boot
from orwynn.config import Config
from orwynn.di.di import Di
from orwynn.module.module import Module


class Menu(RootModel):
    root: dict[str, float]


class BurgerShotConfig(Config):
    location: str
    employees: int
    menu: Menu


@pytest.fixture
def raw_apprc() -> AppRc:
    return {
        "prod": {
            "BurgerShot": {
                "location": "Vinewood",
                "employees": 15,
                "menu": {
                    "standard_burger": 1.25,
                    "cola": 1.5
                }
            }
        },
        "dev": {
            "BurgerShot": {
                "employees": 25,
                "menu": {
                    "cola": 1.8,
                    "pizza": 4.1,
                    "fried_chicken": 3.5
                }
            }
        },
        "test": {
            "BurgerShot": {
                "location": "Jefferson",
                "menu": {
                    "standard_burger": 1.1,
                    "fried_chicken": 5.0
                }
            }
        }
    }


@pytest.mark.asyncio
async def test_prod(raw_apprc: AppRc):
    await Boot.create(
        root_module=Module("/", Providers=[BurgerShotConfig]),
        apprc=raw_apprc,
        mode=AppMode.PROD
    )

    assert validation.apply(
        Di.ie().find("BurgerShotConfig"),
        BurgerShotConfig
    ).model_dump() == MapUtils.find("prod.BurgerShot", raw_apprc)


@pytest.mark.asyncio
async def test_dev(raw_apprc: AppRc):
    await Boot.create(
        root_module=Module("/", Providers=[BurgerShotConfig]),
        apprc=raw_apprc,
        mode=AppMode.DEV
    )

    assert validation.apply(
        Di.ie().find("BurgerShotConfig"),
        BurgerShotConfig
    ).model_dump() == {
        "location": "Vinewood",
        "employees": 25,
        "menu": {
            "standard_burger": 1.25,
            "cola": 1.8,
            "pizza": 4.1,
            "fried_chicken": 3.5
        }
    }


@pytest.mark.asyncio
async def test_test(raw_apprc: AppRc):
    await Boot.create(
        root_module=Module("/", Providers=[BurgerShotConfig]),
        apprc=raw_apprc,
        mode=AppMode.TEST
    )

    assert validation.apply(
        Di.ie().find("BurgerShotConfig"),
        BurgerShotConfig
    ).dict() == {
        "location": "Jefferson",
        "employees": 25,
        "menu": {
            "standard_burger": 1.1,
            "cola": 1.8,
            "pizza": 4.1,
            "fried_chicken": 5.0
        }
    }
