import subprocess
import json
import pandas as pd



API_token = 'TOKEN'


#curl function
def curl(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return stdout
    else:
        return stderr

#to table function Formats JSON data into a table using pandas.
def json_to_table(json_data):
    try:
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        df = pd.DataFrame(data)
        sorted_df = df.sort_values(by='name')
        return sorted_df
    except Exception as e:
        print(f"Error: {e}")
        return None

pd.set_option('display.max_rows', None)    # Show all rows
pd.set_option('display.max_columns', None) # Show all columns
pd.set_option('display.width', None)       # Disable line wrapping
pd.set_option('display.max_colwidth', None)# Show full column contents


#Get memebers of group
getmembers = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/GROUP/members/?per_page=150'
page = curl(getmembers)
allmembers = json.loads(page)

groupmembers = json_to_table(allmembers)

with open("GroupMembers.txt", "w") as file:
  print(groupmembers, file=file)