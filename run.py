import argparse
from jira_elves import expand_issue_in_line, fetch_jira_issues
from dotenv import dotenv_values

config = dotenv_values(".env")

def expand_issues():
    jira_domain = config["JIRA_DOMAIN"]
    email = config["JIRA_USER"]
    api_token = config["JIRA_TOKEN"]

    with open("input.txt", "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        new_line = expand_issue_in_line(line, jira_domain, email, api_token)
        new_lines.append(new_line)
        print(new_line, end='')  # Print the result to stdout

    with open("output.txt", "w") as f:
        f.writelines(new_lines)

def list_issues_in_release(release_number):
    jira_domain = config["JIRA_DOMAIN"]
    email = config["JIRA_USER"]
    api_token = config["JIRA_TOKEN"]

    JQL_QUERY = f'project = "BMC2" and fixversion = {release_number} and status = Done ORDER BY created DESC'

    issues = fetch_jira_issues(JQL_QUERY, jira_domain, email, api_token, ["key", "summary", "components"])
    for issue in issues:
        print(issue["key"], "-", issue["fields"]["summary"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JIRA tasks.')
    parser.add_argument('command', type=str, help='Use "expand" to expand issues or "list_release=RELEASE_NUMBER" to list issues in release.')

    args = parser.parse_args()

    # Split the command argument at '='
    action, _, value = args.command.partition('=')

    if action == "expand" and not value:
        expand_issues()
    elif action == "list_release" and value:
        list_issues_in_release(value)
    else:
        print("Invalid command. Use 'expand' or 'list_release=RELEASE_NUMBER'.")
