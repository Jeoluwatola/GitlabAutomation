import subprocess
import json
import requests

ORGAdminID = 'ID'
projectname = 'ORG-ops-starter'
developers = []
maintainers = []
allowed_to_merge =[]
GITLAB_API_TOKEN = 'TOKEN'
BASE_URL = "https://gitlab.com/api/v4"

get_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GITLAB_API_TOKEN}"
}

post_headers = {
    "Authorization": f"Bearer {GITLAB_API_TOKEN}"
}


#create project
createproject_params = {
    "name" : projectname,
    "namespace_id" : ORGAdminID,
    "initialize_with_readme" : "true",
    "default_branch" : "staging"
}
resp = requests.post(f"{BASE_URL}/projects/", headers=post_headers, params=createproject_params)
data = resp.json()
print(data)
projectid = data.get("id", [])
print(projectid)
print(f'{projectname} was created with id {projectid}')



#add approval rule
addapprovalrule_params = {
    "name" : 'approval',
    "approvals_required" : '1',
    "applies_to_all_protected_branches" : "true"
}
resp = requests.post(f"{BASE_URL}/projects/{projectid}/approval_rules", headers=post_headers, params=addapprovalrule_params)
data = resp.json()
print(data)



#create main branch
createbranch_params = {
    "branch" : "main",
    "ref" : "staging",
    "applies_to_all_protected_branches" : "true"
}
resp = requests.post(f"{BASE_URL}/projects/{projectid}/repository/branches", headers=post_headers, params=createbranch_params)
data = resp.json()
print(data)
print('Main branch created')



#create subgroup
subgroupname = f'{projectname}_Subgroup'
subgrouppath = f'{subgroupname}'
createsubgroup_params = {
    "path" : f'{subgrouppath}',
    "name" : f'{subgroupname}',
    "parent_id" : f"{ORGAdminID}"
}
resp = requests.post(f"{BASE_URL}/groups/", headers=post_headers, params=createsubgroup_params)
data = resp.json()
print(data)
subgroupid = data.get("id", [])
print(f'{subgroupname} was created with id {subgroupid}')



#add subgroup to project
addsubgroup_params = {
    "group_id" : f"{subgroupid}",
    "group_access" : "40"
}
resp = requests.post(f"{BASE_URL}/projects/{projectid}/share", headers=post_headers, params=addsubgroup_params)
data = resp.json()
print(data)
print ("Project has been shared with the subgroup")


#add devops to project
adddevops_params = {
    "group_id" : "id",
    "group_access" : "40"
}
resp = requests.post(f"{BASE_URL}/projects/{projectid}/share", headers=post_headers, params=adddevops_params)
data = resp.json()
print(data)
print ("Project has been shared with the Devops Team")


#Get members of ORGAdmin group
def get_all_members():
    all_members = []
    page = 1
    while True:
        resp = requests.get(f"{BASE_URL}/groups/ORGAdmin/members", headers=get_headers, params={"page": page})

        if resp.status_code != 200:
            print(f"Error fetching members: {resp.status_code} - {resp.text}")
            break

        data = resp.json()
        if not data:
            break

        all_members.extend(data)
        page += 1

    return sorted(all_members, key=lambda x: x['name'].lower())

allmembers = get_all_members()

#Retrieve userids for developers
developerids = []
for i in developers:
    userid = next((item["id"] for item in allmembers if item["name"] == i), None)
    developerids.append(userid)

#Retrieve userids for maintainers 
maintainerids = []
for i in maintainers:
    userid = next((item["id"] for item in allmembers if item["name"] == i), None)
    maintainerids.append(userid)

#Retrieve userids for those allowed to merge
allowed_to_mergeids = []
for i in allowed_to_merge:
    userid = next((item["id"] for item in allmembers if item["name"] == i), None)
    allowed_to_mergeids.append(userid)


#add users to subgroup
for i in developerids:
    adduser_params = {
    "user_id" : f"{i}",
    "access_level" : "30"
    }
    username = next((item["name"] for item in allmembers if item["id"] == i), None)
    resp = requests.post(f"{BASE_URL}/groups/{subgroupid}/members", headers=post_headers, params=adduser_params)
    data = resp.json()
    print(data)
    print(username + ' was added as a Developer')

for i in maintainerids:
    adduser_params = {
    "user_id" : f"{i}",
    "access_level" : "40"
    }
    username = next((item["name"] for item in allmembers if item["id"] == i), None)
    resp = requests.post(f"{BASE_URL}/groups/{subgroupid}/members", headers=post_headers, params=adduser_params)
    data = resp.json()
    print(data)
    print(username + ' was added as a Maintainer')
    


#protect main branch
protectbranch_params = {
    "name" : "main",
    "push_access_level" : "40",
    "merge_access_level" : "40"
    }
resp = requests.post(f"{BASE_URL}/projects/{projectid}/protected_branches", headers=post_headers, params=protectbranch_params)
data = resp.json()
print(data)
print('Main branch protected')



#Allow merge rights on staging branch
for i in allowed_to_mergeids:
    allowmerge_params = {
        "allowed_to_merge%5B%5D%5Buser_id%5D" : f"{i}",
        "allowed_to_push%5B%5D%5Buser_id%5D" : f"{i}"
        }
    username = next((item["name"] for item in allmembers if item["id"] == i), None)
    resp = requests.patch(f"{BASE_URL}/projects/{projectid}/protected_branches/staging", headers=post_headers, params=allowmerge_params)
    data = resp.json()
    print(data)
    print(username + ' was granted access to merge on staging')



#Allow merge rights on main branch
for i in allowed_to_mergeids:
    allowmerge_params = {
        "allowed_to_merge%5B%5D%5Buser_id%5D" : f"{i}",
        "allowed_to_push%5B%5D%5Buser_id%5D" : f"{i}"
        }
    username = next((item["name"] for item in allmembers if item["id"] == i), None)
    resp = requests.patch(f"{BASE_URL}/projects/{projectid}/protected_branches/main", headers=post_headers, params=allowmerge_params)
    data = resp.json()
    print(data)
    print(username + ' was granted access to merge on main')