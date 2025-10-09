import re

class StringCalculator:
    """
    A calculator for summing numbers from a string input,
    following specific rules for delimiters, negatives, and large numbers.
    """

    # CCN = 3 (entry + if < 0 + if <= 1000) - Already compliant
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
        
        return 0 # Numbers > 1000 are ignored


    # --- New Helper Methods for _extract_delimiters_and_numbers ---

    # CCN = 2 (entry + if '[' in delimiter_spec)
    def _parse_bracketed_delimiters(self, delimiter_spec: str, custom_string_delimiters: list):
        """Parses a bracketed delimiter specification (e.g., '[***][*][%]')"""
        if '[' in delimiter_spec: # This check acts as the main conditional
            # Use re.findall to extract contents within brackets
            extracted_delimiters = re.findall(r"\[(.*?)\]", delimiter_spec)
            for d in extracted_delimiters: # CCN +1 for the loop implicitly
                if d: # Ensure delimiter is not empty
                    custom_string_delimiters.append(re.escape(d))

    # CCN = 2 (entry + if delimiter_spec)
    def _parse_single_char_delimiter(self, delimiter_spec: str, default_char_delimiters: list):
        """Parses a single character delimiter specification (e.g., ';')"""
        if delimiter_spec: # This check acts as the main conditional
            default_char_delimiters.append(delimiter_spec)


    # CCN = 3 (entry + if starts with // + if newline_index != -1)
    def _extract_delimiters_and_numbers(self, numbers_input: str) -> tuple:
        """
        Extracts custom delimiters and the number string to be parsed.
        Returns a tuple: (list_of_string_delimiters, list_of_char_delimiters, numbers_string_to_parse).
        """
        default_char_delimiters = [',', '\n']
        custom_string_delimiters = []
        numbers_to_parse = numbers_input

        if numbers_input.startswith("//"): # CCN +1
            try:
                newline_index = numbers_input.index('\n')
                if newline_index != -1: # CCN +1
                    delimiter_spec = numbers_input[2:newline_index]
                    
                    self._parse_bracketed_delimiters(delimiter_spec, custom_string_delimiters)
                    self._parse_single_char_delimiter(delimiter_spec, default_char_delimiters) # This might add redundant if both formats are present.

                    numbers_to_parse = numbers_input[newline_index + 1:]
            except ValueError:
                pass # Fallback to default if custom delimiter format is malformed

        # Escape default char delimiters for regex, then combine with custom string delimiters
        regex_delimiters = [re.escape(d) for d in default_char_delimiters if isinstance(d, str)] + custom_string_delimiters
        return regex_delimiters, numbers_to_parse

    # --- New Helper Method for Add ---
    
    # CCN = 2 (entry + for loop)
    def _calculate_sum_and_find_negatives(self, number_str_list: list, negative_numbers: list) -> int:
        """Calculates the sum of numbers and collects any negatives."""
        total_sum = 0
        for num_str in number_str_list: # CCN +1 for the loop
            total_sum += self._parse_and_validate_number(num_str, negative_numbers)
        return total_sum

    # CCN = 3 (entry + if not numbers + if negative_numbers)
    def Add(self, numbers: str) -> int:
        """
        Calculates the sum of numbers in the input string.
        Supports various delimiters, ignores numbers > 1000, and throws
        an exception for negative numbers.
        """
        if not numbers: # CCN +1
            return 0

        # Step 1: Extract delimiters and the numbers string to parse
        regex_delimiters, numbers_to_parse = self._extract_delimiters_and_numbers(numbers)
        
        # Combine all delimiters into a single regex pattern for splitting
        split_pattern = '|'.join(regex_delimiters)
        
        # Use re.split to split the string by multiple delimiters
        # We then filter out empty strings
        number_str_list = [
            num.strip() for num in re.split(split_pattern, numbers_to_parse) if num.strip()
        ]

        negative_numbers = []

        # Step 2 & 3: Parse and validate numbers, calculate sum
        total_sum = self._calculate_sum_and_find_negatives(number_str_list, negative_numbers)

        # Step 4: Check for negative numbers and throw exception
        if negative_numbers: # CCN +1
            raise ValueError(f"negatives not allowed: {','.join(map(str, negative_numbers))}")

        return total_sum
