from .nifi_api import (
    create_pg, add_processor, connect, export_flow,
    start_processor, stop_processor, get_processor_status,
    update_processor_config, delete_processor, list_processors,
    list_process_groups, get_flow_status, create_template,
    instantiate_template
)

class NiFiTool:
    """NiFi API Tool for CrewAI agents"""
    
    def __init__(self):
        self.name = "nifi_api"
        self.description = "Low-level NiFi REST operations for creating, managing, and deploying flows"
    
    def create_process_group(self, name: str, parent: str = "root") -> str:
        """Create a new process group in NiFi"""
        return create_pg(name, parent)
    
    def add_processor(self, process_group_id: str, processor_type: str, config: dict) -> str:
        """Add a processor to a process group"""
        return add_processor(process_group_id, processor_type, config)
    
    def connect_processors(self, source_id: str, target_id: str, process_group_id: str = "root", source_port: str = "success", target_port: str = "in") -> str:
        """Connect two processors or process groups"""
        return connect(source_id, target_id, process_group_id, source_port, target_port)
    
    def export_flow_definition(self, process_group_id: str = "root") -> dict:
        """Export flow definition as JSON"""
        return export_flow(process_group_id)
    
    def start_processor(self, processor_id: str) -> dict:
        """Start a processor"""
        return start_processor(processor_id)
    
    def stop_processor(self, processor_id: str) -> dict:
        """Stop a processor"""
        return stop_processor(processor_id)
    
    def get_processor_status(self, processor_id: str) -> dict:
        """Get processor status and statistics"""
        return get_processor_status(processor_id)
    
    def update_processor_config(self, processor_id: str, config: dict) -> dict:
        """Update processor configuration"""
        return update_processor_config(processor_id, config)
    
    def delete_processor(self, processor_id: str) -> bool:
        """Delete a processor"""
        return delete_processor(processor_id)
    
    def list_processors(self, process_group_id: str = "root") -> list:
        """List all processors in a process group"""
        return list_processors(process_group_id)
    
    def list_process_groups(self, parent_id: str = "root") -> list:
        """List all process groups under a parent"""
        return list_process_groups(parent_id)
    
    def get_flow_status(self, process_group_id: str = "root") -> dict:
        """Get overall flow status and statistics"""
        return get_flow_status(process_group_id)
    
    def create_template(self, name: str, description: str, process_group_id: str = "root") -> str:
        """Create a template from a process group"""
        return create_template(name, description, process_group_id)
    
    def instantiate_template(self, template_id: str, process_group_id: str = "root") -> dict:
        """Instantiate a template in a process group"""
        return instantiate_template(template_id, process_group_id)
    
    def create_process_group(self, name: str, parent: str = "root") -> str:
        """Create a new process group in NiFi"""
        return create_pg(name, parent)
    
    def add_processor(self, process_group_id: str, processor_type: str, config: dict) -> str:
        """Add a processor to a process group"""
        return add_processor(process_group_id, processor_type, config)
    
    def connect_processors(self, source_id: str, target_id: str, process_group_id: str = "root", source_port: str = "success", target_port: str = "in") -> str:
        """Connect two processors or process groups"""
        return connect(source_id, target_id, process_group_id, source_port, target_port)
    
    def export_flow_definition(self, process_group_id: str = "root") -> dict:
        """Export flow definition as JSON"""
        return export_flow(process_group_id)
    
    def start_processor(self, processor_id: str) -> dict:
        """Start a processor"""
        return start_processor(processor_id)
    
    def stop_processor(self, processor_id: str) -> dict:
        """Stop a processor"""
        return stop_processor(processor_id)
    
    def get_processor_status(self, processor_id: str) -> dict:
        """Get processor status and statistics"""
        return get_processor_status(processor_id)
    
    def update_processor_config(self, processor_id: str, config: dict) -> dict:
        """Update processor configuration"""
        return update_processor_config(processor_id, config)
    
    def delete_processor(self, processor_id: str) -> bool:
        """Delete a processor"""
        return delete_processor(processor_id)
    
    def list_processors(self, process_group_id: str = "root") -> list:
        """List all processors in a process group"""
        return list_processors(process_group_id)
    
    def list_process_groups(self, parent_id: str = "root") -> list:
        """List all process groups under a parent"""
        return list_process_groups(parent_id)
    
    def get_flow_status(self, process_group_id: str = "root") -> dict:
        """Get overall flow status and statistics"""
        return get_flow_status(process_group_id)
    
    def create_template(self, name: str, description: str, process_group_id: str = "root") -> str:
        """Create a template from a process group"""
        return create_template(name, description, process_group_id)
    
    def instantiate_template(self, template_id: str, process_group_id: str = "root") -> dict:
        """Instantiate a template in a process group"""
        return instantiate_template(template_id, process_group_id) 