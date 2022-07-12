# TODO(EDWARD): packaging

import ctypes
from dataclasses import dataclass
from typing import Optional


class Gs1GeneratorError(Exception):
    pass


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

c_library.gs1_encoder_free.argtypes = [ctx_pointer_type]

c_library.gs1_encoder_getErrMsg.restype = ctypes.c_char_p
c_library.gs1_encoder_getErrMsg.argtypes = [ctx_pointer_type]


@dataclass
class ScalingParams:
    @classmethod
    def factory(cls, args: dict):
        if "pix_mult" in args:
            cls = PixelScaling
        else:
            cls = DeviceDotScaling

            args["min_x_dim"] = (
                args["min_x_dim"] if args.get("min_x_dim") is not None else 0
            )
            args["max_x_dim"] = (
                args["max_x_dim"] if args.get("max_x_dim") is not None else 0
            )
        return cls(**args)


@dataclass
class PixelScaling(ScalingParams):
    pix_mult: float


@dataclass
class DeviceDotScaling(ScalingParams):
    resolution: float
    min_x_dim: float
    target_x_dim: float
    max_x_dim: float


@dataclass
class DotScalingParams:
    resolution: float
    target_x_dim: float
    min_x_dim: Optional[float] = None
    max_x_dim: Optional[float] = None


# TODO read these enums from object file
gs1_encoder_sNONE = -1  #        ///< None defined
gs1_encoder_sDataBarOmni = 0  #     ///< GS1 DataBar Omnidirectional
gs1_encoder_sDataBarTruncated = 1  #     ///< GS1 DataBar Truncated
gs1_encoder_sDataBarStacked = 2  #     ///< GS1 DataBar Stacked
gs1_encoder_sDataBarStackedOmni = 3  #     ///< GS1 DataBar Stacked Omnidirectional
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


# TODO read these enums from object file
gs1_encoder_dBMP = 0
gs1_encoder_dTIF = 1
gs1_encoder_dRAW = 2


def error_things(ctx, result):

    if result:
        return

    msg = c_library.gs1_encoder_getErrMsg(ctx)
    raise Gs1GeneratorError(msg.decode("ascii"))


def generate_gs1_datamatrix(
    data: str,
    x_undercut: Optional[float] = None,
    y_undercut: Optional[float] = None,
    dm_rows: Optional[int] = None,
    dm_cols: Optional[int] = None,
    scaling: Optional[dict] = None,
) -> bytes:

    if scaling:
        scalingparams = ScalingParams.factory(scaling)
    else:
        scalingparams = None

    ctx = c_library.gs1_encoder_init(None)

    try:
        result = c_library.gs1_encoder_setFormat(ctx, gs1_encoder_dBMP)
        error_things(ctx, result)

        result = c_library.gs1_encoder_setOutFile(
            ctx, b""
        )  # output to buffer, not a file
        error_things(ctx, result)

        result = c_library.gs1_encoder_setSym(ctx, gs1_encoder_sDM)
        error_things(ctx, result)

        result = c_library.gs1_encoder_setAIdataStr(ctx, data.encode("ascii"))
        error_things(ctx, result)

        # more configuration

        if isinstance(scalingparams, PixelScaling):
            # 1. Pixel-based scaling system (no real world dimensions)
            result = c_library.gs1_encoder_setPixMult(ctx, scalingparams.pix_mult)
            error_things(ctx, result)
        elif isinstance(scalingparams, DeviceDotScaling):
            # 2. Device-dot scaling system (real world dimensions)
            result = c_library.gs1_encoder_setDeviceResolution(
                ctx, scalingparams.resolution
            )
            error_things(ctx, result)

            result = c_library.gs1_encoder_setXdimension(
                ctx,
                scalingparams.min_x_dim,
                scalingparams.target_x_dim,
                scalingparams.max_x_dim,
            )
            error_things(ctx, result)
        else:
            if scalingparams is None:
                pass
            else:
                assert False

        if x_undercut is not None:
            result = c_library.gs1_encoder_setXundercut(ctx, x_undercut)
            error_things(ctx, result)

        if y_undercut is not None:
            result = c_library.gs1_encoder_setYundercut(ctx, y_undercut)
            error_things(ctx, result)

        # Configure datamatrix parameters
        if dm_rows is not None:
            result = c_library.gs1_encoder_setDmRows(ctx, dm_rows)
            error_things(ctx, result)

        if dm_cols is not None:
            result = c_library.gs1_encoder_setDmColumns(ctx, dm_cols)
            error_things(ctx, result)

        # Generate output

        result = c_library.gs1_encoder_encode(ctx)
        error_things(ctx, result)

        size = c_library.gs1_encoder_getBufferSize(ctx)
        buffer = ctypes.create_string_buffer(size)

        got_size = c_library.gs1_encoder_copyOutputBuffer(ctx, buffer, size)
        assert got_size == size

        return buffer.raw
    finally:
        # pass
        c_library.gs1_encoder_free(ctx)
