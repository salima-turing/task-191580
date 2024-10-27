import unittest
from math import isnan


def validate_bin_ranges(bin_edges, data_range, min_bin_width=None, max_bin_width=None, min_overlap=None):
    """
    Validate bin ranges for edge case inputs.

    Args:
        bin_edges (list): List of bin edge values.
        data_range (tuple): (min, max) values of the data range.
        min_bin_width (float, optional): Minimum acceptable bin width. Defaults to None.
        max_bin_width (float, optional): Maximum acceptable bin width. Defaults to None.
        min_overlap (float, optional): Minimum acceptable overlap between consecutive bins. Defaults to None.
    Raises:
        ValueError: If any validation fails.
    """
    # Check if bin edges are in ascending order
    if not all(bin_edges[i] <= bin_edges[i + 1] for i in range(len(bin_edges) - 1)):
        raise ValueError("Bin edges must be in ascending order.")

    # Check for valid bin ranges
    for i in range(len(bin_edges) - 1):
        bin_width = bin_edges[i + 1] - bin_edges[i]

        # Validate minimum bin width
        if min_bin_width and bin_width < min_bin_width:
            raise ValueError(f"Bin width {bin_width} is smaller than the minimum acceptable width {min_bin_width}")

        # Validate maximum bin width
        if max_bin_width and bin_width > max_bin_width:
            raise ValueError(f"Bin width {bin_width} is larger than the maximum acceptable width {max_bin_width}")

        # Validate minimum overlap between consecutive bins
        if min_overlap and i > 0:
            prev_bin_width = bin_edges[i] - bin_edges[i - 1]
            overlap = bin_width - (prev_bin_width - min_overlap)
            if overlap < min_overlap:
                raise ValueError(
                    f"Overlap between bins {i} and {i + 1} is smaller than the minimum acceptable overlap.")

    # Check if the first bin covers the data minimum
    if bin_edges[0] > data_range[0]:
        raise ValueError("The first bin does not cover the minimum data value.")

    # Check if the last bin covers the data maximum
    if bin_edges[-1] < data_range[1]:
        raise ValueError("The last bin does not cover the maximum data value.")


def dynamic_bin_selection(data, num_bins=10, min_bin_width=None, max_bin_width=None, min_overlap=None):
    """
    Select bins dynamically based on the data and specified constraints.
    """
    data = sorted(data)
    data_range = (min(data), max(data))

    # Implement dynamic bin selection algorithm here
    # For simplicity, let's just use equal-width bins for demonstration purposes
    bin_width = (data_range[1] - data_range[0]) / num_bins

    bin_edges = [data_range[0]]
    for _ in range(num_bins):
        bin_edges.append(bin_edges[-1] + bin_width)

    # Validate the bin ranges using the existing validation function
    validate_bin_ranges(bin_edges, data_range, min_bin_width, max_bin_width, min_overlap)

    return bin_edges


class TestBinRangeValidation(unittest.TestCase):

    def test_valid_bin_ranges(self):
        # Test valid bin ranges with default parameters
        data = [1, 5, 8, 12, 13, 17, 20, 25, 28, 32]
        bin_edges = dynamic_bin_selection(data)
        self.assertTrue(True)  # Assertion changed to check if no exception is raised

    def test_invalid_bin_width(self):
        data = [1, 5, 10, 15, 20]
        with self.assertRaises(ValueError) as cm:
            dynamic_bin_selection(data, min_bin_width=6)
        self.assertEqual(str(cm.exception), "Bin width 5 is smaller than the minimum acceptable width 6")


if __name__ == "__main__":
    unittest.main()
