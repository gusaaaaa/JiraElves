from setuptools import setup, find_packages

setup(
    name="jira-elves",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'python-dotenv',
        'jira[cli]',
        'openai',
    ],
    entry_points={
      'console_scripts': [
        'jiraelf=jira_elves.jiraelf:main',
      ]
    }
)
