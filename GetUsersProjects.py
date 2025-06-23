import subprocess
import json
import sys

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

print(userid)


#Get projects
allprojects = json.loads('[]')
for i in range(1,8,1):
    getProjects = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/GROUP/projects/?page={i}'
    page = curl(getProjects)
    a = json.loads(page)
    allprojects = allprojects + a

#Retrieve all project ids
projectids = [item['id'] for item in allprojects]


#get members of each project then check for the presense of the user and put the project ids in a list
userprojectids = [ ]
for i in projectids:
    getProjectMembers = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/projects/{i}/members'
    page = curl(getProjectMembers)
    page = json.loads(page)
    userpresent = any(item['name'] == user for item in page)
    if userpresent == True:
        userprojectids.append(i)
    else:
        continue

print(userprojectids)

if userprojectids == '[]':
    print("User is not a direct member of any project")
    sys.exit(1)


#get the name of the projects where the user is found
projectnames = []
for i in userprojectids:
    projectname = next((item["name"] for item in allprojects if item["id"] == i), None)
    projectnames.append(projectname)

print(projectnames)


