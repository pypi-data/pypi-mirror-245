from itaxotools import calculate_distances as calc


def test_basic():
    x = "agggtcgttaggtcagtcgt"
    y = "----tcg-taagtcagtcgt"
    precision = 0.00051

    assert calc.seq_distances_p(x, y) - 0.067 <= precision
    assert calc.seq_distances_p_gaps(x, y) - 0.125 <= precision
    assert calc.seq_distances_jukes_cantor(x, y) - 0.070 <= precision
    assert calc.seq_distances_kimura2p(x, y) - 0.072 <= precision
