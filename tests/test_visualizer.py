from awo.visualizer import _as_unix_seconds, _build_plot_series


def test_as_unix_seconds_float():
    assert _as_unix_seconds(1000.5) == 1000.5


def test_as_unix_seconds_iso_string():
    value = _as_unix_seconds("2026-07-11T12:00:00")
    assert value is not None
    assert isinstance(value, float)


def test_as_unix_seconds_invalid_returns_none():
    assert _as_unix_seconds("not-a-timestamp") is None
    assert _as_unix_seconds(None) is None


def test_build_plot_series_elapsed_from_unix():
    logs = [
        {"timestamp": 200.0, "cpu_percent": 1.0, "memory_percent": 50.0},
        {"timestamp": 205.0, "cpu_percent": 2.0, "memory_percent": 51.0},
        {"timestamp": 210.0, "cpu_percent": 3.0, "memory_percent": 52.0},
    ]
    elapsed, cpu, memory = _build_plot_series(logs)
    assert elapsed == [0.0, 5.0, 10.0]
    assert cpu == [1.0, 2.0, 3.0]
    assert memory == [50.0, 51.0, 52.0]


def test_build_plot_series_sorts_out_of_order():
    logs = [
        {"timestamp": 210.0, "cpu_percent": 3.0, "memory_percent": 52.0},
        {"timestamp": 200.0, "cpu_percent": 1.0, "memory_percent": 50.0},
    ]
    elapsed, cpu, _ = _build_plot_series(logs)
    assert elapsed == [0.0, 10.0]
    assert cpu == [1.0, 3.0]