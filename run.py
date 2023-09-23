import requests
import re
import base64
from dotenv import dotenv_values

config = dotenv_values(".env")

def get_jira_title(domain, email, api_token, issue_key):
    url = f"https://{domain}/rest/api/3/issue/{issue_key}"

    auth_base64 = base64.b64encode(bytes(f"{email}:{api_token}", 'ascii')).decode('ascii')

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve {issue_key}: {response.text}")
        return None

    return response.json()["fields"]["summary"]

def main():
    jira_domain = config["JIRA_DOMAIN"]
    email = config["JIRA_USER"]
    api_token = config["JIRA_TOKEN"]

    with open("input.txt", "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        match = re.search(r"https://[\w.-]+/browse/(\w+-\d+)", line)
        if match:
            issue_key = match.group(1)
            issue_number = issue_key.split('-')[1]  # Split by hyphen and take the second part
            title = get_jira_title(jira_domain, email, api_token, issue_key)
            if title:
                markdown_link = f"{title} [#{issue_number}](https://{jira_domain}/browse/{issue_key})"
                line = line.replace(match.group(0), markdown_link)
        new_lines.append(line)
        print(line, end='')  # Print the result to stdout

    with open("output.txt", "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    main()
