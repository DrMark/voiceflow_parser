#!/usr/bin/env python3
"""
Simple script to parse a Voiceflow export file and dump its contents to a text file.
"""
import json
import sys
import shutil
from pathlib import Path
from typing import Dict, Any, List, Union
from collections import Counter


def parse_voiceflow_file(input_file: str, output_file: str = None) -> None:
    """
    Parse a Voiceflow export file and dump its contents to a text file.
    
    Args:
        input_file: Path to the Voiceflow export file (.vf)
        output_file: Path to the output text file. If None, will be generated based on input filename.
    """
    try:
        # Process input file path
        input_path = Path(input_file)
        file_name = input_path.stem
        
        # Set up directories
        exports_dir = Path('voiceflow_exports')
        exports_dir.mkdir(exist_ok=True)
        
        # Copy the file to the exports directory if it's not already there
        if not str(input_path).startswith(str(exports_dir)):
            export_file_path = exports_dir / input_path.name
            if not export_file_path.exists():
                shutil.copy2(input_file, export_file_path)
                print(f"Copied export file to {export_file_path}")
            input_file = str(export_file_path)
        
        # Load the JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Determine output file path
        if output_file is None:
            projects_dir = Path('voiceflow_projects')
            projects_dir.mkdir(exist_ok=True)
            output_file = str(projects_dir / f"{file_name}.structure.txt")
        
        # Create the output directory if it doesn't exist
        output_path = Path(output_file).parent
        output_path.mkdir(exist_ok=True, parents=True)
        
        # Write the formatted JSON to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write project info
            if "project" in data:
                project = data["project"]
                f.write(f"Project: {project.get('name', 'Unnamed')}\n")
                f.write(f"Team ID: {project.get('teamID', 'Unknown')}\n")
                f.write(f"Project ID: {project.get('projectID', 'Unknown')}\n")
                f.write(f"Created: {project.get('createdAt', 'Unknown')}\n")
                f.write(f"Updated: {project.get('updatedAt', 'Unknown')}\n\n")
            
            # Count node types
            node_types = Counter()
            for diagram_id, diagram in data.get("diagrams", {}).items():
                for node_id, node in diagram.get("nodes", {}).items():
                    if isinstance(node, dict) and "type" in node:
                        node_types[node["type"]] += 1
            
            # Write node type counts
            f.write("Node Types:\n")
            for node_type, count in node_types.most_common():
                f.write(f"  {node_type}: {count}\n")
            f.write("\n")
            
            # Write diagram info
            f.write(f"Diagrams: {len(data.get('diagrams', {}))}\n")
            for diagram_id, diagram in data.get("diagrams", {}).items():
                f.write(f"  {diagram.get('name', 'Unnamed')}: {len(diagram.get('nodes', {}))} nodes\n")
            f.write("\n")
            
            # Write variable info
            f.write(f"Variables: {len(data.get('variables', []))}\n")
            for var in data.get("variables", []):
                if isinstance(var, dict):
                    f.write(f"  {var.get('name', 'Unnamed')}: {var.get('type', 'Unknown')}\n")
            f.write("\n")
            
            # Write intent info
            f.write(f"Intents: {len(data.get('intents', []))}\n")
            for intent in data.get("intents", []):
                if isinstance(intent, dict):
                    f.write(f"  {intent.get('name', 'Unnamed')}: {len(intent.get('inputs', []))} inputs\n")
            f.write("\n")
            
            # Write prompt info
            f.write(f"Prompts: {len(data.get('prompts', []))}\n")
            for prompt in data.get("prompts", []):
                if isinstance(prompt, dict):
                    f.write(f"  {prompt.get('name', 'Unnamed')}: {len(prompt.get('messageOrder', []))} messages\n")
            f.write("\n")
            
            # Write agent info
            f.write(f"Agents: {len(data.get('agents', []))}\n")
            for agent in data.get("agents", []):
                if isinstance(agent, dict):
                    f.write(f"  {agent.get('name', 'Unnamed')}: {len(agent.get('instructions', []))} instructions\n")
            f.write("\n")
            
            # Write component counts
            components = [
                ("buttons", "Buttons"),
                ("captures", "Captures"),
                ("apis", "APIs"),
                ("kbSearches", "KB Searches"),
                ("choices", "Choices"),
                ("cards", "Cards")
            ]
            
            for key, label in components:
                count = len(data.get(key, []))
                f.write(f"{label}: {count}\n")
                if count > 0:
                    for item in data.get(key, []):
                        if isinstance(item, dict):
                            f.write(f"  {item.get('name', item.get('id', 'Unnamed'))}\n")
                    f.write("\n")
        
        print(f"Successfully parsed Voiceflow export and wrote structure to {output_file}")
        
    except json.JSONDecodeError:
        print(f"Error: The file {input_file} is not a valid JSON file.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_voiceflow.py <input_file.vf> [output_file.txt]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    parse_voiceflow_file(input_file, output_file)
