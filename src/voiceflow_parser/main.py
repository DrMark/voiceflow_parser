#!/usr/bin/env python3
"""
Voiceflow Parser - A tool to parse Voiceflow exports and generate project files.

This tool takes a Voiceflow export (.vf file) and converts it into a structured
project with appropriate files and folders.
"""
import sys
from pathlib import Path
from typing import Dict, Any

import click
from rich.console import Console

from voiceflow_parser.services.parser_service import VoiceflowParserService

console = Console()

def main(vf_file: str, output: str) -> None:
    """
    Parse a Voiceflow export (.vf file) and generate project files.
    
    Args:
        vf_file: Path to the Voiceflow export file (.vf)
        output: Output directory for the generated project
    """
    try:
        # Create a parser service
        parser_service = VoiceflowParserService(console=console)
        
        # Load the export file
        export_data = parser_service.load_export(vf_file)
        
        # Parse the export data
        export = parser_service.parse_export(export_data)
        
        # Generate the project structure
        parser_service.generate_project_structure(export, output)
        
        console.print(f"[bold green]Successfully parsed and generated project in:[/bold green] {output}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # This is for direct script execution
    # For normal usage, use the CLI entry point
    if len(sys.argv) < 2:
        console.print("[bold red]Error:[/bold red] Missing Voiceflow export file path.")
        console.print("Usage: python -m voiceflow_parser.main <vf_file> [output_dir]")
        sys.exit(1)
    
    vf_file = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    main(vf_file, output)
