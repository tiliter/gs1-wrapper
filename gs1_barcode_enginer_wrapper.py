# use wrapper around https://github.com/gs1/gs1-barcode-engine
# cloned to gs1-barcode-engine
# TODO(EDWARD): fix pathing
# TODO(EDWARD): packaging

import ctypes
from dataclasses import dataclass
from typing import Optional

# A. Create library
c_library = ctypes.CDLL("build_artifacts/libgs1encoders.so")


# define expected arguments and return types

ctx_pointer_type = ctypes.c_void_p  # hack


c_library.gs1_encoder_init.restype = ctx_pointer_type
c_library.gs1_encoder_init.argtypes = []

c_library.gs1_encoder_setFormat.restype = ctypes.c_bool
c_library.gs1_encoder_setFormat.argtypes = [ctx_pointer_type, ctypes.c_int]

c_library.gs1_encoder_setOutFile.restype = ctypes.c_bool
c_library.gs1_encoder_setOutFile.argtypes = [ctx_pointer_type, ctypes.c_char_p]

c_library.gs1_encoder_setSym.restype = ctypes.c_bool
c_library.gs1_encoder_setSym.argtypes = [ctx_pointer_type, ctypes.c_int]

c_library.gs1_encoder_setDataStr.restype = ctypes.c_bool
c_library.gs1_encoder_setDataStr.argtypes = [ctx_pointer_type, ctypes.c_char_p]

c_library.gs1_encoder_setAIdataStr.restype = ctypes.c_bool
c_library.gs1_encoder_setAIdataStr.argtypes = [ctx_pointer_type, ctypes.c_char_p]


# gs1_encoder_setPixMult (gs1_encoder *ctx, int pixMult)
c_library.gs1_encoder_setPixMult.restype = ctypes.c_bool
c_library.gs1_encoder_setPixMult.argtypes = [ctx_pointer_type, ctypes.c_int]


# gs1_encoder_setDeviceResolution (gs1_encoder *ctx, double resolution)
c_library.gs1_encoder_setDeviceResolution.restype = ctypes.c_bool
c_library.gs1_encoder_setDeviceResolution.argtypes = [ctx_pointer_type, ctypes.c_double]


# gs1_encoder_setXdimension (gs1_encoder *ctx, double min, double target, double max)
c_library.gs1_encoder_setXdimension.restype = ctypes.c_bool
c_library.gs1_encoder_setXdimension.argtypes = [
    ctx_pointer_type,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]


# gs1_encoder_setXundercut (gs1_encoder *ctx, int Xundercut)
c_library.gs1_encoder_setXundercut.restype = ctypes.c_bool
c_library.gs1_encoder_setXundercut.argtypes = [ctx_pointer_type, ctypes.c_int]


# gs1_encoder_setYundercut (gs1_encoder *ctx, int Yundercut)
c_library.gs1_encoder_setYundercut.restype = ctypes.c_bool
c_library.gs1_encoder_setYundercut.argtypes = [ctx_pointer_type, ctypes.c_int]


# gs1_encoder_setDmRows (gs1_encoder *ctx, int rows)
c_library.gs1_encoder_setDmRows.restype = ctypes.c_bool
c_library.gs1_encoder_setDmRows.argtypes = [ctx_pointer_type, ctypes.c_int]


# gs1_encoder_setDmColumns (gs1_encoder *ctx, int columns)
c_library.gs1_encoder_setDmColumns.restype = ctypes.c_bool
c_library.gs1_encoder_setDmColumns.argtypes = [ctx_pointer_type, ctypes.c_int]


c_library.gs1_encoder_encode.restype = ctypes.c_bool
c_library.gs1_encoder_encode.argtypes = [ctx_pointer_type]

c_library.gs1_encoder_getBufferSize.restype = ctypes.c_size_t
c_library.gs1_encoder_getBufferSize.argtypes = [ctx_pointer_type]

c_library.gs1_encoder_copyOutputBuffer.restype = ctypes.c_size_t
c_library.gs1_encoder_copyOutputBuffer.argtypes = [
    ctx_pointer_type,
    ctypes.c_void_p,
    ctypes.c_size_t,
]


c_library.gs1_encoder_getBuffer.restype = ctypes.c_size_t
c_library.gs1_encoder_getBuffer.argtypes = [ctx_pointer_type]


# c_library.gs1_encoder_free.restype=ctypes.
c_library.gs1_encoder_free.argtypes = [ctx_pointer_type]


# TODO: handle errors properly


@dataclass
class ScalingParams:
    pass


@dataclass
class PixelScaling(ScalingParams):
    pix_mult: float


@dataclass
class DeviceDotScaling(ScalingParams):
    resolution: float
    min_x_dim: float
    target_x_dim: float
    max_x_dim: float


def scaling_params_factory(args: dict) -> ScalingParams:
    if "pix_mult" in args:
        cls = PixelScaling
    else:
        cls = DeviceDotScaling
        
        args['min_x_dim']=args['min_x_dim'] if args.get('min_x_dim') is not None else 0
        args['max_x_dim']=args['max_x_dim'] if args.get('max_x_dim') is not None else 0
    return cls(**args)


@dataclass
class DotScalingParams:
    resolution: float
    target_x_dim: float
    min_x_dim: Optional[float] = None
    max_x_dim: Optional[float] = None


def generate_gs1_datamatrix(
    data: str,
    x_undercut: Optional[float] = None,
    y_undercut: Optional[float] = None,
    dm_rows: Optional[int] = None,
    dm_cols: Optional[int] = None,
    scaling: Optional[dict] = None,
) -> bytes:

    if scaling:
        scalingparams = scaling_params_factory(scaling)
    else:
        scalingparams=None

    ctx = c_library.gs1_encoder_init(None)

    try:

        # TODO read these enums from object file
        gs1_encoder_dBMP = 0
        gs1_encoder_dTIF = 1
        gs1_encoder_dRAW = 2
        result = c_library.gs1_encoder_setFormat(ctx, gs1_encoder_dBMP)
        assert result is True

        result = c_library.gs1_encoder_setOutFile(ctx, b"")  # set to buffer
        assert result is True

        # TODO read these enums from object file
        gs1_encoder_sNONE = -1  #        ///< None defined
        gs1_encoder_sDataBarOmni = 0  #     ///< GS1 DataBar Omnidirectional
        gs1_encoder_sDataBarTruncated = 1  #     ///< GS1 DataBar Truncated
        gs1_encoder_sDataBarStacked = 2  #     ///< GS1 DataBar Stacked
        gs1_encoder_sDataBarStackedOmni = (
            3  #     ///< GS1 DataBar Stacked Omnidirectional
        )
        gs1_encoder_sDataBarLimited = 4  #     ///< GS1 DataBar Limited
        gs1_encoder_sDataBarExpanded = 5  #     ///< GS1 DataBar Expanded (Stacked)
        gs1_encoder_sUPCA = 6  #     ///< UPC-A
        gs1_encoder_sUPCE = 7  #     ///< UPC-E
        gs1_encoder_sEAN13 = 8  #     ///< EAN-13
        gs1_encoder_sEAN8 = 9  #     ///< EAN-8
        gs1_encoder_sGS1_128_CCA = 10  #     ///< GS1-128 with CC-A or CC-B
        gs1_encoder_sGS1_128_CCC = 11  #     ///< GS1-128 with CC-C
        gs1_encoder_sQR = 12  #     ///< (GS1) QR Code
        gs1_encoder_sDM = 13  #     ///< (GS1) Data Matrix
        gs1_encoder_sNUMSYMS = 14  #     ///< Value is the number of symbologies

        result = c_library.gs1_encoder_setSym(ctx, gs1_encoder_sDM)
        assert result is True

        result = c_library.gs1_encoder_setAIdataStr(ctx, data.encode("ascii"))
        assert result is True

        # more configuration

        # 1. Pixel-based scaling system (no real world dimensions)

        if isinstance(scalingparams, PixelScaling):
            result = c_library.gs1_encoder_setPixMult(ctx, scalingparams.pix_mult)
            assert result is True
        elif isinstance(scalingparams, DeviceDotScaling):
            # 2. Device-dot scaling system (real world dimensions)
            # result=c_library.gs1_encoder_setDeviceResolution.argtypes=[ctx_pointer_type,ctypes.c_double]
            # set device resolution in dots per unit. to be used with and before setXdimension
            result = c_library.gs1_encoder_setDeviceResolution(
                ctx, scalingparams.resolution
            )
            assert result is True

            # result=c_library.gs1_encoder_setXdimension.argtypes=[ctx_pointer_type,ctypes.c_double,ctypes.c_double,ctypes.c_double]
            result = c_library.gs1_encoder_setXdimension(
                ctx,
                scalingparams.min_x_dim,
                scalingparams.target_x_dim,
                scalingparams.max_x_dim,
            )
            assert result is True
        else:
            if scalingparams is None:
                pass
            else:
                assert False

        # calibration: set undercut

        # result=c_library.gs1_encoder_setXundercut.argtypes=[ctx_pointer_type,ctypes.c_int]
        if x_undercut is not None:
            result = c_library.gs1_encoder_setXundercut(ctx, x_undercut)
            assert result is True

        if y_undercut is not None:
            # result=c_library.gs1_encoder_setYundercut.argtypes=[ctx_pointer_type,ctypes.c_int]
            result = c_library.gs1_encoder_setYundercut(ctx, y_undercut)
            assert result is True

        # cionfigure datamatrix

        # result=c_library.gs1_encoder_setDmRows.argtypes=[ctx_pointer_type,ctypes.c_int]

        if dm_rows is not None:
            result = c_library.gs1_encoder_setDmRows(ctx, dm_rows)
            assert result is True

        if dm_cols is not None:
            # result=c_library.gs1_encoder_setDmColumns.argtypes=[ctx_pointer_type,ctypes.c_int]
            result = c_library.gs1_encoder_setDmColumns(ctx, dm_cols)
            assert result is True

        # do actual things

        result = c_library.gs1_encoder_encode(ctx)
        assert result is True

        size = c_library.gs1_encoder_getBufferSize(ctx)
        buffer = ctypes.create_string_buffer(size)

        got_size = c_library.gs1_encoder_copyOutputBuffer(ctx, buffer, size)
        assert got_size == size

        return buffer.raw
    finally:
        c_library.gs1_encoder_free(ctx)


# with open("itsaslive.bmp", "rb") as f:
#     baseline_data=f.read()
#     print()


# things = get_bmp_data("(01)94210325403182(30)2(3922)0460(93)TQ")
# assert things==baseline_data
