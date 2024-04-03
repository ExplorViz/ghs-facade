from . import app, gl
from flask import jsonify, request

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Fetch a list of projects from GitLab and return them as JSON."""
    try:
        projects = gl.projects.list(membership=True)
        projects_data = [{"id": project.id, "name": project.name, "web_url": project.web_url} for project in projects]
        return jsonify(projects_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_merge_request', methods=['POST'])
def update_merge_request():
    # Parse the JSON object from the request
    data = request.json
    merge_request_id = data.get('merge_request_id')
    project_id = data.get('project_id')
    explorviz_url = data.get('explorviz_url')
    
    try:
        # Obtain the project and merge request objects
        project = gl.projects.get(project_id, lazy=True)
        merge_request = project.mergerequests.get(merge_request_id, lazy=True)
        
        # Update the description of the merge request
        new_description = f"{merge_request.description}\n\nExplorViz URL: {explorviz_url}"
        merge_request.description = new_description
        merge_request.save()
        
        return jsonify({"success": True, "message": "Merge request updated successfully."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400