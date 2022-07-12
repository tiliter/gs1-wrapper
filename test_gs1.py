import treepoem
import time
from typing import Callable
import pytest
import io


from gs1_barcode_enginer_wrapper import generate_gs1_datamatrix

# Barcode generation.
# Accepts input text which will be ASCII encoded then
# expressed as a barcode.
# Output is PNG encoded data as `bytes`
BarcodeGenerator = Callable[[str], bytes]


# time: ~230ms
def treepoem_generator(barcode_text: str) -> bytes:
    # todo: what size of barcode do i need to generate?!?!?!
    # looks like 20x20 for the time being.
    im = treepoem.generate_barcode(barcode_type="gs1datamatrix", data=barcode_text)
    # return im.tobytes(encoder_name="raw")
    stream = io.BytesIO()
    im.save(stream, format="PNG")
    barcode_png_data = stream.getvalue()

    save_to_file("output/treepoem.png", barcode_png_data)
    return barcode_png_data


def save_to_file(filename, data: bytes):
    with open(filename, "wb") as f:
        f.write(data)


# takes about 0.38ms on mac, 0.76ms on pi
def gs1_bartcode_engine_wrapper_generator(barcode_text: str) -> bytes:
    # use wrapper around https://github.com/gs1/gs1-barcode-engine
    # cloned to gs1-barcode-engine

    module_x_dim_mm = 0.7

    module_x_dim_inches = module_x_dim_mm * 0.0393701
    dpi = 157.35

    bmp_data = generate_gs1_datamatrix(
        barcode_text,
        dm_rows=22,
        dm_cols=22,
        x_undercut=0,
        y_undercut=0,
        scaling={"resolution": dpi, "target_x_dim": module_x_dim_inches},
    )

    save_to_file("output/gs1_barcode_enginer_wrapper.bmp", bmp_data)

    return bmp_data


@pytest.fixture
def barcode_text() -> str:
    return "(01)94210325403182(30)2(3922)0460(93)TQ"


@pytest.fixture
def generator() -> BarcodeGenerator:
    # return treepoem_generator
    return gs1_bartcode_engine_wrapper_generator


def test_barcode_generation(barcode_text: str, generator: BarcodeGenerator):

    # TODO maybe compare the differentt ypes.

    start = time.monotonic()
    barcode_bytes = generator(barcode_text)
    print(f"time taken={time.monotonic()-start}")
