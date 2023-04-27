import itertools
from os import environ
from time import sleep

from github import Github
from github.GithubException import GithubException

ORGANIZATION = "UCB-W255"
SEMESTER_REPO_PREFIX = "spring23"
STUDENT_TEAM_ID = 5538453
ADMIN_TEAM_ID = 5538478
MIDS4LIFE_TEAM_ID = 5978047

instructor_list = []
student_list = []
mids4life_list = []


def runner():
    g = Github(environ["GITHUB_PAT"])

    org = g.get_organization(ORGANIZATION)
    student_team = org.get_team(STUDENT_TEAM_ID)
    admin_team = org.get_team(ADMIN_TEAM_ID)
    mids4life_team = org.get_team(MIDS4LIFE_TEAM_ID)

    # Add Everyone to Org
    for student in list(
        itertools.chain.from_iterable([student_list, instructor_list, mids4life_list])
    ):
        print(f"Adding {student} to {ORGANIZATION} organization")
        user = g.get_user(student)
        try:
            org.invite_user(user)
        except GithubException as e:
            print(e)

    # Add Instructors to the Admin Team
    for instructor in instructor_list:
        print(f"Adding {instructor} to Instructor team")
        user = g.get_user(instructor)
        admin_team.add_membership(user)

    # Add Students to the Student Team
    for student in student_list:
        print(f"Adding {student} to Student team")
        user = g.get_user(student)
        student_team.add_membership(user)

    # Create Student Repo with student as admin
    for student in student_list:
        repo = f"{SEMESTER_REPO_PREFIX}-{student}"
        print(f"Creating {student} repo: {repo}")
        user = g.get_user(student)
        repo = org.create_repo(repo, private=True)
        sleep(5)
        repo.add_to_collaborators(user, permission="admin")

    # Add Alumni to the MIDS4LIFE Team
    for mids4life in mids4life_list:
        print(f"Adding {mids4life} to MIDS4LIFE team")
        user = g.get_user(mids4life)
        mids4life_team.add_membership(user)

    # Create Alumni Repo with Alumni as admin
    for mids4life in mids4life_list:
        repo = f"mids4life-{mids4life}"
        print(f"Creating {mids4life} repo: {repo}")
        user = g.get_user(mids4life)
        repo = org.create_repo(repo, private=True)
        sleep(5)
        repo.add_to_collaborators(user, permission="admin")
