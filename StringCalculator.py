import re

class StringCalculator:
    """
    A calculator for summing numbers from a string input,
    following specific rules for delimiters, negatives, and large numbers.
    """

    # CCN = 3 (entry + if < 0 + if <= 1000) - Compliant
    def _parse_and_validate_number(self, num_str: str, negative_numbers: list) -> int:
        """
        Parses a single number string, collects negatives, and ignores numbers > 1000.
        Returns the number if valid for summing, otherwise 0.
        """
        number = int(num_str)

        if number < 0:
            negative_numbers.append(number)
            return 0
        
        if number <= 1000:
            return number
        
        return 0


    # CCN = 3 (entry + for loop + if d) - Compliant
    def _add_extracted_delimiters(self, extracted_delimiters: list, custom_string_delimiters: list):
        """Adds escaped delimiters to the list if they are not empty."""
        for d in extracted_delimiters:
            if d:
                custom_string_delimiters.append(re.escape(d))

    # CCN = 2 (entry + if '[' in delimiter_spec) - Compliant
    def _parse_bracketed_delimiters(self, delimiter_spec: str, custom_string_delimiters: list):
        """Parses a bracketed delimiter specification (e.g., '[***][*][%]')"""
        if '[' in delimiter_spec:
            extracted_delimiters = re.findall(r"\[(.*?)\]", delimiter_spec)
            self._add_extracted_delimiters(extracted_delimiters, custom_string_delimiters)

    # CCN = 2 (entry + if delimiter_spec) - Compliant
    def _parse_single_char_delimiter(self, delimiter_spec: str, default_char_delimiters: list):
        """Parses a single character delimiter specification (e.g., ';')"""
        if delimiter_spec:
            default_char_delimiters.append(delimiter_spec)


    # CCN = 3 (entry + if '[' in delimiter_spec + else) - Compliant
    def _process_custom_delimiter_line(self, numbers_input_line: str, default_char_delimiters: list, custom_string_delimiters: list) -> str:
        """Processes the custom delimiter line part of the input string."""
        newline_index = numbers_input_line.index('\n')
        delimiter_spec = numbers_input_line[2:newline_index]

        if '[' in delimiter_spec:
             self._parse_bracketed_delimiters(delimiter_spec, custom_string_delimiters)
        else:
             self._parse_single_char_delimiter(delimiter_spec, default_char_delimiters)

        return numbers_input_line[newline_index + 1:]


    # CCN = 3 (entry + try + except) - Compliant
    def _handle_custom_delimiter_prefix(self, numbers_input: str, default_char_delimiters: list, custom_string_delimiters: list) -> str:
        """
        Handles the '//[delimiter]\n' prefix if present.
        Returns the remaining numbers string to parse.
        """
        try:
            return self._process_custom_delimiter_line(
                numbers_input, default_char_delimiters, custom_string_delimiters
            )
        except ValueError:
            return numbers_input


    # CCN = 3 (entry + list comprehension + if isinstance) - Compliant
    def _finalize_regex_delimiters(self, default_char_delimiters: list, custom_string_delimiters: list) -> list:
        """Combines and escapes all collected delimiters for regex splitting."""
        return [re.escape(d) for d in default_char_delimiters if isinstance(d, str)] + custom_string_delimiters


    # CCN = 3 (entry + if numbers_input.startswith("//") + if statement in finalize)
    # The 'if' in the list comprehension might be counting against this function's CCN if not careful.
    # The fix is to move the initialization logic out, so this function focuses *only* on the conditional.
    def _get_delimiters_and_numbers_from_prefix(self, numbers_input: str) -> tuple:
        """
        Processes the input to extract delimiters and the numbers string.
        Returns: (default_char_delimiters, custom_string_delimiters, numbers_to_parse)
        """
        default_char_delimiters = [',', '\n']
        custom_string_delimiters = []
        numbers_to_parse = numbers_input

        if numbers_input.startswith("//"): # CCN +1
            numbers_to_parse = self._handle_custom_delimiter_prefix(
                numbers_input, default_char_delimiters, custom_string_delimiters
            )
        
        return default_char_delimiters, custom_string_delimiters, numbers_to_parse


    # CCN = 1 (entry only) - NOW this one should be compliant!
    def _extract_delimiters_and_numbers(self, numbers_input: str) -> tuple:
        """
        Extracts custom delimiters and the number string to be parsed.
        Returns a tuple: (list_of_string_delimiters, list_of_char_delimiters, numbers_string_to_parse).
        """
        # Delegate all the conditional logic to the new helper
        default_char_delimiters, custom_string_delimiters, numbers_to_parse = \
            self._get_delimiters_and_numbers_from_prefix(numbers_input)

        # Finalize the regex delimiters
        regex_delimiters = self._finalize_regex_delimiters(default_char_delimiters, custom_string_delimiters)
        return regex_delimiters, numbers_to_parse


    # CCN = 3 (entry + list comprehension + if num.strip()) - Compliant
    def _split_numbers_string(self, numbers_to_parse: str, split_pattern: str) -> list:
        """Splits the numbers string using the given pattern and filters empty entries."""
        return [
            num.strip() for num in re.split(split_pattern, numbers_to_parse) if num.strip()
        ]

    # CCN = 2 (entry + for loop) - Compliant
    def _calculate_sum_and_find_negatives(self, number_str_list: list, negative_numbers: list) -> int:
        """Calculates the sum of numbers and collects any negatives."""
        total_sum = 0
        for num_str in number_str_list:
            total_sum += self._parse_and_validate_number(num_str, negative_numbers)
        return total_sum

    # CCN = 3 (entry + if not numbers + if negative_numbers) - Compliant
    def Add(self, numbers: str) -> int:
        """
        Calculates the sum of numbers in the input string.
        Supports various delimiters, ignores numbers > 1000, and throws
        an exception for negative numbers.
        """
        if not numbers:
            return 0

        # Step 1: Extract delimiters and the numbers string to parse
        regex_delimiters, numbers_to_parse = self._extract_delimiters_and_numbers(numbers)
        
        # Combine all delimiters into a single regex pattern for splitting
        split_pattern = '|'.join(regex_delimiters)
        
        # Split the numbers string
        number_str_list = self._split_numbers_string(numbers_to_parse, split_pattern)

        negative_numbers = []

        # Step 2 & 3: Parse and validate numbers, calculate sum
        total_sum = self._calculate_sum_and_find_negatives(number_str_list, negative_numbers)

        # Step 4: Check for negative numbers and throw exception
        if negative_numbers:
            raise ValueError(f"negatives not allowed: {','.join(map(str, negative_numbers))}")

        return total_sum
