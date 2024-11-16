def getProjects(projects) -> list[any]:
    allProjects = []
    for project in projects:
        simpleProject = {}
        simpleProject["id"] = project.id
        simpleProject["name"] = project.name
        allProjects.append(simpleProject)
    
    sortedProjects = sorted(allProjects, key=lambda project: project["name"])
    
    return sortedProjects