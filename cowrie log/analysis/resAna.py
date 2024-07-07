# Extract and display the number of unique IPs and the total count for all HTTP methods for each day from the log sample
import re
import os
from collections import Counter
# Initialize the results dictionary
results = []

with open('D:\\STUDY\\CPT\\FYP\\Cowrie materials\\cowrie log\\AnalysisResult\\analysisRes_http.txt', 'r') as file:
    log_sample = file.read()
# Iterate over each log entry and extract required information
for entry in log_sample.split("Analysis for: ")[1:]:
    # Extract the number of unique IPs
    unique_ips_count = int(re.search(r'Total unique IPs: (\d+)', entry).group(1))
    
    # Extract HTTP methods usage and calculate the total count of methods
    methods_usage = re.search(r'HTTP methods usage: ({[^}]+})', entry).group(1)
    total_methods_count = sum(eval(methods_usage).values())
    
    # Store the results
    results.append((total_methods_count, unique_ips_count))

print(results)
