from . import app, gl
from flask import jsonify, request
import os

@app.route('/update_merge_request', methods=['POST'])
def update_merge_request():
    # Parse the JSON object from the request
    data = request.json
    merge_request_id = data.get('merge_request_id') or os.environ.get('CI_MERGE_REQUEST_IID ')
    project_id = data.get('project_id') or os.environ.get('CI_MERGE_REQUEST_PROJECT_ID ')
    explorviz_url = data.get('explorviz_url') or os.environ.get('DEFAULT_EXPLORVIZ_URL')
    
    # Check if the necessary parameters are provided
    if not all([merge_request_id, project_id, explorviz_url]):
        return jsonify({"success": False, "message": "Missing required parameters."}), 400
    
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