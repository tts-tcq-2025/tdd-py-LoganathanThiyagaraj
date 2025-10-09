import pytest
from string_calculator import StringCalculator # Assuming the class is in string_calculator.py

class TestStringCalculator:
    """
    Test suite for the StringCalculator class.
    """

    @pytest.fixture
    def calculator(self):
        """Provides a fresh StringCalculator instance for each test."""
        return StringCalculator()

    def test_tc01_add_empty_string_returns_zero(self, calculator):
        """TC-01: Empty string returns 0."""
        assert calculator.Add("") == 0

    def test_tc02_add_single_number_returns_number(self, calculator):
        """TC-02: Single number returns its value."""
        assert calculator.Add("5") == 5

    def test_tc03_add_two_numbers_comma_separated_returns_sum(self, calculator):
        """TC-03: Two numbers separated by comma."""
        assert calculator.Add("1,2") == 3

    def test_tc04_add_unknown_amount_of_numbers_returns_sum(self, calculator):
        """TC-04: Multiple numbers separated by commas."""
        assert calculator.Add("1,2,3,4") == 10

    def test_tc05_add_new_lines_as_delimiter_returns_sum(self, calculator):
        """TC-05: Numbers separated by newlines and commas."""
        assert calculator.Add("1\n2,3") == 6

    def test_tc06_add_custom_single_char_delimiter_returns_sum(self, calculator):
        """TC-06: Custom single-character delimiter."""
        assert calculator.Add("//;\n1;2") == 3

    def test_tc07_add_single_negative_number_throws_exception(self, calculator):
        """TC-07: Single negative number throws exception."""
        with pytest.raises(ValueError) as excinfo:
            calculator.Add("1,-2")
        assert "negatives not allowed: -2" in str(excinfo.value)

    def test_tc08_add_multiple_negative_numbers_throws_exception(self, calculator):
        """TC-08: Multiple negative numbers listed in exception message."""
        with pytest.raises(ValueError) as excinfo:
            calculator.Add("1,-2,3,-4")
        assert "negatives not allowed: -2,-4" in str(excinfo.value)

    def test_tc09_add_numbers_greater_than_1000_are_ignored(self, calculator):
        """TC-09: Numbers greater than 1000 are ignored."""
        assert calculator.Add("2,1001") == 2
        assert calculator.Add("1000,2") == 1002 # 1000 is not ignored
        assert calculator.Add("1001,2000") == 0 # Both ignored

    def test_tc10_add_custom_multi_char_or_multiple_delimiters_returns_sum(self, calculator):
        """TC-10: Custom multi-character and multiple single-character delimiters."""
        assert calculator.Add("//[***][*][%]\n1***2*3%4") == 10

    def test_tc11_add_custom_delimiter_with_negative_number_throws_exception(self, calculator):
        """TC-11: Custom delimiter with a negative number."""
        with pytest.raises(ValueError) as excinfo:
            calculator.Add("//[x]\n1x-2x3")
        assert "negatives not allowed: -2" in str(excinfo.value)

    def test_tc12_add_custom_delimiter_with_numbers_over_1000_returns_sum(self, calculator):
        """TC-12: Custom delimiter with numbers over 1000 ignored."""
        assert calculator.Add("//[;]\n1;1001;2") == 3

    def test_tc13_add_invalid_input_comma_followed_by_newline_produces_expected_sum(self, calculator):
        """
        TC-13: Input with a comma followed by a newline is considered invalid/malformed
        by the spec, but our robust parser (using re.split with filter) handles it
        by effectively ignoring the empty string caused by consecutive delimiters.
        Thus, "1,\n" becomes "1" after splitting, which sums to 1.
        """
        assert calculator.Add("1,\n") == 1
        assert calculator.Add("1,\n2") == 3 # For context

    def test_tc14_add_all_features_combined_throws_exception_for_negatives(self, calculator):
        """TC-14: Combines custom multi-char/multiple delimiters, negatives, and ignored numbers."""
        with pytest.raises(ValueError) as excinfo:
            calculator.Add("//[;][foo]\n1;2foo-3;1001")
        assert "negatives not allowed: -3" in str(excinfo.value)

    def test_tc15_add_mixed_default_and_custom_delimiters_returns_sum(self, calculator):
        """TC-15: Uses default and custom delimiters simultaneously."""
        assert calculator.Add("//[bar]\n1,2\n3bar4") == 10
