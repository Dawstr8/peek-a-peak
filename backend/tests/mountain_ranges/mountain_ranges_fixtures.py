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

    for i, range in enumerate(mountain_ranges, start=1):
        range.id = i

    return {
        "tatry": mountain_ranges[0],
        "karkonosze": mountain_ranges[1],
        "beskidy": mountain_ranges[2],
    }
