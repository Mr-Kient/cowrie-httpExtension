import re
import glob
import os

def analyze_log_file(log_file_path, output_file):
    ip_regex = re.compile(r'Request from IP: (\d+\.\d+\.\d+\.\d+)')
    method_regex = re.compile(r"method: b'(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)'")
    post_data_start_regex = re.compile(r"\*{8}\s+Postdata Transport\s+\*{8}")
    post_data_end_regex = re.compile(r"\*{19}")
    post_data_content_regex = re.compile(r"b'([^']+)'")
    
    unique_ips = set()
    http_methods_counter = {}
    post_data_by_ip = {}
    collecting_post_data = False
    current_post_data = set()
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
                current_post_data = set()
            elif post_data_end_regex.search(line) and collecting_post_data:
                collecting_post_data = False
                # Add the POST data to the set associated with the current IP
                if current_ip not in post_data_by_ip:
                    post_data_by_ip[current_ip] = set()
                post_data_by_ip[current_ip].add(''.join(current_post_data))
            elif collecting_post_data:
                post_data_match = post_data_content_regex.search(line)
                if post_data_match:
                    current_post_data.add(post_data_match.group(1).strip())

    output_file.write(f"\nAnalysis for: {os.path.basename(log_file_path)}\n")
    output_file.write(f"Total unique IPs: {len(unique_ips)}\n")
    output_file.write(f"HTTP methods usage: {http_methods_counter}\n")
    
    total_unique_post_segments = sum(len(data) for data in post_data_by_ip.values())
    output_file.write(f"Total unique POST data segments across IPs: {total_unique_post_segments}\n")
    
    for ip, segments in post_data_by_ip.items():
        if segments:
            output_file.write(f"\nIP: {ip} - Unique POST data segments:\n")
            for segment in segments:
                output_file.write(f"{segment}\n")

def analyze_directory(directory_path):
    file_pattern = os.path.join(directory_path, 'HttpProxy-*.log')
    log_files = glob.glob(file_pattern)
    
    if not log_files:
        print("No log files found matching the pattern 'HttpProxy-yyyy_mm_dd.log'.")
        return

    with open('D:\\STUDY\\CPT\\FYP\\Cowrie materials\\cowrie log\\AnalysisResult\\analysisRes_http_.txt', 'w') as output_file:
        for log_file in log_files:
            analyze_log_file(log_file, output_file)

# Path to the directory containing your log files
directory_path = 'D:\\STUDY\\CPT\\FYP\\Cowrie materials\\cowrie log\\log\\http'
analyze_directory(directory_path)

'''
import re
import glob
import os

def analyze_log_file(log_file_path):
    ip_regex = re.compile(r'Request from IP: (\d+\.\d+\.\d+\.\d+)')
    method_regex = re.compile(r"method: b'(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)'")
    post_data_start_regex = re.compile(r"\*{8}\s+Postdata Transport\s+\*{8}")
    post_data_end_regex = re.compile(r"\*{19}")
    post_data_content_regex = re.compile(r"b'([^']+)'")
    
    unique_ips = set()
    http_methods_counter = {}
    post_data_by_ip = {}
    collecting_post_data = False
    current_post_data = set()
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
                current_post_data = set()
            elif post_data_end_regex.search(line) and collecting_post_data:
                collecting_post_data = False
                # Add the POST data to the set associated with the current IP
                if current_ip not in post_data_by_ip:
                    post_data_by_ip[current_ip] = set()
                post_data_by_ip[current_ip].add(''.join(current_post_data))
            elif collecting_post_data:
                post_data_match = post_data_content_regex.search(line)
                if post_data_match:
                    current_post_data.add(post_data_match.group(1).strip())

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

def analyze_directory(directory_path):
    file_pattern = os.path.join(directory_path, 'HttpProxy-*.log')
    log_files = glob.glob(file_pattern)
    
    if not log_files:
        print("No log files found matching the pattern 'HttpProxy-yyyy_mm_dd.log'.")
        return

    for log_file in log_files:
        analyze_log_file(log_file)

# Path to the directory containing your log files
directory_path = 'D:\\STUDY\\CPT\\FYP\\Cowrie materials\\cowrie log\\log\\http'
analyze_directory(directory_path)
'''