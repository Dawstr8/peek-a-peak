from uuid import uuid4

import pytest

from src.mountain_ranges.models import MountainRange


@pytest.fixture
def mountain_ranges() -> list[MountainRange]:
    return [
        MountainRange(name="Tatry"),
        MountainRange(name="Karkonosze"),
        MountainRange(name="Beskidy"),
    ]


@pytest.fixture
def mock_mountain_ranges_map(mountain_ranges) -> dict[str, MountainRange]:
    """
    Returns a map of mock MountainRange objects for unit tests.
    """

    for range in mountain_ranges:
        range.id = uuid4()

    return {
        "tatry": mountain_ranges[0],
        "karkonosze": mountain_ranges[1],
        "beskidy": mountain_ranges[2],
    }
