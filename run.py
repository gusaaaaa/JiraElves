import argparse
import sys
from dotenv import dotenv_values
from jira import JIRA
import re

config = dotenv_values(".env")

jira_domain = config["JIRA_DOMAIN"]
email = config["JIRA_USER"]
api_token = config["JIRA_TOKEN"]

jira = JIRA(server=jira_domain, basic_auth=(email, api_token))

def expand_issues():
    # Reading lines from stdin
    lines = sys.stdin.readlines()

    def format_markdown_line(line, match_string, issue):
        issue_number = issue.key.split('-')[1]  # Split by hyphen and take the second part
        issue_status = issue.fields.status.name
        markdown_link = f"{issue.fields.summary} [#{issue_number}]({match_string}) - {issue_status}"
        return line.replace(match_string, markdown_link)

    def expand_issue_in_line(line, domain, email, api_token, callback):
        match = re.search(r"https://[\w.-]+/browse/(\w+-\d+)", line)
        if match:
            issue_key = match.group(1)
            issue_data = jira.issue(issue_key)
            if issue_data:
                line = callback(line, match.group(0), issue_data)
        return line

    new_lines = []
    for line in lines:
        new_line = expand_issue_in_line(line, jira_domain, email, api_token, format_markdown_line)
        new_lines.append(new_line)
        print(new_line, end='')  # Print the result to stdout

    with open("output.txt", "w") as f:
        f.writelines(new_lines)

def list_issues_in_release(release_number):
    issues = jira.search_issues(f'project = "BMC2" and fixversion = {release_number} and status = Done ORDER BY created DESC')

    for issue in issues:
        print(f'https://{jira_domain}/browse/{issue.key}')

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
