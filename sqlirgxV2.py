import re
import os
import urllib.parse

# added urlib.parse
# Regular expression pattern to detect SQL injection attempts
# Added param
sql_injection_pattern = r"((\%27)|(\'))((\%6F)|o|(\%4F))(\%72|r|(\%52))"
param_pattern = r"(;|'|--|\/\*|xp_)"

# Path to the log file (run from same directory you run the script or put in full parh of file)
log_file = "iis_webserver.log"

# Check if the log file exists
if not os.path.isfile(log_file):
    print(f"Error: {log_file} does not exist.")
    exit()

# Initialize a list to store potential SQL injection attempts
potential_sql_injections = []

# Open the log file and analyze each line
with open(log_file, "r") as f:
    for line in f:
        # Check if the line matches the SQL injection pattern
        if re.search(sql_injection_pattern, line, re.IGNORECASE):
            potential_sql_injections.append(line.strip())

        # Check if the line contains a parameter matching the param_pattern
        param_match = re.search(param_pattern, line)
        if param_match:
            # URL-decode the parameter
            param_start = param_match.start()
            param_end = line.find(" ", param_start)
            param = line[param_start:param_end]
            decoded_param = urllib.parse.unquote(param)

            # Add the line with the decoded parameter to potential_sql_injections
            potential_sql_injections.append(f"{line[:param_start]}{decoded_param}{line[param_end:]}")

# Print the results
if potential_sql_injections:
    print("Potential SQL injection attempts detected:")
    for entry in potential_sql_injections:
        print(entry)
else:
    print("No potential SQL injection attempts detected.")