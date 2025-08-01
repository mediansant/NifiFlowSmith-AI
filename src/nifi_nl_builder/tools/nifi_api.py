import requests
import os
import json

# Updated configuration for local Docker setup
NIFI = os.getenv("NIFI_URL", "http://localhost:8080")
TOKEN = os.getenv("NIFI_TOKEN")
USERNAME = os.getenv("NIFI_USERNAME", "admin")
PASSWORD = os.getenv("NIFI_PASSWORD", "admin123")

def _auth():
    """Get authentication headers for NiFi API"""
    if TOKEN:
        return {"Authorization": f"Bearer {TOKEN}"}
    elif USERNAME and PASSWORD:
        # For local Docker setup, we'll use basic auth
        import base64
        credentials = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
        return {"Authorization": f"Basic {credentials}"}
    return {}

def _make_request(method, url, **kwargs):
    """Make HTTP request with proper error handling"""
    try:
        response = requests.request(method, url, headers=_auth(), verify=False, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"❌ NiFi API Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        raise

def create_pg(name, parent="root"):
    body = {"revision": {"version": 0},
            "component": {"name": name, "position": {"x": 0, "y": 0}}}
    r = _make_request("POST", f"{NIFI}/nifi-api/process-groups/{parent}/process-groups", json=body)
    return r.json()["id"]

def add_processor(pg, ptype, cfg):
    body = {"revision": {"version": 0},
            "component": {"type": ptype,
                          "position": {"x": 0, "y": 0},
                          "config": cfg}}
    r = _make_request("POST", f"{NIFI}/nifi-api/process-groups/{pg}/processors", json=body)
    return r.json()["id"]

def connect(source_id, target_id, pg_id="root", source_port="success", target_port="in"):
    """Connect two processors or process groups"""
    
    # Get source processor details to find available relationships
    source_response = _make_request("GET", f"{NIFI}/nifi-api/processors/{source_id}")
    source_processor = source_response.json()
    
    # Get target processor details to find available relationships
    target_response = _make_request("GET", f"{NIFI}/nifi-api/processors/{target_id}")
    target_processor = target_response.json()
    
    # Find available relationships
    available_relationships = []
    for rel in source_processor['component']['relationships']:
        if rel['autoTerminate'] == False:
            available_relationships.append(rel['name'])
    
    # Use the first available relationship or fallback to 'success'
    if available_relationships:
        source_port = available_relationships[0]
    
    body = {
        "revision": {"version": 0},
        "component": {
            "source": {
                "id": source_id,
                "type": "PROCESSOR",
                "groupId": pg_id
            },
            "destination": {
                "id": target_id,
                "type": "PROCESSOR",
                "groupId": pg_id
            },
            "selectedRelationships": [source_port]
        }
    }
    r = _make_request("POST", f"{NIFI}/nifi-api/process-groups/{pg_id}/connections", json=body)
    return r.json()["id"]

def export_flow(pg_id="root"):
    """Export flow definition as JSON"""
    r = _make_request("GET", f"{NIFI}/nifi-api/process-groups/{pg_id}/download")
    return r.json()

def start_processor(processor_id):
    """Start a processor"""
    # First get the current processor state
    current_response = _make_request("GET", f"{NIFI}/nifi-api/processors/{processor_id}")
    current_processor = current_response.json()
    
    # Update with running state
    body = {
        "revision": current_processor["revision"],
        "component": {
            "id": processor_id,
            "state": "RUNNING"
        }
    }
    r = _make_request("PUT", f"{NIFI}/nifi-api/processors/{processor_id}", json=body)
    return r.json()

def stop_processor(processor_id):
    """Stop a processor"""
    # First get the current processor state
    current_response = _make_request("GET", f"{NIFI}/nifi-api/processors/{processor_id}")
    current_processor = current_response.json()
    
    # Update with stopped state
    body = {
        "revision": current_processor["revision"],
        "component": {
            "id": processor_id,
            "state": "STOPPED"
        }
    }
    r = _make_request("PUT", f"{NIFI}/nifi-api/processors/{processor_id}", json=body)
    return r.json()

def get_processor_status(processor_id):
    """Get processor status and statistics"""
    r = _make_request("GET", f"{NIFI}/nifi-api/processors/{processor_id}")
    return r.json()

def update_processor_config(processor_id, config):
    """Update processor configuration"""
    body = {"revision": {"version": 0}, "component": {"config": config}}
    r = _make_request("PUT", f"{NIFI}/nifi-api/processors/{processor_id}", json=body)
    return r.json()

def auto_terminate_relationships(processor_id, relationships):
    """Auto-terminate specific relationships for a processor"""
    # First get the current processor state
    current_response = _make_request("GET", f"{NIFI}/nifi-api/processors/{processor_id}")
    current_processor = current_response.json()
    
    # Update relationships to auto-terminate
    updated_relationships = []
    for rel in current_processor["component"]["relationships"]:
        if rel["name"] in relationships:
            rel["autoTerminate"] = True
        updated_relationships.append(rel)
    
    # Update processor with auto-terminated relationships
    body = {
        "revision": current_processor["revision"],
        "component": {
            "id": processor_id,
            "config": current_processor["component"]["config"],
            "relationships": updated_relationships
        }
    }
    r = _make_request("PUT", f"{NIFI}/nifi-api/processors/{processor_id}", json=body)
    return r.json()

def delete_processor(processor_id):
    """Delete a processor"""
    _make_request("DELETE", f"{NIFI}/nifi-api/processors/{processor_id}")
    return True

def list_processors(pg_id="root"):
    """List all processors in a process group"""
    r = _make_request("GET", f"{NIFI}/nifi-api/process-groups/{pg_id}/processors")
    return r.json()["processors"]

def list_process_groups(parent_id="root"):
    """List all process groups under a parent"""
    r = _make_request("GET", f"{NIFI}/nifi-api/process-groups/{parent_id}/process-groups")
    return r.json()["processGroups"]

def get_flow_status(pg_id="root"):
    """Get overall flow status and statistics"""
    try:
        r = _make_request("GET", f"{NIFI}/nifi-api/process-groups/{pg_id}/status")
        return r.json()
    except:
        # Fallback to getting basic process group info
        r = _make_request("GET", f"{NIFI}/nifi-api/process-groups/{pg_id}")
        return r.json()

def create_template(name, description, pg_id="root"):
    """Create a template from a process group"""
    body = {
        "name": name,
        "description": description,
        "snippet": {
            "processGroups": {},
            "processors": {},
            "connections": {},
            "inputPorts": {},
            "outputPorts": {},
            "funnels": {},
            "labels": {},
            "remoteProcessGroups": {}
        }
    }
    r = _make_request("POST", f"{NIFI}/nifi-api/process-groups/{pg_id}/templates", json=body)
    return r.json()["id"]

def instantiate_template(template_id, pg_id="root"):
    """Instantiate a template in a process group"""
    body = {"originX": 0, "originY": 0}
    r = _make_request("POST", f"{NIFI}/nifi-api/process-groups/{pg_id}/template-instance", json=body)
    return r.json() 