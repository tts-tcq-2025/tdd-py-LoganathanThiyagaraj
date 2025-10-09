import re

class StringCalculator:
    """
    A calculator for summing numbers from a string input,
    following specific rules for delimiters, negatives, and large numbers.
    """

    # CCN = 3 (entry + if < 0 + if <= 1000)
    def _parse_and_validate_number(self, num_str: str, negative_numbers: list) -> int:
        """
        Parses a single number string, collects negatives, and ignores numbers > 1000.
        Returns the number if valid for summing, otherwise 0.
        """
        number = int(num_str)

        if number < 0:
            negative_numbers.append(number)
            return 0  # Negative numbers are collected, but don't contribute to the sum
        
        if number <= 1000:
            return number
        
        # Numbers > 1000 are ignored
        return 0

    # CCN = 3 (entry + if starts with // + if delimiter_spec.contains("["))
    def _extract_delimiters_and_numbers(self, numbers_input: str) -> tuple:
        """
        Extracts custom delimiters and the number string to be parsed.
        Returns a tuple: (list_of_string_delimiters, list_of_char_delimiters, numbers_string_to_parse).
        """
        default_char_delimiters = [',', '\n']
        custom_string_delimiters = []
        numbers_to_parse = numbers_input

        if numbers_input.startswith("//"):
            try:
                # Find the first newline character after the //
                newline_index = numbers_input.index('\n')
                delimiter_spec = numbers_input[2:newline_index]

                if '[' in delimiter_spec: # Handles multi-char or multiple bracketed delimiters
                    # Example: "[***][*][%]"
                    # Use re.findall to extract contents within brackets
                    extracted_delimiters = re.findall(r"\[(.*?)\]", delimiter_spec)
                    for d in extracted_delimiters:
                        if d: # Ensure delimiter is not empty
                            custom_string_delimiters.append(re.escape(d)) # Escape for re.split
                else:
                    # Single character custom delimiter (e.g., "//;\n")
                    if delimiter_spec:
                        default_char_delimiters.append(delimiter_spec)

                numbers_to_parse = numbers_input[newline_index + 1:]
            except ValueError:
                # No newline found after "//", or other parsing error, treat as regular input
                pass # Fallback to default delimiters if custom delimiter format is malformed

        # For re.split, char delimiters can be combined into a regex character set
        # String delimiters need to be escaped and joined with '|' (OR)
        
        # Escape default char delimiters for regex, then combine with custom string delimiters
        # Note: re.escape(',') -> \, , re.escape('\n') -> \n
        regex_delimiters = [re.escape(d) for d in default_char_delimiters if isinstance(d, str)] + custom_string_delimiters

        return regex_delimiters, numbers_to_parse

    # CCN = 3 (entry + if IsNullOrEmpty + if negative_numbers)
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
        # Use '|' (OR) for multiple delimiters
        split_pattern = '|'.join(regex_delimiters)
        
        # Use re.split to split the string by multiple delimiters
        # re.split handles empty strings as results of consecutive delimiters
        # We then filter out empty strings
        number_str_list = [
            num.strip() for num in re.split(split_pattern, numbers_to_parse) if num.strip()
        ]

        negative_numbers = []
        total_sum = 0

        # Step 2 & 3: Parse and validate numbers, calculate sum
        for num_str in number_str_list: # CCN +1 for the loop
            total_sum += self._parse_and_validate_number(num_str, negative_numbers)

        # Step 4: Check for negative numbers and throw exception
        if negative_numbers: # CCN +1 for the if
            raise ValueError(f"negatives not allowed: {','.join(map(str, negative_numbers))}")

        return total_sum
