from nechto_runtime.metrics import ethical_coefficient


def test_ethics_fallback():
    """When harm or identity values are missing, ethical_coefficient should return the worst-case fallback."""
    # missing harm
    assert ethical_coefficient(None, 0.5) == 0.1
    # missing alignment
    assert ethical_coefficient(0.5, None) == 0.1
    # missing both
    assert ethical_coefficient(None, None) == 0.1
