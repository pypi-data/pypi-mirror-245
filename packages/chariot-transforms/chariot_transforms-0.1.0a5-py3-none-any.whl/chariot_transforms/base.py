from abc import abstractmethod
from typing import List

import torch
import torchvision.transforms.functional as F
from PIL import Image


def validate_rank_4(img):
    if isinstance(img, torch.Tensor) and len(img.shape) != 4:
        raise ValueError("img must be a rank 4 tensor")


class TransformBase:
    """Base class for both pre-processing and augmentation transforms"""

    @staticmethod
    def _validate_input(img):
        validate_rank_4(img)
        if img.shape[0] != 1:
            raise ValueError(
                "Transforms currently only support batches of size 1."
            )

    def __call__(
        self,
        img: torch.Tensor,
        mask: Image.Image = None,
        bbox_dict: dict = None,
    ):
        """
        Parameters
        ----------
        img
            should be a rank 4 image tensor. Currently we only support batches of size 1
            (i.e. img.shape[0] should be 1)
        mask : Image.Image
            segmentation mask
        bbox_dict : dict
            dict with keys "bboxes" and "classes"

        Returns
        -------
        torch.Tensor or tuple
            If only img is passed then the return is the transformed image. Otherwise it is
            a tuple with the first item the transformed image and the other items
            the transformed annotations.
        """
        self._validate_input(img)
        ret = [self._convert_img_tensor(img)]
        if mask is not None:
            ret.append(self._convert_mask(mask))
        if bbox_dict is not None:
            new_bbox_dict = {"bboxes": [], "classes": []}
            for bbox, label in zip(bbox_dict["bboxes"], bbox_dict["classes"]):
                new_bbox = self._convert_bbox(bbox)
                if new_bbox is not None:
                    new_bbox_dict["bboxes"].append(new_bbox)
                    new_bbox_dict["classes"].append(label)

            ret.append(new_bbox_dict)

        return tuple(ret) if len(ret) > 1 else ret[0]

    @abstractmethod
    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        """This method applies the transfomration to an image tensor

        Parameters
        ----------
        img
            input image tensor. this must be of rank 4: [N, C, H, W]

        Returns
        -------
        torch.Tensor
            the transformed image tensor. this will be of rank 4 and have the
            same N, C values
        """
        raise NotImplementedError

    @abstractmethod
    def _convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        raise NotImplementedError

    @abstractmethod
    def _convert_coords(self, coords, img_h, img_w, invert=False):
        raise NotImplementedError

    def _convert_mask(self, mask: Image.Image) -> Image.Image:
        """
        Parameters
        ----------
        mask
            mask should be an 8-bit, single channel PIL image
        """
        return F.to_pil_image(
            self._convert_img_tensor(F.to_tensor(mask).unsqueeze(0))[0]
        )


class ImageOnlyTransform(TransformBase):
    """Base class for transforms that do not change bounding boxes or masks, such as
    color jitters, histogram transforms, etc.
    """

    def _convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        return bbox

    def _convert_coords(self, coords, img_h, img_w, invert=False):
        return coords

    def _convert_mask(self, mask):
        return mask


class IdentityTransform(ImageOnlyTransform):
    def __init__(self):
        pass

    def _convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        return bbox

    def _convert_coords(self, coords, img_h, img_w, invert=False):
        return coords

    def set_magnitude(self, magnitude: float) -> None:
        return

    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        return img

    def __eq__(self, other):
        return isinstance(other, IdentityTransform)


class Compose(TransformBase):
    """Composes several transforms together."""

    __serialization_attributes__ = ["transforms"]

    def __init__(self, transforms: List[TransformBase]):
        """
        Parameters
        ----------
        transforms : list
            list of transforms to compose
        """
        if len(transforms) == 0:
            raise ValueError("transforms list should not be empty")

        self.transforms = []
        for t in transforms:
            if isinstance(t, Compose):
                self.transforms.extend(t.transforms)
            else:
                self.transforms.append(t)

    def _convert_img_tensor(self, img):
        for t in self.transforms:
            img = t._convert_img_tensor(img)
        return img

    def _convert_mask(self, mask, *args, **kwargs):
        for t in self.transforms:
            mask = t._convert_mask(mask, *args, **kwargs)
        return mask

    def _convert_bbox(self, bbox, *args, **kwargs):
        for t in self.transforms:
            bbox = t._convert_bbox(bbox, *args, **kwargs)
            if bbox is None:
                return None
        return bbox

    def __repr__(self):
        format_string = self.__class__.__name__ + "("
        for t in self.transforms:
            format_string += "\n"
            format_string += "    {0}".format(t)
        format_string += "\n)"
        return format_string

    def __eq__(self, other: object) -> bool:
        # ignore identity transforms when comparing
        self_transforms = [
            t for t in self.transforms if not isinstance(t, IdentityTransform)
        ]

        if not isinstance(other, Compose):
            # consider a Compose with a single element to be the same
            if isinstance(other, TransformBase) and len(self_transforms) == 1:
                return self_transforms[0] == other
            if (
                isinstance(other, TransformBase)
                and isinstance(other, IdentityTransform)
                and len(self_transforms) == 0
            ):
                return True
            return False

        other_transforms = [
            t for t in other.transforms if not isinstance(t, IdentityTransform)
        ]
        if len(self_transforms) != len(other_transforms):
            return False
        for t1, t2 in zip(self_transforms, other_transforms):
            if t1 != t2:
                return False
        return True
