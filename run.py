import requests
import re
import base64

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
    jira_domain = "focusuy.atlassian.net"
    email = "gus@focus.uy"
    api_token = "ATATT3xFfGF0ppxAXnUEsiLHFA4InbxbIlicuoMD-uK3UEcwHjzkjEM2AaDV5t8vfiSE8d-nhh0McEtvEfp0EiqvZ7NArkUWcPQ7izz9kZk67SEptdNfWefepMDQnxhF6HUcPcGfTIZ2y8HwYE5iKsH8cvFcKSFEn0eLalNkaNXdLISkYp33_nI=EB1448BE"

    with open("input_file.txt", "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        match = re.search(r"https://[\w.-]+/browse/(\w+-\d+)", line)
        if match:
            issue_key = match.group(1)
            title = get_jira_title(jira_domain, email, api_token, issue_key)
            if title:
                markdown_link = f"{title} [{issue_key}](https://{jira_domain}/browse/{issue_key})"
                line = line.replace(match.group(0), markdown_link)
        new_lines.append(line)

    with open("output_file.md", "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    main()
