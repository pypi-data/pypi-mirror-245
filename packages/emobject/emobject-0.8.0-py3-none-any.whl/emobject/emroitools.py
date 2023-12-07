import numpy as np
from skimage import draw


def convert_rect_to_poly(roi_coord):
    """
    Converts roi coordinates to polygon-style data structure if it is rectangle style.

    Args:
        roi_coord: 2xN numpy array of roi coordinates in either poly or rectangle format.

    Returns:
        A 2xN numpy array of roi coordinates with polygon data structure.
    """

    if len(roi_coord) == 2:  # rect data structure only has two points
        poly_array = []
        roi_coord = roi_coord.T  # transpose required here for rectangular coordinates
        poly_array.append((roi_coord[0][0], roi_coord[1][0]))
        poly_array.append((roi_coord[0][1], roi_coord[1][0]))
        poly_array.append((roi_coord[0][1], roi_coord[1][1]))
        poly_array.append((roi_coord[0][0], roi_coord[1][1]))

        roi_coord = np.array(poly_array)

    return roi_coord


def roi_to_mask(roi_coord, image_shape):
    """
    Converts roi coordinates to binary mask.
    From, https://gist.github.com/hadim/fa89b50bbd240c486c61787d205d28a6

    Args:
        roi_coord: 2xN numpy array of roi coordinates.
        image_shape: a tuple of image shape.

    Returns:
        A binary mask with area enclosed in roi set to True.
    """

    vertex_row_coords = roi_coord[:, 1]
    vertex_col_coords = roi_coord[:, 0]
    fill_row_coords, fill_col_coords = draw.polygon(
        vertex_row_coords, vertex_col_coords, image_shape
    )
    mask = np.zeros(image_shape, dtype=bool)
    mask[fill_row_coords, fill_col_coords] = True

    return mask


def combine_masks_dict(masks_dict):
    """
    Converts a dictionary of masks into one stacked mask.
    Warning, logic assumes ROIs are not overlapping

    Args:
        masks_dict: dictionary of roi_id, binary mask key-value pairs.

    Returns:
        A binary mask of all masks in dictionary combined.
    """

    # initialize a mask
    mask_keys = list(masks_dict.keys())
    combined_mask = np.zeros_like(masks_dict[mask_keys[0]], dtype="uint16")

    # stack image - each subroi is assigned a value equal to roi_id
    for roi_id, mask in masks_dict.items():
        combined_mask = combined_mask + roi_id * mask

    return combined_mask
