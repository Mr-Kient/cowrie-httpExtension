import re
import glob
import os
from collections import Counter

def analyze_log_file(log_file_path, all_ips, all_methods, all_post_data, all_urls):
    ip_regex = re.compile(r'Request from IP: (\d+\.\d+\.\d+\.\d+)')
    method_regex = re.compile(r"method: b'(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)'")
    post_data_start_regex = re.compile(r"\*{8}\s+Postdata Transport\s+\*{8}")
    post_data_end_regex = re.compile(r"\*{19}")
    url_regex = re.compile(r"uri: b'([^']+)'")
    post_data_content_regex = re.compile(r"b'([^']+)'")  # Regex to capture content between b' and '

    collecting_post_data = False
    current_post_data = []

    with open(log_file_path, 'r') as file:
        for line in file:
            ip_match = ip_regex.search(line)
            if ip_match:
                current_ip = ip_match.group(1)
                all_ips[current_ip] += 1

            method_match = method_regex.search(line)
            if method_match:
                method = method_match.group(1)
                all_methods[method] += 1

            url_match = url_regex.search(line)
            if url_match:
                url = url_match.group(1)
                all_urls[url] += 1

            if post_data_start_regex.search(line):
                collecting_post_data = True
            elif post_data_end_regex.search(line) and collecting_post_data:
                collecting_post_data = False
                # Join current POST data and count it
                post_data = ''.join(current_post_data)
                all_post_data[post_data] += 1
                current_post_data = []  # Reset for the next block
            elif collecting_post_data:
                post_data_match = post_data_content_regex.search(line)
                if post_data_match:
                    current_post_data.append(post_data_match.group(1).strip())

def analyze_directory(directory_path):
    all_ips = Counter()
    all_methods = Counter()
    all_post_data = Counter()
    all_urls = Counter()

    file_pattern = os.path.join(directory_path, 'HttpProxy-*.log')
    log_files = glob.glob(file_pattern)
    
    if not log_files:
        print("No log files found.")
        return

    for log_file in log_files:
        analyze_log_file(log_file, all_ips, all_methods, all_post_data, all_urls)

    print("\nTotal IP counts:", sum(all_ips.values()))
    print("Unique IPs:", len(all_ips))
    print("Top 10 IPs:", all_ips.most_common(10))
    print("HTTP methods usage:", all_methods)
    print("Top 10 POST data segments:", all_post_data.most_common(10))
    print("Top 10 URLs:", all_urls.most_common(10))

# Path to the directory containing your log files
directory_path = 'D:\\STUDY\\CPT\\FYP\\Cowrie materials\\cowrie log\\log\\http'
analyze_directory(directory_path)
