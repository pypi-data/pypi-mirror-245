from zaapy.api.analysis import GasField
import numpy as np


def compute(
    field: str,
    data: np.ndarray,
    ref: GasField,
):
    ret_data = data
    ret_coords = ref.coords
    geometry = ret_coords.geometry
    return GasField(
        field,
        ret_data,
        geometry,
        ref.it,
        ref.mfl,
        operation=ref.operation,
        directory=ref.directory,
    )
