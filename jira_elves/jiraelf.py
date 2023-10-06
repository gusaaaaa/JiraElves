import argparse
import sys
from dotenv import dotenv_values
from jira import JIRA
import re
import openai
import json
import textwrap

config = dotenv_values(".env")

jira_domain = config["JIRA_DOMAIN"]
if not jira_domain.startswith("https://"):
    jira_domain = "https://" + jira_domain
jira_user = config["JIRA_USER"]
jira_api_token = config["JIRA_TOKEN"]
jira_project = config["JIRA_PROJECT"]
openai_api_token = config["OPENAI_API_TOKEN"]

jira = JIRA(server=jira_domain, basic_auth=(jira_user, jira_api_token))
openai.api_key = openai_api_token

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
        new_line = expand_issue_in_line(line, jira_domain, jira_user, jira_api_token, format_markdown_line)
        new_lines.append(new_line)
        print(new_line, end='')  # Print the result to stdout

    with open("output.txt", "w") as f:
        f.writelines(new_lines)

def list_issues_in_release(release_number):
    issues = jira.search_issues(f'project = {jira_project} and fixversion = {release_number} and status = Done ORDER BY created DESC')

    for issue in issues:
        print(f'{jira_domain}/browse/{issue.key}')

def read_intentions():
    """
    The `read_intentions` function processes loosely structured input from stdin 
    to create and return a list of intentions.

    Input:
        The function expects the following format for input:

        - Each intention starts on a new line.
        - Additional details about the intention can be prefixed with a space, `-`, or `*`.
        - Multiple lines can be associated with an intention, but they must be
          immediately below the primary line of the intention and must start with
          one of the mentioned prefixes.

        Input Example:
            ```
            Permitir que TransferController maneje transfer_id de tipo arbitrario.
            remove API key from code.
              - currently the API key for accessing Google Analytics is hardcoded in main-app.js.
            ```

    Output:
        The function processes the input to group lines into single intentions.

        Output Example:
            ```
            [
                "Permitir que TransferController maneje transfer_id de tipo arbitrario.",
                "remove API key from code.\n  - currently the API key for accessing Google Analytics is hardcoded in main-app.js."
            ]
            ```

    Internal Working:
        1. Reads raw intentions from stdin and splits them into lines.
        4. Returns a list with intentions.
    """

    # Read from stdin and split lines
    raw_intentions = sys.stdin.readlines()

    # Process the lines to group intentions
    intention_list = []
    current_intention = ""
    for line in raw_intentions:
        if line.startswith(" ") or line.startswith("-") or line.startswith("*"):
            current_intention += "\n" + line.strip()
        else:
            if current_intention:
                intention_list.append(current_intention)
            current_intention = line.strip()
    if current_intention:  # Add the last intention if any
        intention_list.append(current_intention)

    return intention_list

def from_ticket_to_jira_issue_fields(ticket):
    formatted_description = textwrap.dedent(
        f"""Background

        {ticket['background']}

        User Story

        {ticket['user_story']}

        Goals

        {ticket['goals']}

        How to demo

        {ticket['how_to_demo']}

        Acceptance Criteria

        {ticket['acceptance_criteria']}
        """)

    fields = {
        'project': jira_project,
        'summary': ticket['summary'],
        'description': formatted_description,
        'issuetype': {'name': ticket['issue_type']}
    }

    return fields

def command_create_issues_from_intentions():
    intention_list = read_intentions()

    issue_field_list = []
    for intention_str in intention_list:
        ticket = intention_to_ticket(intention_str)
        if ticket is None:
            continue
        issue_field_list.append(from_ticket_to_jira_issue_fields(ticket))

    if issue_field_list:
        issues = jira.create_issues(field_list=issue_field_list)

        for issue in issues:
            issue_key = issue['issue'].key
            print(f"{jira_domain}/browse/{issue_key}")

def intention_to_ticket(intention_str):
    """
        The `intention_to_ticket` function processes an intention to create and return a ticket description.
        A ticket description is a dictionary that contains key elements, including background, goals, and acceptance criteria.

        Input Example:
            ```
            remove API key from code.
            - currently the API key for accessing Google Analytics is hardcoded in main-app.js.
            ```

        Output Example:
            ```
            {
                "issue_type": "Bug",
                "need": "Remove the hardcoded API key for accessing Google Analytics in main-app.js.",
                "context": "Currently, the API key for accessing Google Analytics is hardcoded in the main-app.js file.",
                "summary": "Remove the hardcoded API key for accessing Google Analytics in main-app.js",
                "background": "Hardcoding the API key for accessing Google Analytics in the main-app.js file poses a security risk, as anyone with access to the code can view the API key and potentially misuse it.",
                "user_story": "As a developer, I want to remove the hardcoded API key for accessing Google Analytics in main-app.js, so that the API key is not exposed and can be managed securely.",
                "goals": "The goal is to remove the hardcoded API key from the code and implement a more secure method for accessing Google Analytics.",
                "how_to_demo": "1. Open the main-app.js file\\n2. Remove the hardcoded API key from the code\\n3. Implement a secure method for accessing Google Analytics",
                "acceptance_criteria": "- The API key should not be present in the main-app.js file\\n- The application should still be able to access Google Analytics using a secure method"
            }

        Internal Working:
            1. Converts each intention into a JSON-formatted ticket description.
            2. Parses the JSON into a dictionary.
            3. Returns a ticket description.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "The AI company JiraElves has created the Caladriel assistant. Caladriel converts intentions expressed in natural language, into JSON-formatted ticket descriptions. In order to achive this goal, first Caladriel corrects grammar and/or translates intentions to English if needed; then infers an ISSUE_TYPE, a NEED, and a CONTEXT from the updated intention; finally Caladriel uses the inferred ISSUE_TYPE, NEED, and CONTEXT as a foundation to describe the ticket. Note: Issue types can be any of \"Task\" (default value, in case it can't be inferred from the intention), \"Bug\", \"Epic\".\n\nJiraElves' Assistant gets the input:\n\"\"\"\nintention = <<<\nPrecisamos agregar un timeout a la clase TransferController. Actualmente, si una respuesta nunca llega, el sequencer se queda bloqueado indefinidamente.\n>>>\n\"\"\"\n\nCaladriel's output:\n```\n{\n  \"issue_type\": \"Task\",\n  \"need\": \"Add a timeout to the TransferController class.\",\n  \"context\": \"Currently, if a response never arrives, the sequencer gets stuck indefinitely.\",\n  \"summary\": \"Allow TransferController to handle transfer_id of arbitrary type\",\n  \"background\": \"Currently, TransferController is only able to handle transfer_id that are integers. This is causing issues when the transfer_id is a string, or other type, and the controller is unable to properly handle the request.\",\n  \"user_story\": \"As a developer, I want to be able to use the TransferController to handle transfer_id of any type, so that I can make sure that all transfers are handled properly.\",\n  \"goals\": \"The goal is to make sure that TransferController is able to handle transfer_id of any type, including strings, integers, etc.\",\n  \"how_to_demo\": \"1. Create a transfer_id of a type other than integer\\n2. Use the TransferController to handle the request\\n3. Verify that the request is handled properly\",\n  \"acceptance_criteria\": \"- TransferController should be able to handle transfer_id of any data type\\n- All requests should be handled properly regardless of the data type of transfer_id\"\n}\n```"
            },
            {
            "role": "user",
            "content": "intention = <<<\nWrite CONTRIBUTE.md\n>>>"
            },
            {
            "role": "assistant",
            "content": "{\n  \"issue_type\": \"Task\",\n  \"need\": \"Write CONTRIBUTE.md file.\",\n  \"context\": \"\",\n  \"summary\": \"Create CONTRIBUTE.md file\",\n  \"background\": \"\",\n  \"user_story\": \"As a contributor, I want a CONTRIBUTE.md file in the project repository, so that I can have guidelines on how to contribute to the project.\",\n  \"goals\": \"The goal is to provide contributors with clear guidelines on how to contribute to the project.\",\n  \"how_to_demo\": \"\",\n  \"acceptance_criteria\": \"The CONTRIBUTE.md file should be added to the project repository and contain clear and comprehensive guidelines on how to contribute.\"\n}"
            },
            {
            "role": "user",
            "content": f"intention = <<<\n{intention_str}\n>>>"
            },
        ],
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_json = response['choices'][0]['message']['content']
    try:
        ticket = json.loads(response_json)
        return ticket
    except json.JSONDecodeError:
        print(f"Failed to decode JSON: {response_json}", file=sys.stderr)
        return None

def main():
    # Initialize the main parser
    parser = argparse.ArgumentParser(description='A collection of elves for Jira users.')
    subparsers = parser.add_subparsers(dest='command')

    # Define the 'expand' command
    expand_parser = subparsers.add_parser('expand', help='Expand issues.')

    # Define the 'list_release' command
    list_release_parser = subparsers.add_parser('list_release', help='List issues in the specified release.')
    list_release_parser.add_argument('RELEASE_NUMBER', type=str, help='Release number to list the issues for.')

    # Define the 'create_issues' command
    create_issues_parser = subparsers.add_parser('create_issues', help='Convert intentions into Jira tickets.')
    create_issues_parser.description = ('Convert a list of intentions into Jira tickets. '
                                       'Reads raw intentions from stdin, processes them, and creates a Jira issue containing '
                                       'a structured ticket description. Each intention starts on a new line. Additional details about '
                                       'the intention can be prefixed with a space, `-`, or `*`. Multiple lines can be associated with an '
                                       'intention, but they must be immediately below the primary line of the intention and must start with '
                                       'one of the mentioned prefixes.')

    args = parser.parse_args()

    if args.command == "expand":
        expand_issues()
    elif args.command == "list_release":
        list_issues_in_release(args.RELEASE_NUMBER)
    elif args.command == "create_issues":
        command_create_issues_from_intentions()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
