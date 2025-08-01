#!/usr/bin/env python3
"""
NiFi Command Line Interface
Manage NiFi flows from the command line
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nifi_nl_builder.tools.nifi_api import (
    list_process_groups, list_processors, get_flow_status,
    start_processor, stop_processor, delete_processor
)
from deploy_flow import NiFiFlowDeployer

class NiFiCLI:
    """Command line interface for NiFi management"""
    
    def __init__(self):
        self.deployer = NiFiFlowDeployer()
    
    def list_flows(self):
        """List all flows in NiFi"""
        print("📋 NiFi Flows")
        print("=" * 40)
        
        try:
            process_groups = list_process_groups()
            
            if not process_groups:
                print("No flows found.")
                return
            
            for pg in process_groups:
                print(f"📁 {pg['component']['name']}")
                print(f"   ID: {pg['id']}")
                print(f"   Status: {pg['status']['aggregateSnapshot']['input']}")
                print()
                
        except Exception as e:
            print(f"❌ Error listing flows: {e}")
    
    def show_flow(self, flow_name: str):
        """Show details of a specific flow"""
        print(f"📊 Flow Details: {flow_name}")
        print("=" * 40)
        
        try:
            process_groups = list_process_groups()
            
            target_pg = None
            for pg in process_groups:
                if pg['component']['name'] == flow_name:
                    target_pg = pg
                    break
            
            if not target_pg:
                print(f"❌ Flow '{flow_name}' not found")
                return
            
            pg_id = target_pg['id']
            
            print(f"📁 Name: {target_pg['component']['name']}")
            print(f"🆔 ID: {pg_id}")
            print(f"📊 Status: {target_pg['status']['aggregateSnapshot']['input']}")
            print()
            
            # List processors in this flow
            processors = list_processors(pg_id)
            
            if processors:
                print("🔧 Processors:")
                for proc in processors:
                    print(f"   • {proc['component']['name']} ({proc['component']['type']})")
                    print(f"     Status: {proc['component']['state']}")
                    print(f"     ID: {proc['id']}")
                    print()
            else:
                print("No processors found in this flow.")
                
        except Exception as e:
            print(f"❌ Error showing flow: {e}")
    
    def start_flow(self, flow_name: str):
        """Start all processors in a flow"""
        print(f"▶️  Starting flow: {flow_name}")
        
        try:
            process_groups = list_process_groups()
            
            target_pg = None
            for pg in process_groups:
                if pg['component']['name'] == flow_name:
                    target_pg = pg
                    break
            
            if not target_pg:
                print(f"❌ Flow '{flow_name}' not found")
                return
            
            pg_id = target_pg['id']
            processors = list_processors(pg_id)
            
            started_count = 0
            for proc in processors:
                try:
                    start_processor(proc['id'])
                    print(f"✅ Started {proc['component']['name']}")
                    started_count += 1
                except Exception as e:
                    print(f"⚠️  Could not start {proc['component']['name']}: {e}")
            
            print(f"🎉 Started {started_count} processors in flow '{flow_name}'")
            
        except Exception as e:
            print(f"❌ Error starting flow: {e}")
    
    def stop_flow(self, flow_name: str):
        """Stop all processors in a flow"""
        print(f"⏹️  Stopping flow: {flow_name}")
        
        try:
            process_groups = list_process_groups()
            
            target_pg = None
            for pg in process_groups:
                if pg['component']['name'] == flow_name:
                    target_pg = pg
                    break
            
            if not target_pg:
                print(f"❌ Flow '{flow_name}' not found")
                return
            
            pg_id = target_pg['id']
            processors = list_processors(pg_id)
            
            stopped_count = 0
            for proc in processors:
                try:
                    stop_processor(proc['id'])
                    print(f"✅ Stopped {proc['component']['name']}")
                    stopped_count += 1
                except Exception as e:
                    print(f"⚠️  Could not stop {proc['component']['name']}: {e}")
            
            print(f"🎉 Stopped {stopped_count} processors in flow '{flow_name}'")
            
        except Exception as e:
            print(f"❌ Error stopping flow: {e}")
    
    def deploy_flow(self, name: str, description: str):
        """Deploy a new flow from description"""
        print(f"🚀 Deploying new flow: {name}")
        print(f"📝 Description: {description}")
        
        success = self.deployer.deploy_simple_flow(name, description)
        
        if success:
            print(f"🎉 Flow '{name}' deployed successfully!")
        else:
            print(f"❌ Failed to deploy flow '{name}'")
    
    def deploy_template(self, template_name: str, flow_name: str):
        """Deploy a flow from template"""
        print(f"🚀 Deploying template: {template_name}")
        print(f"📝 Flow name: {flow_name}")
        
        success = self.deployer.deploy_from_template(template_name, flow_name)
        
        if success:
            print(f"🎉 Template '{template_name}' deployed as '{flow_name}'!")
        else:
            print(f"❌ Failed to deploy template '{template_name}'")
    
    def list_templates(self):
        """List available templates"""
        print("📋 Available Templates")
        print("=" * 40)
        
        if not self.deployer.flow_templates:
            print("No templates found.")
            return
        
        for name, template in self.deployer.flow_templates.items():
            print(f"📄 {name}")
            print(f"   Description: {template.get('description', 'No description')}")
            print(f"   Processors: {len(template.get('processors', []))}")
            print()

def main():
    """Main CLI function"""
    
    parser = argparse.ArgumentParser(description="NiFi Flow Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List flows command
    subparsers.add_parser("list", help="List all flows")
    
    # Show flow command
    show_parser = subparsers.add_parser("show", help="Show flow details")
    show_parser.add_argument("flow_name", help="Name of the flow to show")
    
    # Start flow command
    start_parser = subparsers.add_parser("start", help="Start a flow")
    start_parser.add_argument("flow_name", help="Name of the flow to start")
    
    # Stop flow command
    stop_parser = subparsers.add_parser("stop", help="Stop a flow")
    stop_parser.add_argument("flow_name", help="Name of the flow to stop")
    
    # Deploy flow command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy a new flow")
    deploy_parser.add_argument("name", help="Name of the flow")
    deploy_parser.add_argument("description", help="Description of the flow")
    
    # Deploy template command
    template_parser = subparsers.add_parser("template", help="Deploy from template")
    template_parser.add_argument("template_name", help="Name of the template")
    template_parser.add_argument("flow_name", help="Name for the new flow")
    
    # List templates command
    subparsers.add_parser("templates", help="List available templates")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = NiFiCLI()
    
    if args.command == "list":
        cli.list_flows()
    elif args.command == "show":
        cli.show_flow(args.flow_name)
    elif args.command == "start":
        cli.start_flow(args.flow_name)
    elif args.command == "stop":
        cli.stop_flow(args.flow_name)
    elif args.command == "deploy":
        cli.deploy_flow(args.name, args.description)
    elif args.command == "template":
        cli.deploy_template(args.template_name, args.flow_name)
    elif args.command == "templates":
        cli.list_templates()

if __name__ == "__main__":
    main() 