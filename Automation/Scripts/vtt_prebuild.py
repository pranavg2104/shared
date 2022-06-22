"""
    The python script for input verification and validation will perform the following task
        1. Check for the presence of the config file at given location.
        2. Check for the format of the config file at given location.
        3. Verify the variable name are in given format and not empty.
        4. Fetch the required data from the config file.
        5. Initialize the teamcity variable during runtime using teamcity service messages.
        6. Check for the presence of the input file required for this pipeline to run.
"""

import json
import os
import sys

# Check if config file is present on given location
if os.path.exists("Scripts\\vtt_config.json"):
    print("config file present at "+os.getcwd()+"\\vtt_config.json")
else:
    sys.exit("config file not present at "+os.getcwd()+"\\vtt_config.json")

# open the config file
json_ = open("Scripts\\vtt_config.json", "r")
path_details = {}
try:
    # check whether the json is in proper format
    path_details = json.load(json_)
except Exception as e:
    sys.exit("Json format is incorrect")
    # variable name so that user does not enter wrong variable details
data = ["dpa_file","dll_path","sln_path","additional_file","additional_files_path","microsar_sip_foler"]

res = [ele for ele in data if (ele in path_details and path_details[ele] or (ele == "additional_files_path" and isinstance(path_details[ele],list)))]
# check if all the variable are present if yes proceed further or raise the error
if len(res) == len(data):
    print("All variable are present in config file with respective data types")
else:
    print(res)
    print(path_details)
    sys.exit("Please check the var name or data type of a particular variable entered in config file")
    
    # fetch the details from config file
project_path = path_details.get("dpa_file")
folder = path_details.get("microsar_sip_foler")

# check if all input files are present at given location
if os.path.exists(project_path):
    print("Input file present "+os.getcwd()+"\\"+project_path)
else:
    sys.exit("Input file not present at "+os.getcwd()+"\\"+project_path)

if os.path.isdir(folder):
    print("Microsar sip folder present "+folder)
else:
    sys.exit("Microsar sip folder not present "+folder)

# list all the files present in directory of microsar sip
directory = []
present = 0
for path, subdirs, files in os.walk(folder):
    for name in files:
        directory.append(os.path.join(path, name))

for file in directory:
    if file.endswith(".c") or file.endswith(".h") or file.endswith(".cpp") or file.endswith(".arxml"):
        present = 1

if present:
    print("Files are present in microsar sip folder")
else:
    sys.exit("Files are not present microsar sip folder is empty")
