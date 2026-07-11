from awo.analyzer import _stats


def test_stats_min_max_avg():
    result = _stats([1.0, 2.0, 3.0, 4.0])
    assert result["min"] == 1.0
    assert result["max"] == 4.0
    assert result["avg"] == 2.5