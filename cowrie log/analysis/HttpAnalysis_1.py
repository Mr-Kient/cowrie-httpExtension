import re
import os
'''
def analyze_log_file(log_file_path):
    # Regular expressions for matching lines of interest
    ip_regex = re.compile(r'Request from IP: (\d+\.\d+\.\d+\.\d+)')
    method_regex = re.compile(r"method: b'(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)'")
    post_data_start_regex = re.compile(r"\*{8}\s+Postdata Transport\s+\*{8}")
    post_data_end_regex = re.compile(r"\*{19}")
    
    # Initialize counters and variables
    ip_requests_counter = {}
    http_methods_counter = {}
    collected_post_data = []
    collecting_post_data = False
    post_data_temp = []

    # Open and process the log file
    with open(log_file_path, 'r') as file:
        for line in file:
            # Check for IP requests
            ip_match = ip_regex.search(line)
            if ip_match:
                ip = ip_match.group(1)
                if ip in ip_requests_counter:
                    ip_requests_counter[ip] += 1
                else:
                    ip_requests_counter[ip] = 1

            # Check for HTTP methods
            method_match = method_regex.search(line)
            if method_match:
                method = method_match.group(1)
                if method in http_methods_counter:
                    http_methods_counter[method] += 1
                else:
                    http_methods_counter[method] = 1

            # Extract POST data
            if post_data_start_regex.search(line):
                collecting_post_data = True
                post_data_temp = []
            elif post_data_end_regex.search(line) and collecting_post_data:
                collecting_post_data = False
                collected_post_data.append("".join(post_data_temp))
            elif collecting_post_data:
                post_data_temp.append(line.strip())

    # Results
    total_ip_requests = sum(ip_requests_counter.values())
    unique_ip_count = len(ip_requests_counter)
    specific_post_data_count = sum(1 for data in collected_post_data if "username = admin & psd = Feefifofum" in data)

    print(f"Total Number of IP Requests: {total_ip_requests} from {unique_ip_count} unique IPs")
    print(f"HTTP Methods Used: {http_methods_counter}")
    print(f"Total Extracted POST Data Segments: {len(collected_post_data)}")
    print(f"Segments Matching Specific Criteria: {specific_post_data_count}")
'''
def analyze_log_file(log_file_path):
    ip_regex = re.compile(r'Request from IP: (\d+\.\d+\.\d+\.\d+)')
    method_regex = re.compile(r"method: b'(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)'")
    post_data_start_regex = re.compile(r"\*{8}\s+Postdata Transport\s+\*{8}")
    post_data_end_regex = re.compile(r"\*{19}")
    
    unique_ips = set()
    http_methods_counter = {}
    post_data_by_ip = {}
    collecting_post_data = False
    current_post_data = []
    current_ip = None

    with open(log_file_path, 'r') as file:
        for line in file:
            ip_match = ip_regex.search(line)
            if ip_match:
                current_ip = ip_match.group(1)
                unique_ips.add(current_ip)

            method_match = method_regex.search(line)
            if method_match:
                method = method_match.group(1)
                http_methods_counter[method] = http_methods_counter.get(method, 0) + 1

            if post_data_start_regex.search(line):
                collecting_post_data = True
                current_post_data = []
            elif post_data_end_regex.search(line) and collecting_post_data:
                collecting_post_data = False
                # Add the POST data to the set associated with the current IP
                if current_ip not in post_data_by_ip:
                    post_data_by_ip[current_ip] = set()
                post_data_by_ip[current_ip].add(''.join(current_post_data))
            elif collecting_post_data:
                current_post_data.append(line.strip())

    print(f"\nAnalysis for: {os.path.basename(log_file_path)}")
    print(f"Total unique IPs: {len(unique_ips)}")
    print(f"HTTP methods usage: {http_methods_counter}")
    
    total_unique_post_segments = sum(len(data) for data in post_data_by_ip.values())
    print(f"Total unique POST data segments across IPs: {total_unique_post_segments}")
    
    for ip, segments in post_data_by_ip.items():
        if segments:
            print(f"\nIP: {ip} - Unique POST data segments:")
            for segment in segments:
                print(segment)

# Path to your log file
log_file_path = 'D:\\STUDY\\CPT\\FYP\\Cowrie materials\\cowrie log\\log\\HttpProxy-2024_4_8.log'
analyze_log_file(log_file_path)
