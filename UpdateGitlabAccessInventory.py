import csv
import requests


serial = 1
headers_csv = ["S/N", "Project", "Maintainers","Developers","Reporters"]
API_token = 'API_TOKEN'
local_path = "LOCAL_PATH"
BASE_URL = "https://gitlab.com/api/v4"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_token}"
}


#Get projects
allprojects = []
page = 1
while True:
        resp = requests.get(f"{BASE_URL}/groups/GROUPNAME/projects", headers=headers, params={"page": page})

        if resp.status_code != 200:
            print(f"Error fetching projects: {resp.status_code} - {resp.text}")
            break

        data = resp.json()
        if not data:
            break

        allprojects.extend(data)
        page += 1

sorted_projects = sorted(allprojects, key=lambda x: x['name'].lower())          #sort projects alphabetically

projectids = [item['id'] for item in sorted_projects]           #Retrieve all project ids

with open(local_path, mode="w", newline="") as file:            #create file on local
    writer = csv.writer(file)
    writer.writerow(headers_csv)  # Write headers   
    for i in projectids:
        resp = requests.get(f"{BASE_URL}/projects/{i}/members/all", headers=headers)
        page_json = resp.json()

        projectname = next((item["name"] for item in allprojects if item["id"] == i), None)
        reporters_list = [item["name"] for item in page_json if item["access_level"] == 20]
        developers_list = [item["name"] for item in page_json if item["access_level"] == 30]
        maintainers_list = [item["name"] for item in page_json if item["access_level"] == 40]

        #sort the names alphabetically
        reporters_list.sort()
        developers_list.sort()
        maintainers_list.sort()

        #Remove square brackets from list
        reporters_str = ', '.join(str(x) for x in reporters_list)
        developers_str = ', '.join(str(x) for x in developers_list)
        maintainers_str = ', '.join(str(x) for x in maintainers_list)

        data = [
        [serial,projectname,maintainers_str,developers_str,reporters_str]
        ]
        writer.writerows(data)    # Write all data rows
        serial = serial + 1       #For serial number column