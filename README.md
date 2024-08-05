# Clarity AI

## Log File Parser

This project is a Python script to parse log files and find connections to a specified hostname within a given time range.

### Description

The script reads a log file, filters the entries based on a specified time range, and lists the hostnames that have connected to a given target hostname within that period. The script takes the log file path, start time, end time, and target hostname as inputs from the user. 

### Prerequisites

- Python version 3

### Installation

1. Clone the repository or download the script.
2. Navigate to the project directory.
3. Install the required dependencies using pip:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

This project is powered by Streamlit, allowing for an intuitive and interactive web application to parse and analyze log files.

### Running the Application

1. **Start the Streamlit App**: Run the following command to launch the Streamlit web app:
    ```sh
    streamlit run app.py
    ```

2. **Access the App**: Open your web browser and navigate to the local URL provided by Streamlit (typically `http://localhost:8501`).

3. **Using the App**:
    - Use the sidebar to:
        - Select a start and end date.
        - Enter the start and end times.
        - Enter the target hostname you are interested in.
    - Click the 'Parse Log' button to parse the log file and display the results.

### Running the Application
You can also access the tool online using the following link:

https://clarityai-logs.streamlit.app

This will take you directly to the Streamlit app where you can interact with the log parser without needing to run it locally.

### Example

```sh
Enter the start time (YYYY-MM-DD HH:MM:SS): 2023-01-01 00:00:00
Enter the end time (YYYY-MM-DD HH:MM:SS): 2023-01-01 03:00:00
Enter the target hostname: Aadvik

Found 2 connections involving Aadvik
Hosts connected to Aadvik between 2023-01-01 00:00:00 and 2023-01-01 03:00:00:
- Keimy
- Tyreonna

