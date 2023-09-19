import requests
import re

def get_jira_title(domain, email, api_token, issue_key):
    url = f"https://{domain}/rest/api/2/issue/{issue_key}"
    headers = {
        "Authorization": f"Basic {email}:{api_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve {issue_key}: {response.text}")
        return None

    return response.json()["fields"]["summary"]

def main():
    jira_domain = "focusuy.atlassian.net"
    email = "gus@focus.com"
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
                markdown_link = f"[{issue_key}: {title}](https://{jira_domain}/browse/{issue_key})"
                line = line.replace(match.group(0), markdown_link)
        new_lines.append(line)

    with open("output_file.md", "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    main()
