import re
import argparse  

def parse_logfile(file_path):
    # Define the pattern to get the advertiser device name
    advertiser_device_name = re.compile(r"\[DEVICE\]:\s*([\w:]+)\s*\(random\).*RSSI\s*(-?\d+)\s+(\S+)\s+C:")

    # Define the pattern to match lines with data length 5 and extract the RSSI value
    scan_pattern = re.compile(r"PER_ADV_SYNC\[\d+\]:.*RSSI\s*(-?\d+),.*data length (\d+),.*data:\s*([0-9a-fA-F]+)?")
    
    advertiser_device_name_found = False
    device_name = None 
    rssi_values = []
    with open(file_path, "r") as logfile:  
        for line in logfile:  
            # Extract the device name if not already found
            if not advertiser_device_name_found:
                match_device_name = advertiser_device_name.search(line)
                if match_device_name:
                    device_name = match_device_name.group(3)  # Extract device name
                    advertiser_device_name_found = True

            # Extract logs that contain valid data
            match_data = scan_pattern.search(line)  # Check if the line matches the pattern
            if match_data:
                data_length = int(match_data.group(2))  # Extract data length
                if data_length == 0:
                    continue  # Skip lines with data length 0

                rssi = int(match_data.group(1))  # Extract RSSI value
                data = match_data.group(3)  # Extract the data field if available
                rssi_values.append(rssi)

                #print(f"Matched line: {line.strip()}")
                print(f"Extracted RSSI: {rssi}, Data: {data}, Data Length: {data_length}")

    num_scans = len(rssi_values)
    average_rssi = sum(rssi_values) / num_scans if num_scans > 0 else 0
    return num_scans, average_rssi, device_name

def main():
    parser = argparse.ArgumentParser(description="Parse a receiver log file and calculate scan statistics (num of scans and average rssi).")
    parser.add_argument("logfile", help="Path to the log file", nargs='?', default="../sample_of_received_logs.txt")    
    args = parser.parse_args() 

    num_scans, average_rssi, device_name = parse_logfile(args.logfile)

    # Print fianl results
    print("\033[33m------------------- FINAL RESULTS -------------------\033[0m") 
    print(f"\033[32mAdvertiser device name: {device_name}\033[0m")  
    print(f"\033[32mNumber of scans:        {num_scans}\033[0m")          
    print(f"\033[32mAverage RSSI:           {average_rssi:.2f} dBm\033[0m") 
    print(f"\033[32mParsed file:            {args.logfile}\033[0m")     

if __name__ == "__main__":
    main()
