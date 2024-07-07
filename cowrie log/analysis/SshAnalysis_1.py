import json

def analyze_cowrie_log(file_path):
    # Define the event IDs of interest
    event_ids_of_interest = ['cowrie.session.connect', 'cowrie.command.input', 'cowrie.session.closed']
    
    # Initialize counters and a set for unique source IP addresses
    event_counts = {event_id: 0 for event_id in event_ids_of_interest}
    src_ips = set()

    # Read the file line by line and perform the analysis
    with open(file_path, 'r') as file:
        for line in file:
            event = json.loads(line.strip())  # Parsing each line as a separate JSON object
            if event['eventid'] in event_ids_of_interest:
                event_counts[event['eventid']] += 1
                if 'src_ip' in event:
                    src_ips.add(event['src_ip'])

    # Calculate the number of unique source IPs
    unique_src_ips_count = len(src_ips)

    # Return the analysis results
    return event_counts, unique_src_ips_count

# Example usage
file_path = 'd:/STUDY/CPT/FYP/Cowrie materials/cowrie log/log/cowrie_2024-04-08.json'
analysis_results = analyze_cowrie_log(file_path)
print(analysis_results)
