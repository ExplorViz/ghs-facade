def getProjects(response: list[any]) -> list[any]:
    projects = []
    for project in response:
        simpleProject = {}
        simpleProject["id"] = project["id"]
        simpleProject["name"] = project["name"]
        projects.append(simpleProject)
    return projects


def getProjects(projects) -> list[any]:
    allProjects = []
    for project in projects:
        simpleProject = {}
        simpleProject["id"] = project.id
        simpleProject["name"] = project.name
        allProjects.append(simpleProject)
    return allProjects