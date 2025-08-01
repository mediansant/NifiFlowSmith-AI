"""
CrewAI-compatible NiFi tools using BaseTool
"""

from crewai.tools import BaseTool
from .nifi_api import (
    create_pg, add_processor, connect, export_flow,
    start_processor, stop_processor, get_processor_status,
    update_processor_config, delete_processor, list_processors,
    list_process_groups, get_flow_status, create_template,
    instantiate_template
)

class CreateProcessGroupTool(BaseTool):
    name: str = "create_nifi_process_group"
    description: str = "Create a new process group in NiFi"
    
    def _run(self, name: str, parent: str = "root") -> str:
        return create_pg(name, parent)

class AddProcessorTool(BaseTool):
    name: str = "add_nifi_processor"
    description: str = "Add a processor to a process group"
    
    def _run(self, process_group_id: str, processor_type: str, config: dict) -> str:
        return add_processor(process_group_id, processor_type, config)

class ConnectProcessorsTool(BaseTool):
    name: str = "connect_nifi_processors"
    description: str = "Connect two processors or process groups"
    
    def _run(self, source_id: str, target_id: str, process_group_id: str = "root") -> str:
        return connect(source_id, target_id, process_group_id)

class StartProcessorTool(BaseTool):
    name: str = "start_nifi_processor"
    description: str = "Start a processor"
    
    def _run(self, processor_id: str) -> dict:
        return start_processor(processor_id)

class StopProcessorTool(BaseTool):
    name: str = "stop_nifi_processor"
    description: str = "Stop a processor"
    
    def _run(self, processor_id: str) -> dict:
        return stop_processor(processor_id)

class ListProcessorsTool(BaseTool):
    name: str = "list_nifi_processors"
    description: str = "List all processors in a process group"
    
    def _run(self, process_group_id: str = "root") -> list:
        return list_processors(process_group_id)

class GetFlowStatusTool(BaseTool):
    name: str = "get_nifi_flow_status"
    description: str = "Get overall flow status and statistics"
    
    def _run(self, process_group_id: str = "root") -> dict:
        return get_flow_status(process_group_id)

class ExportFlowTool(BaseTool):
    name: str = "export_nifi_flow"
    description: str = "Export flow definition as JSON"
    
    def _run(self, process_group_id: str = "root") -> dict:
        return export_flow(process_group_id)

# Function-based tools for backward compatibility
def create_nifi_process_group(name: str, parent: str = "root") -> str:
    """Create a new process group in NiFi"""
    return create_pg(name, parent)

def add_nifi_processor(process_group_id: str, processor_type: str, config: dict) -> str:
    """Add a processor to a process group"""
    return add_processor(process_group_id, processor_type, config)

def connect_nifi_processors(source_id: str, target_id: str, process_group_id: str = "root") -> str:
    """Connect two processors or process groups"""
    return connect(source_id, target_id, process_group_id)

def start_nifi_processor(processor_id: str) -> dict:
    """Start a processor"""
    return start_processor(processor_id)

def stop_nifi_processor(processor_id: str) -> dict:
    """Stop a processor"""
    return stop_processor(processor_id)

def list_nifi_processors(process_group_id: str = "root") -> list:
    """List all processors in a process group"""
    return list_processors(process_group_id)

def get_nifi_flow_status(process_group_id: str = "root") -> dict:
    """Get overall flow status and statistics"""
    return get_flow_status(process_group_id)

def export_nifi_flow(process_group_id: str = "root") -> dict:
    """Export flow definition as JSON"""
    return export_flow(process_group_id) 