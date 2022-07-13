import pathlib
import subprocess


def execute():
    """
        do the equivalent of the following shell script:

        rm -rf build_artifacts/*.*
        rm -rf gs1-barcode-engine

        git clone https://github.com/gs1/gs1-barcode-engine.git
        cd gs1-barcode-engine/src/c-lib
        git checkout 2021-09-10
        make test
        make
        cp build/*.* ../../../build_artifacts

        cd ../../..
        rm -rf gs1-barcode-engine
        """
        
    BUILD_ARTIFACTS_FOLDER_NAME = "build_artifacts"
    LIBRARY_NAME = "gs1-barcode-engine"
    build_root = pathlib.Path(__file__).resolve().parent
    source_location = build_root / LIBRARY_NAME / "src" / "c-lib"
    build_output = source_location / "build"
    build_artifacts_location = build_root / BUILD_ARTIFACTS_FOLDER_NAME

    _ = subprocess.check_output(["rm", "-rf", LIBRARY_NAME], cwd=build_root)
    _ = subprocess.check_output(
        ["rm", "-rf", BUILD_ARTIFACTS_FOLDER_NAME], cwd=build_root
    )

    _ = subprocess.check_output(
        ["git", "clone", "https://github.com/gs1/gs1-barcode-engine.git"],
        cwd=build_root,
    )
    _ = subprocess.check_output(["git", "checkout", "2021-09-10"], cwd=source_location)
    _ = subprocess.check_output(["make", "test"], cwd=source_location)
    _ = subprocess.check_output(["make"], cwd=source_location)
    _ = subprocess.check_output(
        ["rm", "-rf", BUILD_ARTIFACTS_FOLDER_NAME],
        cwd=build_root,
    )
    _ = subprocess.check_output(
        ["mkdir", BUILD_ARTIFACTS_FOLDER_NAME],
        cwd=build_root,
    )

    _ = subprocess.check_output(
        [f"cp *.* {str(build_artifacts_location)}"],  # hacky as hell
        cwd=build_output,
        shell=True,  # needed for wildcard operator to wokr
    )


if __name__ == "__main__":
    execute()
