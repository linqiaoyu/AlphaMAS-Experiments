#!/usr/bin/env python3
"""Pack the frozen Formal M0 tree without adding host-specific metadata."""

from __future__ import annotations

import sys
import io
import subprocess
import tarfile
import time
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: pack_m0_raw_bundle.py SOURCE_TREE OUTPUT_TAR_GZ")
    source = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    if not source.is_dir():
        raise SystemExit(f"source tree does not exist: {source}")
    output.parent.mkdir(parents=True, exist_ok=True)
    root_name = source.name
    paths = [source, *sorted(source.rglob("*"))]
    with tarfile.open(output, mode="w:gz", compresslevel=6, format=tarfile.PAX_FORMAT) as archive:
        for path in paths:
            relative_name = root_name if path == source else f"{root_name}/{path.relative_to(source)}"
            info = archive.gettarinfo(str(path), arcname=relative_name)
            if info.isreg():
                data = b""
                for _ in range(20):
                    try:
                        data = subprocess.check_output(["/bin/cat", str(path)], timeout=10)
                    except (OSError, subprocess.SubprocessError):
                        data = b""
                    if len(data) == info.size:
                        break
                    time.sleep(0.1)
                if len(data) != info.size:
                    raise OSError(
                        f"could not pack {path}: tar_size={info.size}, "
                        f"stat_size={path.stat().st_size}, read_size={len(data)}"
                    )
                archive.addfile(info, io.BytesIO(data))
            else:
                archive.addfile(info)


if __name__ == "__main__":
    main()
