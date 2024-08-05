import streamlit as st
from datetime import datetime

def parse_log_file(file, init_time, end_time, target_host):
    """
    Parses the provided log file and finds connections to the target host within the given time range.

    Args:
        file (str): Path to the log file.
        init_time (str): Initial time in 'YYYY-MM-DD HH:MM:SS' format.
        end_time (str): End time in 'YYYY-MM-DD HH:MM:SS' format.
        target_host (str): Target hostname to filter connections.

    Returns:
        list: List of hostnames connected to the target host.
    """
    connections = []

    # Convert init_time and end_time to timestamps for easy comparison
    init_timestamp = datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S').timestamp()
    end_timestamp = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').timestamp()

    # Store log entries in a list to sort them
    log_entries = []

    # Open and read the log file
    with open(file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 3:
                continue  # Skip lines without the required structure

            timestamp, host1, host2 = parts
            try:
                log_timestamp = int(timestamp) / 1000  # Convert milliseconds to seconds
                log_entries.append((log_timestamp, host1, host2))
            except ValueError:
                continue  # Skip lines with invalid timestamps

    # Sort log entries by timestamp
    log_entries.sort(key=lambda entry: entry[0])

    # Filter log entries based on time range and target host
    for log_timestamp, host1, host2 in log_entries:
        if init_timestamp <= log_timestamp <= end_timestamp:
            if host1 == target_host or host2 == target_host:
                if host1 == target_host:
                    connections.append(host2)
                elif host2 == target_host:
                    connections.append(host1)

    return connections

def extract_hostnames_from_log(file):
    """
    Extracts all unique hostnames from the log file.

    Args:
        file (str): Path to the log file.

    Returns:
        list: A sorted list of unique hostnames found in the log file.
    """
    hostnames = set() 

    with open(file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                _, host1, host2 = parts
                hostnames.add(host1)
                hostnames.add(host2)

    return sorted(hostnames) 

# Streamlit app configuration
st.set_page_config(page_title="Log Parser", page_icon="🔍")

# Load the hostnames from the log file
hostnames = extract_hostnames_from_log('input-file-10000__1_.txt')

# Sidebar content
with st.sidebar:
    st.image("clarity_ai_logo.png", use_column_width=True)  # Display Clarity AI logo

    # Input: Start and End Date
    start_date = st.date_input('Start date')
    end_date = st.date_input('End date')

    # Input: Start and End Time with Seconds
    start_time = st.text_input('Start time (HH:MM:SS)', '00:00:00')
    end_time = st.text_input('End time (HH:MM:SS)', '23:59:59')

    # Validate time format
    try:
        start_time = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time, '%H:%M:%S').time()
        valid_times = True
    except ValueError:
        valid_times = False
        st.error('Please enter a valid time in HH:MM:SS format.')

    # Combine date and time inputs
    start_datetime = f"{start_date} {start_time}"
    end_datetime = f"{end_date} {end_time}"

    # Input: Target Host using a selectbox with autocomplete
    target_host = st.selectbox('Select or type the target hostname', hostnames)

    # Button to Parse Log File
    parse_button = st.button('Parse Log')

# Main content area
st.title('Log File Parser')

st.write("""
## Welcome to the Clarity AI Log File Parser

This application allows you to parse log files and filter connections involving a specific host within a given time range.

**How it works:**

1. Use the sidebar to select a start and end date, as well as times.
2. Enter the target hostname you're interested in.
3. The app will scan the log file and display all the hosts that connected with the target host during the specified time period.

This tool is designed to help you analyze network logs efficiently and effectively.

**Note:** Make sure that the log file is properly formatted and placed in the same directory as this app.
""")

# Show results when the parse button is clicked and times are valid
if parse_button and valid_times:
    if start_datetime and end_datetime and target_host:
        # Parse the log file and get results
        result = parse_log_file('input-file-10000__1_.txt', start_datetime, end_datetime, target_host)
        
        if result:
            st.markdown(f"### Found {len(result)} connections involving `{target_host}`")
            st.markdown(f"**Hosts connected to `{target_host}` between `{start_datetime}` and `{end_datetime}`:**")
            st.markdown("\n".join([f"- {host}" for host in result]))
        else:
            st.markdown(f"No connections found for `{target_host}` between `{start_datetime}` and `{end_datetime}`.")
