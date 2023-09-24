# 🧝‍♂️ Jira Elves 🧝‍♀️

**A collection of helpers for Jira users**

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
python run.py
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

## Quick Start 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/jira_elves.git
   ```

2. Navigate to the directory:
   ```bash
   cd jira_elves
   ```

3. Set up your `.env` file with the following:
   ```
   JIRA_DOMAIN=your_jira_domain
   JIRA_USER=your_email
   JIRA_TOKEN=your_api_token
   ```

4. Run the magic:
   ```bash
   python run.py
   ```

5. Watch as your `input.txt` transforms into an `output.txt` filled with descriptive markdown links!

## Contribute 🤝

Love what the elves are doing? Want to add more magic? We welcome contributions! Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License 📜

This project is licensed under the MIT License. See [LICENSE](LICENSE.txt) for details.
