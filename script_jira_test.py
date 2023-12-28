from __future__ import annotations

from jira import JIRA

if __name__ == '__main__':

    with open("API.token", "r") as reader:
        API_TOKEN = reader.read().strip()

    jira = JIRA(
        server="https://neurocat.atlassian.net",
        basic_auth=('adrian.mindak@neurocat.ai', API_TOKEN),
    )

    # aidkit_project = jira.project(id="AK")
    issue = jira.issue("AK-5032")

    print(issue)
