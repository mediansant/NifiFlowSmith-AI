#!/usr/bin/env python3
"""
NiFi Flow Deployment Script
Deploys flows to local NiFi instance based on natural language descriptions
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nifi_nl_builder.tools.nifi_api import (
    create_pg, add_processor, connect, get_flow_status,
    start_processor, stop_processor, list_processors,
    update_processor_config, delete_processor, auto_terminate_relationships
)

class NiFiFlowDeployer:
    """Deploy NiFi flows to local instance"""
    
    def __init__(self):
        self.flow_templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load flow templates from JSON files"""
        templates_dir = Path(__file__).parent / "templates"
        templates = {}
        
        if templates_dir.exists():
            for template_file in templates_dir.glob("*.json"):
                try:
                    with open(template_file, 'r') as f:
                        templates[template_file.stem] = json.load(f)
                except Exception as e:
                    print(f"⚠️  Warning: Could not load template {template_file}: {e}")
        
        return templates
    
    def deploy_simple_flow(self, name: str, description: str) -> bool:
        """Deploy a simple flow with basic processors"""
        
        print(f"🚀 Deploying flow: {name}")
        print(f"📝 Description: {description}")
        
        try:
            # Create process group
            pg_id = create_pg(name)
            print(f"✅ Created process group: {name}")
            
            # Add processors based on description
            processors = self._create_processors_from_description(description, pg_id)
            
            # Connect processors
            self._connect_processors(processors, pg_id)
            
            # Start the flow
            self._start_flow(processors)
            
            print(f"🎉 Flow '{name}' deployed successfully!")
            print(f"🌐 View in NiFi UI: http://localhost:8080/nifi")
            
            return True
            
        except Exception as e:
            print(f"❌ Error deploying flow: {e}")
            return False
    
    def _create_processors_from_description(self, description: str, pg_id: str) -> Dict[str, str]:
        """Create processors based on natural language description"""
        
        processors = {}
        description_lower = description.lower()
        
        # Source processors
        if "file" in description_lower and "read" in description_lower:
            processors['source'] = self._add_file_reader(pg_id)
        elif "generate" in description_lower:
            processors['source'] = self._add_generator(pg_id)
        elif "http" in description_lower:
            processors['source'] = self._add_http_listener(pg_id)
        else:
            processors['source'] = self._add_generator(pg_id)  # Default
        
        # Processing processors
        if "transform" in description_lower or "convert" in description_lower:
            processors['transform'] = self._add_transformer(pg_id)
        
        if "filter" in description_lower:
            processors['filter'] = self._add_filter(pg_id)
        
        # Destination processors
        if "log" in description_lower:
            processors['destination'] = self._add_logger(pg_id)
        elif "file" in description_lower and "write" in description_lower:
            processors['destination'] = self._add_file_writer(pg_id)
        elif "database" in description_lower:
            processors['destination'] = self._add_database_writer(pg_id)
        else:
            processors['destination'] = self._add_logger(pg_id)  # Default
        
        return processors
    
    def _add_file_reader(self, pg_id: str) -> str:
        """Add a file reader processor"""
        config = {
            "properties": {
                "Input Directory": "/tmp/input",
                "File Filter": ".*\\.txt$",
                "Recurse Subdirectories": "true"
            },
            "schedulingPeriod": "1 sec"
        }
        processor_id = add_processor(pg_id, "org.apache.nifi.processors.standard.GetFile", config)
        print(f"✅ Added file reader processor")
        return processor_id
    
    def _add_generator(self, pg_id: str) -> str:
        """Add a flow file generator"""
        config = {
            "properties": {
                "File Size": "1KB",
                "Batch Size": "1",
                "Data Format": "Text"
            },
            "schedulingPeriod": "1 sec"
        }
        processor_id = add_processor(pg_id, "org.apache.nifi.processors.standard.GenerateFlowFile", config)
        print(f"✅ Added flow generator processor")
        return processor_id
    
    def _add_http_listener(self, pg_id: str) -> str:
        """Add an HTTP listener"""
        config = {
            "properties": {
                "Listening Port": "8081",
                "Base Path": "/nifi"
            }
        }
        processor_id = add_processor(pg_id, "org.apache.nifi.processors.standard.ListenHTTP", config)
        print(f"✅ Added HTTP listener processor")
        return processor_id
    
    def _add_transformer(self, pg_id: str) -> str:
        """Add a data transformer"""
        config = {
            "properties": {
                "Replacement Value": "transformed",
                "Search Value": "original"
            }
        }
        processor_id = add_processor(pg_id, "org.apache.nifi.processors.standard.ReplaceText", config)
        print(f"✅ Added transformer processor")
        return processor_id
    
    def _add_filter(self, pg_id: str) -> str:
        """Add a filter processor"""
        config = {
            "properties": {
                "Filter Mode": "include",
                "Filter": ".*"
            }
        }
        processor_id = add_processor(pg_id, "org.apache.nifi.processors.standard.RouteOnAttribute", config)
        print(f"✅ Added filter processor")
        return processor_id
    
    def _add_logger(self, pg_id: str) -> str:
        """Add a logger processor"""
        config = {
            "properties": {
                "Log Level": "info",
                "Log Payload": "true"
            },
            "autoTerminatedRelationships": ["success"]
        }
        processor_id = add_processor(pg_id, "org.apache.nifi.processors.standard.LogAttribute", config)
        print(f"✅ Added logger processor")
        return processor_id
    
    def _add_file_writer(self, pg_id: str) -> str:
        """Add a file writer"""
        config = {
            "properties": {
                "Directory": "/tmp/output",
                "Conflict Resolution Strategy": "replace"
            }
        }
        processor_id = add_processor(pg_id, "org.apache.nifi.processors.standard.PutFile", config)
        print(f"✅ Added file writer processor")
        return processor_id
    
    def _add_database_writer(self, pg_id: str) -> str:
        """Add a database writer"""
        config = {
            "properties": {
                "Database Connection Pooling Service": "",
                "SQL Statement": "INSERT INTO test_table (data) VALUES (?)"
            }
        }
        processor_id = add_processor(pg_id, "org.apache.nifi.processors.standard.PutDatabaseRecord", config)
        print(f"✅ Added database writer processor")
        return processor_id
    
    def _connect_processors(self, processors: Dict[str, str], pg_id: str):
        """Connect processors in sequence"""
        
        processor_list = list(processors.values())
        
        for i in range(len(processor_list) - 1):
            source_id = processor_list[i]
            target_id = processor_list[i + 1]
            
            connection_id = connect(source_id, target_id, pg_id)
            print(f"✅ Connected processor {i+1} to {i+2}")
    
    def _start_flow(self, processors: Dict[str, str]):
        """Start all processors in the flow"""
        
        processor_list = list(processors.values())
        
        for i, (name, processor_id) in enumerate(processors.items()):
            try:
                # Auto-terminate relationships for the final processor
                if i == len(processors) - 1:  # Last processor
                    auto_terminate_relationships(processor_id, ["success"])
                    print(f"✅ Auto-terminated relationships for {name} processor")
                
                start_processor(processor_id)
                print(f"✅ Started {name} processor")
            except Exception as e:
                print(f"⚠️  Warning: Could not start {name} processor: {e}")
    
    def deploy_from_template(self, template_name: str, flow_name: str) -> bool:
        """Deploy a flow from a predefined template"""
        
        if template_name not in self.flow_templates:
            print(f"❌ Template '{template_name}' not found")
            return False
        
        template = self.flow_templates[template_name]
        
        print(f"🚀 Deploying template: {template_name}")
        print(f"📝 Flow name: {flow_name}")
        
        try:
            # Create process group
            pg_id = create_pg(flow_name)
            
            # Add processors from template
            processors = {}
            for proc_config in template.get('processors', []):
                processor_id = add_processor(pg_id, proc_config['type'], proc_config.get('config', {}))
                processors[proc_config['name']] = processor_id
                print(f"✅ Added {proc_config['name']} processor")
            
            # Connect processors from template
            for connection in template.get('connections', []):
                source = processors.get(connection['source'])
                target = processors.get(connection['target'])
                if source and target:
                    connect(source, target)
                    print(f"✅ Connected {connection['source']} to {connection['target']}")
            
            # Start the flow
            self._start_flow(processors)
            
            print(f"🎉 Template '{template_name}' deployed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error deploying template: {e}")
            return False

def main():
    """Main deployment function"""
    
    deployer = NiFiFlowDeployer()
    
    print("🚀 NiFi Flow Deployer")
    print("=" * 40)
    
    # Example deployments
    examples = [
        {
            "name": "Simple Logging Flow",
            "description": "Generate data and log it"
        },
        {
            "name": "File Processing Flow", 
            "description": "Read from file, transform data, and write to output file"
        },
        {
            "name": "HTTP Data Flow",
            "description": "Listen for HTTP requests, filter data, and log results"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Deploying: {example['name']}")
        success = deployer.deploy_simple_flow(example['name'], example['description'])
        
        if success:
            print(f"✅ {example['name']} deployed successfully!")
        else:
            print(f"❌ {example['name']} deployment failed!")
        
        time.sleep(2)  # Brief pause between deployments
    
    print("\n🎉 Deployment complete!")
    print("🌐 View all flows in NiFi UI: http://localhost:8080/nifi")

if __name__ == "__main__":
    main() 