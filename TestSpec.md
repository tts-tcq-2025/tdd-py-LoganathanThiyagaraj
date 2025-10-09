| Test ID | 	Test Name                        		| Input                  		| Expected Output / Behavior                  |  Description                                 										|
|---------|---------------------------------------------|-------------------------------|-----------------------------------------------|-----------------------------------------------------------------------------------|
| TC-01   | 	EmptyStringReturnsZero   	 			| ""							| 0												| Empty string returns 0 															|
| TC-02   | 	SingleNumberReturnsItself   			| "5"							| 5												| Single number returns its value 													|
| TC-03   | 	TwoNumbersCommaSeparated	   			| "1,2"							| 3												| Two numbers separated by comma 													|
| TC-04   | 	UnknownAmountOfNumbers	   				| "1,2,3,4"						| 10											| Multiple numbers separated by commas 												|
| TC-05   | 	NewLinesAsDelimiter	   					| "1\n2,3"						| 6												| Numbers separated by newlines and commas 											|
| TC-06   | 	CustomSingleCharDelimiter	   			| "//;\n1;2"					| 3												| Custom single-character delimiter 												|
| TC-07   | 	NegativesThrowExceptionSingle	   		| "1,-2"						| Exception: ("negatives not allowed: -2") 		| Single negative number throws exception 											|	
| TC-08   | 	NegativesThrowExceptionMultiple	   		| "1,-2,3,-4"					| Exception: ("negatives not allowed: -2,-4") 	| Multiple negative numbers listed in exception message 							|
| TC-09   | 	IgnoreNumbersGreaterThan1000	      	| "2,1001"						| 2												| Numbers greater than 1000 are ignored 											|
| TC-10   | 	CustomMultiCharOrMultipleDelimiters   	| "//[][][%]\n123%4"			| 10											| Custom multi-character and multiple single-character delimiters 					|
| TC-11   | 	CustomDelimiterWithNegativeNumber	   	| "//[x]\n1x-2x3"				| Exception: ("negatives not allowed: -2") 		| Custom delimiter with a negative number 											|
| TC-12   | 	CustomDelimiterWithNumbersOver1000	   	| "//[;]\n1;1001;2"				| 3												| Custom delimiter with numbers over 1000 ignored 									|
| TC-13   | 	InvalidInput_CommaFollowedByNewline	   	| "1,\n"						| FormatException 								| Input with a comma followed by a newline is considered invalid/malformed 	   		|
| TC-14   | 	AllFeaturesCombined	   					| "//[;][foo]\n1;2foo-3;1001"	| Exception: ("negatives not allowed: -3") 		| Combines custom multi-char/multiple delimiters, negatives, and ignored numbers	|
| TC-15   | 	MixedDefaultAndCustomDelimiters	   		| "//[bar]\n1,2\n3bar4"			| 10											| Uses default and custom delimiters simultaneously 								|
