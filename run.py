from jira_elves import expand_issue_in_line
from dotenv import dotenv_values

config = dotenv_values(".env")

with open("input.txt", "r") as f:
    content = f.read()

def main():
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

if __name__ == "__main__":
    main()
