# Calculate Distances

[![PyPI - Version](https://img.shields.io/pypi/v/itaxotools-calculate-distances)](
    https://pypi.org/project/itaxotools-calculate-distances)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/itaxotools-calculate-distances)](
    https://pypi.org/project/itaxotools-calculate-distances)
[![PyPI - License](https://img.shields.io/pypi/l/itaxotools-calculate-distances)](
    https://pypi.org/project/itaxotools-calculate-distances)
[![GitHub - Tests](https://img.shields.io/github/actions/workflow/status/iTaxoTools/calculate_distances/test.yml?label=tests)](
    https://github.com/iTaxoTools/calculate_distances/actions/workflows/test.yml)

Calculate distances between DNA sequences. Leverages Rust for faster computation.

Originally part of [TaxI2](https://github.com/iTaxoTools/TaxI2).

## Installation

calculate_distances is available on PyPI. You can install it through `pip`:

```
pip install itaxotools-calculate-distances
```

## Usage

Import the distance calculation functions, each of which take two string arguments:

```
from itaxotools import calculate_distances as calc

x = "ACGT"
y = "AN-A"

calc.seq_distances_p(x, y)  # 0.5
calc.seq_distances_p_gaps(x, y)  # 0.66
calc.seq_distances_jukes_cantor(x, y)  # 0.82
calc.seq_distances_kimura2p(x, y)  # inf
```

## Unit tests

Only basic tests included. More extensive unit testing is currently done as part of [TaxI2](
    https://github.com/iTaxoTools/TaxI2/blob/main/tests/test_distances.py).
