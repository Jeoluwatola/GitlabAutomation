import subprocess
import json

API_token = 'TOKEN'
user = "USERNAME"

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
print (userid)


#Get subgroups
allgroups = json.loads('[]')
for i in range(1,8,1):
    getMembers = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/GROUP/subgroups/?page={i}'
    page = curl(getMembers)
    a = json.loads(page)
    allgroups = allgroups + a


#Retrieve all subgroup ids
groupids = [item['id'] for item in allgroups]


#get members of each subgroup then check for the presense of the user and put the group ids in a list
usergroupids = [ ]
for i in groupids:
    getGroupMembers = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/{i}/members'
    page = curl(getGroupMembers)
    page = json.loads(page)
    userpresent = any(item['name'] == user for item in page)
    if userpresent == True:
        usergroupids.append(i)
    else:
        continue
    
#get the name of the groups where the user is found
usergroupnames = []
for i in usergroupids:
    usergroupname = next((item["name"] for item in allgroups if item["id"] == i), None)
    usergroupnames.append(usergroupname)
    print("User exists in " + usergroupname)