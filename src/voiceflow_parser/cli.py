#!/usr/bin/env python3
"""
Command-line interface for the Voiceflow Parser.
"""
import os
import shutil
from pathlib import Path
import click
from rich.console import Console

from voiceflow_parser.services.parser_service import VoiceflowParserService

console = Console()

@click.group()
def cli():
    """Voiceflow Parser - Convert Voiceflow exports to project files."""
    pass

@cli.command()
@click.argument('vf_file', type=click.Path(exists=True))
@click.option('--output', '-o', default=None, help='Output directory for the generated project')
def parse(vf_file, output):
    """Parse a Voiceflow export file and generate project files."""
    console.print(f"[bold green]Voiceflow Parser[/bold green]")
    
    try:
        # Create a parser service
        parser_service = VoiceflowParserService(console=console)
        
        # Set up directories
        vf_file_path = Path(vf_file)
        vf_file_name = vf_file_path.stem
        
        # Create exports directory and copy the file there if it's not already there
        exports_dir = Path('voiceflow_exports')
        exports_dir.mkdir(exist_ok=True)
        
        # Determine if the file is already in the exports directory
        if not str(vf_file_path).startswith(str(exports_dir)):
            export_file_path = exports_dir / vf_file_path.name
            # Copy the file to the exports directory if it's not already there
            if not export_file_path.exists():
                shutil.copy2(vf_file, export_file_path)
                console.print(f"Copied export file to [bold cyan]{export_file_path}[/bold cyan]")
            vf_file = str(export_file_path)
        
        # Determine output directory
        if output is None:
            projects_dir = Path('voiceflow_projects')
            projects_dir.mkdir(exist_ok=True)
            output = str(projects_dir / vf_file_name)
        
        # Load the export file
        export_data = parser_service.load_export(vf_file)
        
        # Parse the export data
        export = parser_service.parse_export(export_data)
        
        # Generate the project structure
        parser_service.generate_project_structure(export, output)
        
        console.print(f"[bold green]Successfully parsed and generated project in:[/bold green] {output}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise

@cli.command()
@click.argument('vf_file', type=click.Path(exists=True))
@click.option('--output', '-o', default=None, help='Output file for the formatted JSON')
def analyze(vf_file, output):
    """Analyze a Voiceflow export file and display its structure."""
    console.print(f"[bold green]Voiceflow Export Analyzer[/bold green]")
    
    try:
        # Create exports directory and copy the file there if it's not already there
        vf_file_path = Path(vf_file)
        exports_dir = Path('voiceflow_exports')
        exports_dir.mkdir(exist_ok=True)
        
        # Determine if the file is already in the exports directory
        if not str(vf_file_path).startswith(str(exports_dir)):
            export_file_path = exports_dir / vf_file_path.name
            # Copy the file to the exports directory if it's not already there
            if not export_file_path.exists():
                shutil.copy2(vf_file, export_file_path)
                console.print(f"Copied export file to [bold cyan]{export_file_path}[/bold cyan]")
            vf_file = str(export_file_path)
        
        # Create a parser service
        parser_service = VoiceflowParserService(console=console)
        
        # Load the export file
        export_data = parser_service.load_export(vf_file)
        
        # Parse the export data
        export = parser_service.parse_export(export_data)
        
        # Display basic statistics
        console.print("\n[bold]Project Details:[/bold]")
        if export.project and export.project.name:
            console.print(f"Project Name: {export.project.name}")
        
        console.print(f"\n[bold]Diagrams ({len(export.diagrams)}):[/bold]")
        for diagram_id, diagram in export.diagrams.items():
            node_count = len(diagram.nodes) if diagram.nodes else 0
            console.print(f"  - {diagram.name} (ID: {diagram_id}): {node_count} nodes")
        
        console.print(f"\n[bold]Variables ({len(export.variables)}):[/bold]")
        for var in export.variables[:10]:  # Show first 10 variables
            console.print(f"  - {var.name} ({var.type})")
        if len(export.variables) > 10:
            console.print(f"  ... and {len(export.variables) - 10} more")
        
        console.print(f"\n[bold]Intents ({len(export.intents)}):[/bold]")
        for intent in export.intents:
            console.print(f"  - {intent.name}")
        
        # If output file is specified, write the formatted export to it
        if output:
            import json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(export.dict(), f, indent=2)
            console.print(f"\nFormatted export written to: {output}")
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise

@cli.command()
def version():
    """Display the version of the Voiceflow Parser."""
    from importlib.metadata import version as get_version
    try:
        version = get_version("voiceflow_parser")
        console.print(f"Voiceflow Parser v{version}")
    except:
        console.print("Voiceflow Parser (development version)")

if __name__ == '__main__':
    cli()
