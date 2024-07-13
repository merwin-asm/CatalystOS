import requests
import hashlib
import time
import os
import subprocess

URL = 'https://raw.githubusercontent.com/merwin-asm/CatalystOS/main/src/current.py'  # Replace with the actual URL
CHECK_INTERVAL = 20  # Check every 60 seconds

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)

def calculate_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def run_script(filename):
    return subprocess.Popen(['python', filename])

def stop_script(process):
    if process:
        process.terminate()
        process.wait()

def main():
    current_hash = None
    process = None

    while True:
        try:
            # Fetch the data from the URL
            data = fetch_data(URL)
            
            # Calculate the hash of the fetched data
            new_hash = calculate_hash(data)
            
            # Check if the data has changed
            if new_hash != current_hash:
                print("Data has changed, updating and running the new script.")
                
                # Save the new data to current.py
                save_to_file(data, 'current.py')
                
                # Stop the currently running script if it exists
                stop_script(process)
                
                # Run the new script
                process = run_script('current.py')
                
                # Update the current hash
                current_hash = new_hash
            else:
                print("No change detected.")
        except Exception as e:
            print(f"Error: {e}")

        # Wait for the next check
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
