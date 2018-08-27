from github import Github


def connect (user, password):
    #  create and return the Github instance
    return Github(user, password)

def show_projects(g):
    for repo in g.get_user().get_repos():
        print(repo.name)
