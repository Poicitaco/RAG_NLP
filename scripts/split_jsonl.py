"""Split large JSONL files into GitHub-friendly shards."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def split_jsonl(input_path: Path, output_dir: Path, prefix: str, max_mb: int) -> list[dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    max_bytes = max_mb * 1024 * 1024
    manifest = []
    part = 1
    current_path = output_dir / f"{prefix}_part{part:03d}.jsonl"
    handle = current_path.open("w", encoding="utf-8")
    rows = 0
    bytes_written = 0

    def close_part() -> None:
        nonlocal handle, rows, bytes_written
        handle.close()
        manifest.append(
            {
                "path": current_path.as_posix(),
                "rows": rows,
                "bytes": current_path.stat().st_size,
            }
        )

    with input_path.open("r", encoding="utf-8") as source:
        for line in source:
            encoded_size = len(line.encode("utf-8"))
            if rows > 0 and bytes_written + encoded_size > max_bytes:
                close_part()
                part += 1
                current_path = output_dir / f"{prefix}_part{part:03d}.jsonl"
                handle = current_path.open("w", encoding="utf-8")
                rows = 0
                bytes_written = 0
            handle.write(line)
            rows += 1
            bytes_written += encoded_size
    close_part()
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--max-mb", type=int, default=80)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    manifest = split_jsonl(Path(args.input), Path(args.output_dir), args.prefix, args.max_mb)
    payload = {
        "source": args.input,
        "max_mb": args.max_mb,
        "parts": manifest,
        "total_rows": sum(int(part["rows"]) for part in manifest),
        "total_bytes": sum(int(part["bytes"]) for part in manifest),
    }
    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"split {args.input} into {len(manifest)} parts")
    print(f"saved manifest to {args.manifest}")


if __name__ == "__main__":
    main()
