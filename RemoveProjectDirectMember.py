import subprocess
import json

API_token = 'TOKEN'
user = "USER"
projects = ['PROJECT1', 'PROJECT2']

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

#Get all projects in group
allprojects = json.loads('[]')
for i in range(1,8,1):
    getProjects = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/GROUP/projects/?page={i}'
    page = curl(getProjects)
    a = json.loads(page)
    allprojects = allprojects + a


#Get project ids of the specified projects
projectids = []
for i in projects:
    projectid = next((item["id"] for item in allprojects if item["name"] == i), None)
    projectids.append(projectid)

print(projectids)


#remove user from projects 
for i in projectids:
    projectname = next((item["name"] for item in allprojects if item["id"] == i), None)
    deleteuserfromproject = f'curl -X DELETE -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/projects/{i}/members/{userid}'
    page = curl(deleteuserfromproject)
    print(page)
    print("User deleted from " + projectname)


