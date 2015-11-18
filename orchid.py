#!/usr/bin/env python

# Author: Fadi Almasri

from ConfigParser import SafeConfigParser
import gitlab
import json

parser = SafeConfigParser()
parser.read('config')

GITLAB_URL = parser.get('gitlab', 'url')
SECRET_TOKEN = parser.get('gitlab', 'secret_token')

# Register a connection to a gitlab instance, using its URL and a user private token
gl = gitlab.Gitlab(GITLAB_URL, SECRET_TOKEN)

# Connect to get the current user
gl.auth()

# Get a list of projects
for project in gl.Project():
    print(project.name)

    # Get all commits
    for commit in project.Commit():
        c = json.loads(commit.json())
        print c["created_at"]
        print c["id"]
        print c["author_name"]
        #gitlab.ProjectCommit.

