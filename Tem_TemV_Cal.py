import numpy as np
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning, NumbaWarning
import warnings

#忽略警告
# warnings.simplefilter('ignore', category = NumbaDeprecationWarning)
# warnings.simplefilter('ignore', category = NumbaWarning)
# warnings.filterwarnings("ignore")


from numba import int32, float32, boolean    # import the types
from numba.experimental import jitclass
import numba as nb


# spec = \
# [('nTime_Window', int32), ('fSlab_Width', float32[:]), ('fSlab_Thick', float32[:]), ('fCasting_Speed', float32[:]),
# ('fMold_Level', float32[:]), ('fTundishTem', float32[:]), ('fMoldFrequency', float32[:]), ('fMoldStroke', float32[:]),
# ('fMoldNonSinuFac', float32[:]), ('Tc_Num_Broad', int32), ('Tc_Num_Narrow', int32), ('fMoldBroadOuterTem', float32[:,:]),
# ('fMoldBroadInnerTem', float32[:,:]), ('fMoldNarrowLeftTem', float32[:,:]), ('fMoldNarrowRightTem', float32[:,:]),
# ('fErrorThermoLimitMin', float32), ('fErrorThermoLimitMax', float32), ('bMoldBroadInnerTem', boolean[:]),
# ('bMoldBroadOuterTem', boolean[:]), ('bMoldNarrowLeftTem', boolean[:]), ('bMoldNarrowRightTem', boolean[:]),
# ('fCalibrateMouldBroadInnerTem', float32[:]), ('fCalibrateMouldBroadOuterTem', float32[:]),
# ('fCalibrateMouldNarrowLeftTem', float32[:]), ('fCalibrateMouldNarrowRightTem', float32[:]), ('fMouldInTemerature', float32),
# ('fMouldInTemerature', float32), ('CEDIAN_HEIGHT', int32), ('CEDIAN_WIDE', int32), ('fTemInnerWide', float32[:,:]),
# ('fTemOuterWide', float32[:,:]), ('fTemLeftNarrow' ,float32[:]), ('fTemRightNarrow', float32[:]), ('HEIGHT_COUNT', int32),
# ('WIDE_COUNT', int32), ('NARROW_COUNT', int32), ('fOuterWide', float32[:,:]), ('fInnerWide', float32[:,:]),
# ('fRightNarrow', float32[:,:]), ('fLeftNarrow', float32[:,:]), ('fOuterWide_Trick', float32[:,:]), ('fInnerWide_Trick', float32[:,:]),
# ('fRightNarrow_Trick', float32[:,:]), ('fLeftNarrow_Trick', float32[:,:]), ('Time_Interval', int32), ('fOuterWideQueue', float32[:,:,:]),
# ('fInnerWideQueue', float32[:,:,:]), ('fRightNarrowQueue', float32[:,:,:]), ('fLeftNarrowQueue', float32[:,:,:]),
# ('fWideLength', float32), ('fWideGrid', float32), ('fHeightLength', float32), ('fHeightGrid', float32), ('fNarrowLength', float32),
# ('fNarrowGrid', float32), ('fWideHengXiangJuLi', float32[:]), ('fZongXiangJuLi', float32[:]), ('fNarrowHengXiangJuLi', float32[:]),  # an array field
# ('fTemAdjust', int32)    # a simple scalar field
# ]


# @jitclass(spec)
