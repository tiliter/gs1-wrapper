# GS1 Library wrapper

A thin Python wrapper around https://github.com/gs1/gs1-barcode-engine.

Example usage: 

```
    import py_gs1_barcode_engine

    INCHES_PER_MM = 0.0393701
    dpi = 157.35
    module_x_dim_mm = 7
    module_x_dim_inches = module_x_dim_mm * INCHES_PER_MM

    bmp_data = py_gs1_barcode_engine.generate_gs1_datamatrix(
        "(01)94210325403182(30)2(3922)0460(93)TQ",
        dm_rows=22,
        dm_cols=22,
        x_undercut=0,
        y_undercut=0,
        scaling={"resolution": dpi, "target_x_dim": module_x_dim_inches},
    )

    with open("barcode.bmp", "wb") as f:
        f.write(bmp_data)
        
```

## Running tests

```
pip install -r requirements.txt
./compile_and_test_lib.sh
pytest
```
