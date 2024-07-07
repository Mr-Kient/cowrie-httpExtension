import json
import glob
import os
from collections import Counter

def analyze_cowrie_log(file_path):
    # Define the event IDs of interest
    event_ids_of_interest = ['cowrie.session.connect', 'cowrie.command.input', 'cowrie.session.closed']
    
    # Initialize counters for events and protocols, and a set for unique source IP addresses
    event_counts = {event_id: 0 for event_id in event_ids_of_interest}
    protocol_counts = Counter()
    src_ips = set()

    # Read the file line by line and perform the analysis
    with open(file_path, 'r') as file:
        for line in file:
            event = json.loads(line.strip())
            if event['eventid'] in event_ids_of_interest:
                event_counts[event['eventid']] += 1
                if 'src_ip' in event:
                    src_ips.add(event['src_ip'])
                if event['eventid'] == 'cowrie.session.connect' and 'protocol' in event:
                    protocol_counts[event['protocol']] += 1

    # Calculate the number of unique source IPs
    unique_src_ips_count = len(src_ips)

    # Return the analysis results, including protocol counts
    return event_counts, unique_src_ips_count, protocol_counts

def analyze_all_logs(directory_path):
    # Construct the search pattern to match all log files of interest
    search_pattern = os.path.join(directory_path, 'cowrie_*.json')
    
    # Find all files matching the pattern
    log_files = glob.glob(search_pattern)
    
    # Dictionary to hold analysis results for each file
    all_analysis_results = {}
    
    for file_path in log_files:
        # Extracting the date from the filename
        base_name = os.path.basename(file_path)
        date_part = base_name.replace('cowrie_', '').replace('.json', '')
        
        # Analyze the current log file
        analysis_results = analyze_cowrie_log(file_path)
        
        # Store the results with the date as the key
        all_analysis_results[date_part] = analysis_results
    
    return all_analysis_results

# Example usage
directory_path = 'D:\\STUDY\\CPT\\FYP\\Cowrie materials\\cowrie log\\log\\ssh'
analysis_results = analyze_all_logs(directory_path)
for date, (event_counts, unique_ips, protocol_counts) in analysis_results.items():
    print(f"Date: {date}, Event Counts: {event_counts}, Unique IPs: {unique_ips}, Protocol Counts: {protocol_counts}")
