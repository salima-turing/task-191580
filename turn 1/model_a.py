import unittest

def bin_data(data, bin_edges):

	# Automatic validation of bin edges
	if not all(bin_edges[i] < bin_edges[i+1] for i in range(len(bin_edges)-1)):
		raise ValueError("Bin edges must be sorted in ascending order and non-overlapping.")

	bins = []

	for value in data:
		for i in range(len(bin_edges) - 1):
			if bin_edges[i] <= value < bin_edges[i+1]:
				bins.append(i)
				break
		else:
			raise ValueError(f"Value {value} is outside the specified data range.")

	return bins

class TestBinningData(unittest.TestCase):

	def test_valid_binning(self):
		data = [1, 5, 3, 7, 2, 4, 6]
		bin_edges = [0, 3, 6, 10]
		expected_bins = [0, 1, 0, 2, 0, 1, 2]
		result = bin_data(data, bin_edges)
		self.assertEqual(result, expected_bins)

	def test_invalid_bin_edges(self):
		data = [1, 5]
		bin_edges = [1, 0, 3]  # Invalid bin edges: not sorted
		with self.assertRaises(ValueError) as context:
			bin_data(data, bin_edges)
		self.assertEqual(str(context.exception), "Bin edges must be sorted in ascending order and non-overlapping.")

	def test_value_outside_range(self):
		data = [1, 5, 10]
		bin_edges = [0, 3, 6]
		with self.assertRaises(ValueError) as context:
			bin_data(data, bin_edges)
		self.assertEqual(str(context.exception), "Value 10 is outside the specified data range.")

if __name__ == '__main__':
	unittest.main()
