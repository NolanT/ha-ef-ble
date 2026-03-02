"""
Script to generate/regenerate protocol buffer source code and typing stubs

Typing stubs are used heavily for typing of device fields and can instantly catch
errors. However, they should not be versioned as they can be quite large and completely
useless for runtime.

This script requires `protoc` to be installed, see https://protobuf.dev/installation/

# Protobuf runtime version compatibility
Home Assistant pins its protobuf runtime to a specific version. Newer versions of
`protoc` generate a `ValidateProtobufRuntimeVersion(...)` call at the top of each
pb2 file that will raise a `VersionError` if the installed runtime is older than the
gencode version — even if the two versions are otherwise wire-compatible.

To keep the generated files compatible with HA's pinned runtime, this script
automatically strips the `ValidateProtobufRuntimeVersion` block (and its unused
`runtime_version` import) from every generated pb2 file after generation. This
matches the format used by pb2 files generated with older protoc versions that HA
has historically shipped.

If you see a VersionError like:
    google.protobuf.runtime_version.VersionError: Detected incompatible Protobuf
    Gencode/Runtime versions when loading <file>.proto: gencode X.Y.Z runtime A.B.C.
re-run this script to regenerate the pb2 files with the version check stripped.
"""  # noqa: INP001

import re
import subprocess
from pathlib import Path

from custom_components.ef_ble.eflib import pb

PB_OUT_PATH = Path(pb.__file__).parent

# Pattern matching the ValidateProtobufRuntimeVersion block inserted by newer protoc.
# This block causes VersionError when HA's pinned runtime is older than the gencode.
_VERSION_CHECK_RE = re.compile(
    r"from google\.protobuf import runtime_version as _runtime_version\n"
    r"_runtime_version\.ValidateProtobufRuntimeVersion\([^)]+\)\n",
    re.DOTALL,
)


def _strip_version_check(pb2_file: Path) -> None:
    """Remove the ValidateProtobufRuntimeVersion block from a generated pb2 file."""
    content = pb2_file.read_text()
    patched, count = _VERSION_CHECK_RE.subn("", content)
    if count:
        # Also remove the "NO CHECKED-IN PROTOBUF GENCODE" comment line added by newer
        # protoc alongside the version check.
        patched = patched.replace("# NO CHECKED-IN PROTOBUF GENCODE\n", "")
        pb2_file.write_text(patched)
        print(f"  stripped version check from {pb2_file.name}")


def generate_proto_typedefs():
    """Generate protocol buffer source code along with typing stubs"""
    proto_dir = Path(__file__).parent
    proto_files = [
        file.relative_to(proto_dir).as_posix() for file in proto_dir.glob("*.proto")
    ]
    subprocess.run(
        [
            "protoc",
            f"-I={proto_dir}",
            f"--python_out={PB_OUT_PATH}",
            f"--pyi_out={PB_OUT_PATH}",
            *proto_files,
        ],
        check=True,
    )
    for pb2_file in PB_OUT_PATH.glob("*_pb2.py"):
        _strip_version_check(pb2_file)


if __name__ == "__main__":
    generate_proto_typedefs()
