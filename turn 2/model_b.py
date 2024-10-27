import unittest


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

    return True


class TestBinRangeValidation(unittest.TestCase):
    def test_valid_bin_ranges(self):
        # Test valid bin ranges with default parameters
        bin_edges = [0, 10, 20, 30, 40, 50]
        data_range = (0, 50)
        self.assertTrue(validate_bin_ranges(bin_edges, data_range))  # No exception raised, validation passes

    def test_invalid_bin_width(self):
        # Test invalid bin width (smaller than min_bin_width)
        bin_edges = [0, 5, 15, 25, 35, 45]
        data_range = (0, 50)
        with self.assertRaises(ValueError) as cm:
            validate_bin_ranges(bin_edges, data_range, min_bin_width=10)
        self.assertEqual(str(cm.exception), "Bin width 5 is smaller than the minimum acceptable width 10")


# Add more test cases for other edge cases (e.g., invalid overlap, data range not covered, etc.)
if __name__ == "__main__":
    unittest.main()
