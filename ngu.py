import re

# Define the regular expression pattern
pattern = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$'  # This pattern matches alphanumeric characters and underscores

# Define the string to check
string_to_check = "2013-05-01"

# Use re.match() to check if the string matches the pattern
match = re.match(pattern, string_to_check)

# Check if there is a match
if not match:
    print("String does not match the regular expression pattern.")
else:
    print("String matches the regular expression pattern.")