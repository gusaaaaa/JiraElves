import requests
import base64

def fetch_jira_issues(jql, domain, email, api_token, fields):
    url = f"https://{domain}/rest/api/3/search"

    auth_base64 = base64.b64encode(bytes(f"{email}:{api_token}", 'ascii')).decode('ascii')

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Accept": "application/json"
    }

    params = {
        "jql": jql,
        "fields": ",".join(fields),
        "maxResults": 100,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}: {response.text}")

    return response.json()["issues"]
