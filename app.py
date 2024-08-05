import streamlit as st
from datetime import datetime

def parse_log_file(file, init_time, end_time, target_host):
    connections = []
    target_connections = 0

    init_timestamp = datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S').timestamp()
    end_timestamp = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').timestamp()

    with open(file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 3:
                continue

            timestamp, host1, host2 = parts
            try:
                log_timestamp = int(timestamp) / 1000  # Convert milliseconds to seconds
            except ValueError:
                continue  # Skip lines with invalid timestamps

            if init_timestamp <= log_timestamp <= end_timestamp:
                if host1 == target_host or host2 == target_host:
                    target_connections += 1
                    if host1 == target_host:
                        connections.append(host2)
                    elif host2 == target_host:
                        connections.append(host1)

    return connections

# Streamlit app
st.set_page_config(page_title="Log Parser", page_icon="🔍")

# Sidebar content
with st.sidebar:
    # Display Clarity AI logo
    st.image("clarity_ai_logo.png", use_column_width=True)

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

    # Input: Target Host
    target_host = st.text_input('Enter target hostname')

    # Button to Parse Log File
    parse_button = st.button('Parse Log')

# Main content area
st.title('Log File Parser')

# App Description in the Main Area
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

# Display the results
if parse_button and valid_times:
    if start_datetime and end_datetime and target_host:
        result = parse_log_file('input-file-10000__1_.txt', start_datetime, end_datetime, target_host)
        
        if result:
            st.markdown(f"### Found {len(result)} connections involving `{target_host}`")
            st.markdown(f"**Hosts connected to `{target_host}` between `{start_datetime}` and `{end_datetime}`:**")
            st.markdown("\n".join([f"- {host}" for host in result]))
        else:
            st.markdown(f"No connections found for `{target_host}` between `{start_datetime}` and `{end_datetime}`.")
    else:
        st.error("Please enter all required inputs.")
