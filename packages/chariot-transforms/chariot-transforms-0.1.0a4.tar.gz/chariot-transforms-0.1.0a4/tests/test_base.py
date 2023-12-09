import pytest

from chariot_transforms.augmentations import Pad
from chariot_transforms.base import Compose
from chariot_transforms.preprocessing import (
    IdentityPreprocessingTransform,
    Resize,
)


def test_compose_equality():
    t1 = IdentityPreprocessingTransform()
    t2 = Resize(224)
    t3 = Pad(10)

    assert Compose([t1, t2, t3]) == Compose([t2, t3])
    assert Compose([t2]) == t2
    assert Compose([t2, Compose([t1, t3])]) == Compose([t2, t3])

    assert Compose([t1, t3]) != Compose([t1])
    assert Compose([t1]) != t2


def test_compose_validation():
    with pytest.raises(ValueError) as exc_info:
        Compose([])
    assert "transforms list should not be empty" in str(exc_info.value)
