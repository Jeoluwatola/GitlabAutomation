import subprocess
import json

GROUPID = 'GROUP_ID'
API_token = 'TOKEN'
projectname = 'Test-Project3'
developers = ['Developer1', 'Developer2']
maintainers = ['Maintainer1', 'JMaintainer2']
subgroups = []

#curl function
def curl(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return stdout
    else:
        return stderr


#create project
createproject = f'curl -X POST  -H "Authorization: Bearer {API_token}" -d "name={projectname}&namespace_id={GROUPID}&initialize_with_readme=true&default_branch=staging" --url "https://gitlab.com/api/v4/projects/"'
page = curl(createproject)
print(page)
data = json.loads(page)
projectid = data.get("id", [])
print(projectid)
print(f'{projectname} was created with id {projectid}')

#add approval rule
addapprovalrule = f'curl -X POST  -H "Authorization: Bearer {API_token}" -d "name=approval&approvals_required=1&applies_to_all_protected_branches=true&rule_type=any_approver" --url "https://gitlab.com/api/v4/projects/{projectid}/approval_rules"'
page = curl(addapprovalrule)
print(page)

#create main branch
createbranch = f'curl -X POST  -H "Authorization: Bearer {API_token}" -d "branch=main&ref=staging" --url "https://gitlab.com/api/v4/projects/{projectid}/repository/branches"'
page = curl(createbranch)
print(page)
print('Main branch created')


#protect main branch
protectbranch = f'curl -X POST  -H "Authorization: Bearer {API_token}" -d "name=main" --url "https://gitlab.com/api/v4/projects/{projectid}/protected_branches"'
page = curl(protectbranch)
print(page)
print('Main branch protected')


#create subgroup
subgroupname = f'{projectname}_Subgroup'
subgrouppath = f'{subgroupname}'
createsubgroup = f'curl -X POST -H "Authorization: Bearer {API_token}" -d "path={subgrouppath}&name={subgroupname}&parent_id={GROUPID}" --url "https://gitlab.com/api/v4/groups/"'
page = curl(createsubgroup)
data = json.loads(page)
print (page)
subgroupid = data.get("id", [])
print(f'{subgroupname} was created with id {subgroupid}')

#Get userids of default maintainers of Subgroup
getSubgroupmembers = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/{subgroupid}/members/all'
page = curl(getSubgroupmembers)
subgroupmembers = json.loads(page)
print(subgroupmembers)
userids = [item["id"] for item in subgroupmembers if item["access_level"] == 40]
print(userids)

#Make default maintainers owners of subgroup
for i in userids:
    username = next((item["name"] for item in subgroupmembers if item["id"] == i), None)
    addUsertoSubgroup = f'curl -X POST -H "Authorization: Bearer {API_token}" -d "user_id={i}&access_level=50" https://gitlab.com/api/v4/groups/{subgroupid}/members/'
    page = curl(addUsertoSubgroup)
    print (page)
    print (username + " is now an owner of the Subgroup")

#add subgroup to project
addSubgrouptoProject = f'curl -X POST -H "Authorization: Bearer {API_token}" -d "group_id={subgroupid}&group_access=40" https://gitlab.com/api/v4/projects/{projectid}/share'
page = curl(addSubgrouptoProject)
print (page)
print ("Project has been shared with the subgroup")


#Get memebers of group
allmembers = json.loads('[]')
for i in range(1,5,1):
    getmembers = f'curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {API_token}" https://gitlab.com/api/v4/groups/GROUP/members/?page={i}'
    page = curl(getmembers)
    a = json.loads(page)
    allmembers = allmembers + a 

#Retrieve userids for developers
developerids = []
for i in developers:
    userid = next((item["id"] for item in allmembers if item["name"] == i), None)
    developerids.append(userid)
print(developerids)

#Retrieve userids for maintainers 
maintainerids = []
for i in maintainers:
    userid = next((item["id"] for item in allmembers if item["name"] == i), None)
    maintainerids.append(userid)
print(maintainerids)


#add users to subgroup
for i in developerids:
    username = next((item["name"] for item in allmembers if item["id"] == i), None)
    addUsertoSubgroup = f'curl -X POST -H "Authorization: Bearer {API_token}" -d "user_id={i}&access_level=30" https://gitlab.com/api/v4/groups/{subgroupid}/members'
    page = curl(addUsertoSubgroup)
    print(page)
    print(username + ' was added as a Developer')

for i in maintainerids:
    username = next((item["name"] for item in allmembers if item["id"] == i), None)
    addUsertoSubgroup = f'curl -X POST -H "Authorization: Bearer {API_token}" -d "user_id={i}&access_level=40" https://gitlab.com/api/v4/groups/{subgroupid}/members'
    page = curl(addUsertoSubgroup)
    print(page)
    print(username + ' was added as a Maintainer')
    
