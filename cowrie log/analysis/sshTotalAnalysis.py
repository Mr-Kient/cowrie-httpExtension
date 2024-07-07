import json
import glob
import os
from collections import Counter

def analyze_cowrie_log(file_path, event_counts, src_ips, protocol_counts):
    # Define the event IDs of interest
    event_ids_of_interest = ['cowrie.session.connect', 'cowrie.command.input', 'cowrie.session.closed']
    
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

def analyze_all_logs(directory_path):
    # Construct the search pattern to match all log files of interest
    search_pattern = os.path.join(directory_path, 'cowrie_*.json')
    
    # Find all files matching the pattern
    log_files = glob.glob(search_pattern)
    
    # Initialize counters for events, protocols and a set for unique source IPs
    event_counts = {event_id: 0 for event_id in ['cowrie.session.connect', 'cowrie.command.input', 'cowrie.session.closed']}
    src_ips = set()
    protocol_counts = Counter()
    
    for file_path in log_files:
        # Analyze each log file and update the counters and set
        analyze_cowrie_log(file_path, event_counts, src_ips, protocol_counts)
    
    # Calculate the total number of unique source IPs
    unique_src_ips_count = len(src_ips)
    
    # Return the aggregated analysis results
    return event_counts, unique_src_ips_count, protocol_counts

# Example usage
directory_path = 'D:\\STUDY\\CPT\\FYP\\Cowrie materials\\cowrie log\\log\\ssh'
event_counts, unique_src_ips_count, protocol_counts = analyze_all_logs(directory_path)
print(f"Total events: {event_counts}")
print(f"Total unique source IPs: {unique_src_ips_count}")
print(f"Protocol counts: {protocol_counts}")
