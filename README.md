# BPlusTree

A Python implementation of a B+ Tree data structure for efficient key-value storage and retrieval, supporting insertion, deletion, search, range queries, and in-order traversal. This implementation is designed for educational and experimental purposes, and includes tools for performance benchmarking across various tree degrees.

## Features

- **B+ Tree Implementation**: Fully functional B+ Tree with adjustable degree (order).
- **Insertion & Deletion**: Efficiently add and remove elements while maintaining B+ Tree properties.
- **Search**: Fast lookup for keys (RIDs).
- **Range Queries**: Retrieve all keys within a specified range.
- **In-order Traversal**: List all keys in sorted order.
- **Performance Benchmarking**: Scripts for measuring operation times for varying tree sizes and degrees.
- **Unit Tests**: Automated tests for correctness and performance (see `unittest/test_bplus.py`).
- **Output Data**: CSV files with performance data for different degrees and sample sizes.

## Project Structure

```
.
├── src/
│   └── bplus.py          # B+ Tree implementation
├── data/
│   ├── collect.py        # Performance data collection script
│   └── output/           # CSV files with timing results
├── unittest/
│   ├── test_bplus.py     # Unit tests for B+ Tree
│   └── output/
│       └── out.txt       # Sample output from tests
├── LICENSE
└── README.md
```

## Getting Started

### Requirements

- Python 3.7+

### B+ Tree Usage Example

```python
from src.bplus import BPlusTree

tree = BPlusTree(deg=3)  # Create a B+ Tree with degree 3

# Insert elements
tree.insert(10, "a")
tree.insert(20, "b")

# Search
result = tree.search(10)
print(result)  # Output: "a"

# Delete
tree.delete(10)

# Inorder traversal
print(tree.inorder())  # Output: [20]
```

### Running Unit Tests

```bash
python -m unittest unittest/test_bplus.py
```

### Collecting Performance Data

You can benchmark the tree operations for various degrees and sample sizes:

```bash
python data/collect.py
```

You will be prompted to enter the B+ Tree degree and the number of samples per setting. Output will be saved in `data/output/` as a CSV file.

## Benchmark Output Files

The `data/output/` directory contains CSV files of the form:

- `out_deg{DEG}_avg{SAMPLES}_id{ID}.csv`

Each file records timing data for insertion, deletion, search, and in-order traversal across increasing element counts.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

- Based on classic database index literature and educational resources.
- Inspired by database systems coursework and public B+ Tree implementations.
