#offboard user from specific projects

import subprocess
import pandas as pd
import json

API_token = 'TOKEN'
user = "USER"
projects = ['PROJECT']
accesslevel = '30' #30 for developer 40 for maintainer

#curl function
def curl(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return stdout
    else:
        return stderr

#Get memebers of group
getmembers = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/GROUP/members/?per_page=150'
page = curl(getmembers)
allmembers = json.loads(page)

#Retrieve id for a particular user
userid = next((item["id"] for item in allmembers if item["name"] == user), None)

print(userid)

#Get subgroups
allgroups = json.loads('[]')
for i in range(1,8,1):
    getSubgroups = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/GROUP/subgroups/?page={i}'
    page = curl(getSubgroups)
    a = json.loads(page)
    allgroups = allgroups + a

#Get subgroupids of the subgroup for all specified projects
subgroupids = []
for i in projects:
    j = i + "_Subgroup"
    print(j)
    subgroupid = next((item["id"] for item in allgroups if item["name"] == j), None)
    subgroupids.append(subgroupid)

print(subgroupids)

#remove user from subgroups 
for i in subgroupids:
    subgroupname = next((item["name"] for item in allgroups if item["id"] == i), None)
    deleteuserfromgroup = f'curl -X DELETE -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/{i}/members/{userid}'
    page = curl(deleteuserfromgroup)
    print(page)
    print("User deleted from " + subgroupname)
