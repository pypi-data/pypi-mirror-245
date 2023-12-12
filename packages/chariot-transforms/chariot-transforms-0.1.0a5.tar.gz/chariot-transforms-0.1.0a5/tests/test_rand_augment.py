import random

import numpy as np
import pytest
import torch

from chariot_transforms.augmentations.transforms import RandAugment


@pytest.fixture
def img():
    return torch.rand(1, 3, 10, 10)


def test_augments(img):
    """Test that rand augment runs and changes an image and keeps its size"""
    rand_augment = RandAugment(10, 2)

    trans_img = rand_augment(img)
    assert (img != trans_img).all()
    assert img.shape == trans_img.shape


def test_augments_no_m(img):
    """Test that rand augment with random magnitude runs and changes an
    image and keeps its size
    """
    rand_augment = RandAugment(10)
    trans_img = rand_augment(img)
    assert not (img == trans_img).all()
    assert img.shape == trans_img.shape


def test_specified_augmentation_identity(img):
    """Test that augmentations can be specified"""
    rand_augment = RandAugment(10, augs_to_use=["Identity"])
    trans_img = rand_augment(img)
    assert (img == trans_img).all()
    assert img.shape == trans_img.shape


def test_specified_augmentations(img):
    """Test that augmentations can be specified"""
    random.seed(42)
    rand_augment = RandAugment(10, 3, augs_to_use=["Equalize", "Invert"])
    trans_img = rand_augment(img)
    for a in rand_augment.augmentations:
        assert a[0] in ["Equalize", "Invert"]

    assert not (img == trans_img).all()
    assert img.shape == trans_img.shape


def test_restricted_augmentations(img):
    """Test that augmentations can be removed"""
    rand_augment = RandAugment(10, 3, augs_to_remove=["Equalize", "Identity"])
    trans_img = rand_augment(img)
    for a in rand_augment.augmentations:
        assert a[0] not in ["Color", "Identity"]

    assert (
        len(RandAugment.augmentations) == len(rand_augment.augmentations) + 2
    )

    assert not (np.array(img) == np.array(trans_img)).all()
    assert img.shape == trans_img.shape


def test_mag_too_big():
    """Test that an error is raised if a magnitude larger than 11 is passed"""
    with pytest.raises(ValueError) as exc_info:
        RandAugment(10, 11)
    assert "m must be between 0 and 10" in str(exc_info.value)


def test_mag_too_small():
    """Test that an error is raised if a magnitude larger than 0 is passed"""
    with pytest.raises(ValueError) as exc_info:
        RandAugment(10, -1)
    assert "m must be between 0 and 10" in str(exc_info.value)
