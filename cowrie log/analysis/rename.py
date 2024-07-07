import os

def rename_files(directory):
    # Navigate to the specified directory
    os.chdir(directory)
    
    # List all files in the directory
    files = os.listdir()

    # Loop through each file
    for file in files:
        # Check if the file follows the specific pattern
        if file.startswith("cowrie.json."):
            # Split the file name at 'json.'
            parts = file.split("json.")
            # Reformat the file name
            new_name = f"cowrie_{parts[1]}.json"
            # Rename the file
            os.rename(file, new_name)
            print(f"Renamed '{file}' to '{new_name}'")

# Example usage
directory_path = 'D:\\STUDY\\CPT\\FYP\\Cowrie materials\\cowrie log\\log\\rename'  # Change this to your directory
rename_files(directory_path)
