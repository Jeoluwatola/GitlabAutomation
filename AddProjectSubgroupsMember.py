#onboard user to specific projects

import subprocess
import json

API_token = 'glpat-4hsMcRGzussh9BxtZPRx'
user = "Binh Nguyen"
projects = ['PROJECT_NAME']
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
allmembers = json.loads('[]')
for i in range(1,5,1):
    getmembers = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/GROUP/members/?page={i}'
    page = curl(getmembers)
    a = json.loads(page)
    allmembers = allmembers + a 

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

#add user to subgroups
for i in subgroupids:
    subgroupname = next((item["name"] for item in allgroups if item["id"] == i), None)
    addUsertoSubgroup = f'curl -X POST -H "Authorization: Bearer {API_token}" -d "user_id={userid}&access_level={accesslevel}" https://gitlab.com/api/v4/groups/{i}/members'
    page = curl(addUsertoSubgroup)
    print(page)
    print(user + ' was added to ' + subgroupname)
