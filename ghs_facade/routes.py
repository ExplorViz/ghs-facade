from ghs_facade.helper_functions import getProjects
from . import app, gl
from flask import jsonify, request
import os
import logging
import requests
import json
import gitlab

LOGGER = logging.getLogger(__name__)

@app.route('/update_merge_request', methods=['POST'])
def update_merge_request():
    data = request.get_json(silent=True) or {}

    merge_request_id = data.get('merge_request_id') or os.environ.get('CI_MERGE_REQUEST_IID')
    project_id = data.get('project_id') or os.environ.get('CI_MERGE_REQUEST_PROJECT_ID')
    explorviz_url = data.get('explorviz_url') or os.environ.get('DEFAULT_EXPLORVIZ_URL')

    LOGGER.debug(f"Update MR: PId: {project_id}, MId: {merge_request_id}, ExplorViz: {explorviz_url}")
    
    # Check if the necessary parameters are provided
    if not all([merge_request_id, project_id, explorviz_url]):
        return jsonify({"success": False, "message": "Missing required parameters."}), 400
    
    try:
        # Obtain the project and merge request objects
        project = gl.projects.get(project_id)
        merge_request = project.mergerequests.get(merge_request_id)

        if "ExplorViz URL" not in merge_request.description:
            # Update the description of the merge request
            new_description = f"{merge_request.description}\n\nExplorViz URL: {explorviz_url}"
            merge_request.description = new_description
            merge_request.save()
            return jsonify({"success": True, "message": "Merge request updated successfully."}), 200
        
        return jsonify({"success": True, "message": "Description already includes ExplorViz URL."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


# could be usefull in the future to get a project by its name
@app.route('/get_project/<string:name>/<string:api_token>/<string:host_url>', methods=['GET'])
@app.route('/get_project/<string:name>', methods=['GET'])
def get_project(name: str, api_token=None, host_url=None):
    LOGGER.debug(f"Get one projects, that can be accessed with the API-Token.")

    if (api_token == None and host_url == None):
        try:
            projects = gl.projects.list(get_all=True, search=name)
            return getProjects(projects)
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 400
    else:
        try:

            gitApi = gitlab.Gitlab("https://" + host_url, private_token=api_token)
            projects = gitApi.projects.list(get_all=True, search=name)
            return getProjects(projects)

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 400



@app.route('/get_all_projects/<string:api_token>/<string:host_url>', methods=['GET'])
@app.route('/get_all_projects', methods=['GET'])
def get_all_projects(api_token=None, host_url=None):
    LOGGER.debug(f"Get all projects, that can be accessed with the API-Token.")

    if (api_token != None and host_url != None):
        try:
            gitApi = gitlab.Gitlab("https://" + host_url, private_token=api_token)
            projects = gitApi.projects.list(get_all=True)
            return getProjects(projects)

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 400
    else:
        try:
            projects = gl.projects.list(get_all=True)
            return getProjects(projects)

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 400


@app.route('/create_issue', methods=['POST'])
def create_issue():
    data = request.get_json()

    project_id = data.get('project_id')
    api_token = data.get('api_token')
    host_url = data.get('host_url')
    title = data.get('title')
    description = data.get('description')

    LOGGER.debug(f"Create Issue for project: {project_id}")

    if not all([project_id, title, description]):
        return jsonify({"success": False, "message": "Missing required parameters."}), 400

    if not all([project_id, api_token, host_url, title, description]):
        try:
            project = gl.projects.get(project_id)
            issue = project.issues.create({"title": title, "description": description})
            issue.save()
            return jsonify({"success": True, "message": "Successfully created Issue"}), 200
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 400
    
    else:
        try:
            gitApi = gitlab.Gitlab("https://" + host_url, private_token=api_token)
            project = gitApi.projects.get(project_id)
            issue = project.issues.create({"title": title, "description": description})
            issue.save()
            return jsonify({"success": True, "message": "Successfully created Issue"}), 200
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 400