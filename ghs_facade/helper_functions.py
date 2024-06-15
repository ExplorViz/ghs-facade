def getProjects(response: list[any]) -> list[any]:
    projects = []
    for project in response:
        simpleProject = {}
        simpleProject["id"] = project["id"]
        simpleProject["name"] = project["name"]
        projects.append(simpleProject)
    return projects
