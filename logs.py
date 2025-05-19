import csv
from datetime import datetime

def save_log(entries):
    # Using a timestamped filename to avoid overwriting files
    filename = f"blast_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Open the file and write the log entries
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Phone", "Status", "Time"])
        
        # Write the header (column names)
        writer.writeheader()
        
        # Write the log entries
        writer.writerows(entries)
