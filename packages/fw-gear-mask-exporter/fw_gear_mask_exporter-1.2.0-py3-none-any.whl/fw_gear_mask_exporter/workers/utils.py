import typing as t

from fw_file.dicom import DICOM
from pydicom.multival import MultiValue


def get_from_shared(dicom: DICOM, steps: t.Tuple[str, str]):
    """Get a value from the SharedFunctionalGroupsSequence by path

    Args:
        dicom (DICOM): Input dicom
        steps (tuple[str, str]): Path steps to a dicom value
            e.g. if you want to get the value of
            dicom.SharedFunctionalGroupsSequence[0].PixelMeasuresSequence[0].SliceThickness
            you would pass in `[PixelMeasuresSequence, SliceThickness]`

    Returns:
        Result
    """
    res = None
    shared = dicom.get("SharedFunctionalGroupsSequence")
    if shared:
        int_ = shared[0].get(steps[0])
        if int_:
            res = int_[0].get(steps[1])
    return res


def get_from_per_frame(dicom: DICOM, steps: t.Tuple[str, str], raising=True):
    """Get a value from the PerFrameFunctionalGroupsSequence by path

    Args:
        dicom (DICOM): Input dicom
        steps (tuple[str, str]): Path steps to a dicom value
            e.g. if you want to get the value of
            dicom.PerFrameFunctionalGroupsSequence[*].PixelMeasuresSequence[*].SliceThickness
            you would pass in `[PixelMeasuresSequence, SliceThickness]`
        raising (bool): Whether to raise an error if the value varies across
            frames. Defaults to True

    Note: This function only returns a value if it is the same across all the
        frames, it will either raise an error or return None based on the value
        of the `raising` kwarg

    Returns:
        Result
    """
    res = None
    per_frame = dicom.get("PerFrameFunctionalGroupsSequence")
    if per_frame:
        results = []
        for frame in per_frame:
            int_ = frame.get(steps[0])
            if int_:
                results.append(int_[0].get(steps[1]))
        # Keep unique values (Multivalues and Lists need to be casted as tuples to be
        # hashable)
        result_set = set(tuple(r) for r in results if isinstance(r, (MultiValue, list)))
        if not len(result_set):
            return res
        # If results are more than one, raise an error according to kwarg
        elif len(result_set) > 1:
            if raising:
                raise RuntimeError(
                    f"{steps[1]} varies across frames, found: {result_set}"
                )
            else:
                return None
        res = results[0]
    return res
