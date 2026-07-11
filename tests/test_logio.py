import json
import pytest

from awo.logio import load_logs


def test_load_logs_reads_jsonl(tmp_path):
    log_file = tmp_path / "sample.jsonl"
    rows = [
        {"timestamp": "2026-07-11T12:00:00", "tag": "a", "cpu_percent": 1.0},
        {"timestamp": "2026-07-11T12:00:05", "tag": "b", "cpu_percent": 2.0},
    ]
    log_file.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n",
        encoding="utf-8",
    )

    loaded = load_logs(path=str(log_file))

    assert len(loaded) == 2
    assert loaded[0]["tag"] == "a"
    assert loaded[1]["cpu_percent"] == 2.0


def test_load_logs_skips_blank_lines(tmp_path):
    log_file = tmp_path / "sample.jsonl"
    log_file.write_text(
        '{"tag": "x", "cpu_percent": 1.0}\n\n{"tag": "y", "cpu_percent": 2.0}\n',
        encoding="utf-8",
    )

    loaded = load_logs(path=str(log_file))

    assert len(loaded) == 2


def test_load_logs_missing_file_raises(tmp_path):
    missing = tmp_path / "nope.jsonl"

    with pytest.raises(FileNotFoundError):
        load_logs(path=str(missing))