# 🧩Project Structure and Instructions

📁 Folder: `ingescape_file`

This folder contains:

- the Ingescape agent project

- the folder `prova_2` with the agent’s entry point `main.py`, already generated and updated using `file_2.py`

📄 Files Overview:

`file.xml`
This is the XMI file exported directly from Cameo. It contains a state machine named `Traffic_light`

`file.py`
This is the first Python script. It reads the `file.xml`, extracts and interprets the structure of the state machine, and generates a .txt file describing its logic in plain text

`file_2.py`
This second script takes the .txt generated by `file.py`, parses the described logic, converts it into executable Python code using the transitions library, and embeds it directly into a working `main.py` file, ready to run as an Ingescape agent

🚀 Running the Agent in Ingescape by Python

To run the final `main.py`, it is strongly recommended to use `Python 3.9`, since newer versions may have compatibility issues with the Ingescape SDK

Use the following command in your terminal:

`py -3.9 "path_to_main.py" <agent_name> <network_interface_name> <port_number>`

Example:

`py -3.9 "C:\path\to\main.py" prova_2 Wi-Fi 5600`


📌 **Licensing**

This project is shared for reference purposes only. It is not open source.  
No license is granted for reuse, modification, or distribution.

