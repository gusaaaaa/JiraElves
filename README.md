# 🧝‍♂️ Jira Elves 🧝‍♀️

**A collection of helpers for Jira users.**

## Usage 🛠️

The `jiraelf` script is a versatile tool designed to help you facilitate your Jira tasks. Here's how to get started:

### Commands:

1. **Expand**: Convert Jira links within a text into descriptive markdown links based on the tickets' titles.

   ```bash
   jiraelf expand
   ```

2. **List Release**: Display a list of issues related to a specific release.

   ```bash
   jiraelf list_release=RELEASE_NUMBER
   ```

For more detailed help, run:

```bash
jiraelf -h
```

## Quick Start 🚀

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/gusaaaaa/JiraElves.git
   ```

2. **Navigate to the Directory**:

   ```bash
   cd JiraElves
   ```

3. **Setup your Environment**:

   Create a `.env` file in the directory where you plan to run the script, and populate it with the following:

   ```
   JIRA_DOMAIN=your_jira_domain
   JIRA_USER=your_email
   JIRA_TOKEN=your_api_token
   ```

   Ensure that the `.env` file is properly set up before running the script.

4. **Install and Run the Script**:

   With the project cloned and the environment variables set up, you can now run the script:

   ```bash
   jiraelf COMMAND
   ```

   Replace `COMMAND` with one of the commands detailed in the **Usage** section.

5. If you're using the `expand` command, watch as your input text transforms into an output filled with descriptive markdown links!

## Usage Example

**Use Case**: Effortlessly help clients map Jira tickets with project progress, making updates more informative and engaging.

### Input:

```
:mega: Update on our progress for the SpaceX Rocket App!

We're gearing up for the release of version 1.0.0 which includes the Falcon 9 simulator, the Dragon capsule guide, and the Starship launch scheduler.

* Falcon 9 Simulator:
    * Status: Almost done!
    * Related tickets:
        * https://spacexapp.atlassian.net/browse/SRX-123
        * https://spacexapp.atlassian.net/browse/SRX-124
* Dragon Capsule Guide:
    * Status: Ready for launch!
    * Related tickets:
        * https://spacexapp.atlassian.net/browse/SRX-125
        * https://spacexapp.atlassian.net/browse/SRX-126
* Starship Launch Scheduler:
    * Status: In progress.
    * Related tickets:
        * https://spacexapp.atlassian.net/browse/SRX-127
```

### Command:

```bash
jiraelf expand < input.txt > output.txt
```

### Output:

```
:mega: Update on our progress for the SpaceX Rocket App!

We're gearing up for the release of version 1.0.0 which includes the Falcon 9 simulator, the Dragon capsule guide, and the Starship launch scheduler.

* Falcon 9 Simulator:
    * Status: Almost done!
    * Related tickets:
        * Implement physics for Falcon 9 landing [#123](https://spacexapp.atlassian.net/browse/SRX-123)
        * Add Falcon 9 launch sound effects [#124](https://spacexapp.atlassian.net/browse/SRX-124)
* Dragon Capsule Guide:
    * Status: Ready for launch!
    * Related tickets:
        * Design interactive Dragon capsule tour [#125](https://spacexapp.atlassian.net/browse/SRX-125)
        * Write content for Dragon capsule history section [#126](https://spacexapp.atlassian.net/browse/SRX-126)
* Starship Launch Scheduler:
    * Status: In progress.
    * Related tickets:
        * Integrate Starship launch dates API [#127](https://spacexapp.atlassian.net/browse/SRX-127)
```

## Troubleshooting 🔍

### Mac Users: SSL or LibreSSL Warning

If you encounter a warning related to `urllib3` and SSL versions, such as:

```
urllib3 v2.0 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
```

This indicates that the version of SSL library your Python installation is using isn't compatible with some of the required packages.

#### Solution:

To resolve this issue on macOS, you can install OpenSSL 1.1.1 using Homebrew:

```bash
brew install openssl@1.1
```

This will ensure your Python environment uses a compatible version of OpenSSL as required by certain packages like `urllib3`.

**Note**: Make sure to restart the terminal after installing openssl.

## Contribute 🤝

Love what the elves are doing? Want to add more magic? We welcome contributions! Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License 📜

This project is licensed under the MIT License. See [LICENSE](LICENSE.txt) for details.
