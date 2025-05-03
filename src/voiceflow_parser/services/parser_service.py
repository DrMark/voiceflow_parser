"""
Parser service for Voiceflow exports.

This module contains the main logic for parsing Voiceflow exports and generating
the appropriate file structure.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from voiceflow_parser.models.export_model import (
    VoiceflowExport, 
    VoiceflowDiagram, 
    VoiceflowVariable,
    VoiceflowIntent,
    VoiceflowResponse,
    VoiceflowPrompt,
    VoiceflowPromptMessage,
    VoiceflowAgent
)


class VoiceflowParserService:
    """Service for parsing Voiceflow exports and generating file structure."""
    
    def __init__(self, console: Optional[Console] = None):
        """
        Initialize the parser service.
        
        Args:
            console: Rich console for output
        """
        self.console = console or Console()
    
    def load_export(self, file_path: str) -> Dict[str, Any]:
        """
        Load a Voiceflow export file.
        
        Args:
            file_path: Path to the Voiceflow export file
            
        Returns:
            Dictionary containing the parsed Voiceflow export
        """
        self.console.print(f"Loading Voiceflow export from [bold cyan]{file_path}[/bold cyan]")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.console.print(f"[bold green]Successfully loaded export file[/bold green]")
            return data
        except json.JSONDecodeError:
            self.console.print(f"[bold red]Error:[/bold red] The file {file_path} is not a valid JSON file.")
            raise
        except FileNotFoundError:
            self.console.print(f"[bold red]Error:[/bold red] The file {file_path} was not found.")
            raise
    
    def parse_export(self, export_data: Dict[str, Any]) -> VoiceflowExport:
        """
        Parse the Voiceflow export data into a structured model.
        
        Args:
            export_data: Raw Voiceflow export data
            
        Returns:
            Structured VoiceflowExport model
        """
        self.console.print("Parsing Voiceflow export data...")
        export = VoiceflowExport.from_export(export_data)
        
        # Print some basic information about the export
        project_name = export.project.name if export.project else "Unknown Project"
        self.console.print(f"Project: [bold]{project_name}[/bold]")
        self.console.print(f"Diagrams: [bold]{len(export.diagrams)}[/bold]")
        self.console.print(f"Variables: [bold]{len(export.variables)}[/bold]")
        self.console.print(f"Intents: [bold]{len(export.intents)}[/bold]")
        self.console.print(f"Responses: [bold]{len(export.responses)}[/bold]")
        self.console.print(f"Prompts: [bold]{len(export.prompts)}[/bold]")
        self.console.print(f"Prompt Messages: [bold]{len(export.promptMessages)}[/bold]")
        self.console.print(f"Agents: [bold]{len(export.agents)}[/bold]")
        self.console.print(f"Buttons: [bold]{len(export.buttons)}[/bold]")
        self.console.print(f"Captures: [bold]{len(export.captures)}[/bold]")
        self.console.print(f"APIs: [bold]{len(export.apis)}[/bold]")
        self.console.print(f"KB Searches: [bold]{len(export.kbSearches)}[/bold]")
        self.console.print(f"Choices: [bold]{len(export.choices)}[/bold]")
        self.console.print(f"Cards: [bold]{len(export.cards)}[/bold]")
        
        return export
    
    def generate_project_structure(self, export: VoiceflowExport, output_dir: str) -> None:
        """
        Generate the project structure from the parsed Voiceflow export.
        
        Args:
            export: Parsed Voiceflow export
            output_dir: Directory to output the generated files
        """
        output_path = Path(output_dir)
        
        # Create the main output directory
        output_path.mkdir(exist_ok=True, parents=True)
        
        self.console.print(f"Generating project structure in [bold cyan]{output_path}[/bold cyan]")
        
        # Create subdirectories
        (output_path / "diagrams").mkdir(exist_ok=True)
        (output_path / "intents").mkdir(exist_ok=True)
        (output_path / "variables").mkdir(exist_ok=True)
        (output_path / "responses").mkdir(exist_ok=True)
        (output_path / "prompts").mkdir(exist_ok=True)
        (output_path / "agents").mkdir(exist_ok=True)
        (output_path / "buttons").mkdir(exist_ok=True)
        (output_path / "captures").mkdir(exist_ok=True)
        (output_path / "apis").mkdir(exist_ok=True)
        (output_path / "kb_searches").mkdir(exist_ok=True)
        (output_path / "choices").mkdir(exist_ok=True)
        (output_path / "cards").mkdir(exist_ok=True)
        
        # Generate project metadata file
        if export.project:
            self._generate_project_metadata(export, output_path)
        
        # Initialize progress bar
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
        )
        
        # Generate diagrams
        with progress:
            task = progress.add_task("Generating files...", total=12)
            
            self._generate_diagrams(export, output_path)
            progress.update(task, advance=1)
            
            self._generate_variables(export, output_path)
            progress.update(task, advance=1)
            
            self._generate_intents(export, output_path)
            progress.update(task, advance=1)
            
            self._generate_responses(export, output_path)
            progress.update(task, advance=1)
            
            self._generate_prompts(export.prompts, output_path)
            progress.update(task, advance=1)
            
            self._generate_agents(export, output_path)
            progress.update(task, advance=1)
            
            self._generate_buttons(export, output_path)
            progress.update(task, advance=1)
            
            self._generate_captures(export, output_path)
            progress.update(task, advance=1)
            
            self._generate_apis(export, output_path)
            progress.update(task, advance=1)
            
            self._generate_kb_searches(export, output_path)
            progress.update(task, advance=1)
            
            self._generate_choices(export, output_path)
            progress.update(task, advance=1)
            
            self._generate_cards(export, output_path)
            progress.update(task, advance=1)
        
        # Generate README
        self._generate_readme(export, output_path)
        
        self.console.print(f"[bold green]Successfully generated project structure in {output_path}[/bold green]")
    
    def _generate_project_metadata(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate project metadata file."""
        with open(output_path / "project.json", "w", encoding="utf-8") as f:
            json.dump(export.project.dict(), f, indent=2)
        
        self.console.print("Generated project metadata file")
    
    def _generate_diagrams(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate diagram files."""
        diagrams_dir = output_path / "diagrams"
        
        # Save all diagrams to a single file
        with open(diagrams_dir / "diagrams.json", "w", encoding="utf-8") as f:
            json.dump({id: d.dict() for id, d in export.diagrams.items()}, f, indent=2)
        
        # Create individual directories for each diagram
        for diagram_id, diagram in export.diagrams.items():
            diagram_dir = diagrams_dir / self._sanitize_filename(diagram.name)
            diagram_dir.mkdir(exist_ok=True)
            
            # Save diagram metadata
            with open(diagram_dir / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(diagram.dict(exclude={"nodes"}), f, indent=2)
            
            # Create nodes directory
            nodes_dir = diagram_dir / "nodes"
            nodes_dir.mkdir(exist_ok=True)
            
            # Save each node to a separate file
            for node_id, node_data in diagram.nodes.items():
                with open(nodes_dir / f"{node_id}.json", "w", encoding="utf-8") as f:
                    json.dump(node_data, f, indent=2)
        
        self.console.print(f"Generated diagram files ({len(export.diagrams)} diagrams)")
    
    def _generate_variables(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate variable files."""
        variables_dir = output_path / "variables"
        
        # Save all variables to a single file
        with open(variables_dir / "variables.json", "w", encoding="utf-8") as f:
            json.dump([v.dict() for v in export.variables], f, indent=2)
        
        # Create individual files for each variable
        for variable in export.variables:
            with open(variables_dir / f"{self._sanitize_filename(variable.name)}.json", "w", encoding="utf-8") as f:
                json.dump(variable.dict(), f, indent=2)
        
        self.console.print(f"Generated variable files ({len(export.variables)} variables)")
    
    def _generate_intents(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate intent files."""
        intents_dir = output_path / "intents"
        
        # Save all intents to a single file
        with open(intents_dir / "intents.json", "w", encoding="utf-8") as f:
            json.dump([i.dict() for i in export.intents], f, indent=2)
        
        # Create individual files for each intent
        for intent in export.intents:
            with open(intents_dir / f"{self._sanitize_filename(intent.name)}.json", "w", encoding="utf-8") as f:
                json.dump(intent.dict(), f, indent=2)
        
        self.console.print(f"Generated intent files ({len(export.intents)} intents)")
    
    def _generate_responses(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate response files."""
        responses_dir = output_path / "responses"
        
        # Save all responses to a single file
        with open(responses_dir / "responses.json", "w", encoding="utf-8") as f:
            json.dump([r.dict() for r in export.responses], f, indent=2)
        
        # Create individual files for each response
        for response in export.responses:
            response_name = response.name or response.id
            with open(responses_dir / f"{self._sanitize_filename(response_name)}.json", "w", encoding="utf-8") as f:
                json.dump(response.dict(), f, indent=2)
            
            # Create a text file with the response content for easy viewing
            if response.content:
                with open(responses_dir / f"{self._sanitize_filename(response_name)}.txt", "w", encoding="utf-8") as f:
                    f.write(response.content)
        
        self.console.print(f"Generated response files ({len(export.responses)} responses)")
    
    def _generate_prompts(self, prompts: List[VoiceflowPrompt], output_dir: Path) -> None:
        """Generate prompt files."""
        if not prompts:
            return

        # Create prompts directory
        prompts_dir = output_dir / "prompts"
        prompts_dir.mkdir(exist_ok=True)

        # Save prompts.json
        with open(prompts_dir / "prompts.json", "w", encoding="utf-8") as f:
            json.dump([p.dict() for p in prompts], f, indent=2)
            
        # Save a detailed version with all message content extracted
        detailed_prompts = []
        for prompt in prompts:
            detailed_prompt = prompt.dict()
            
            # Convert messages to include extracted content
            detailed_messages = []
            for message in prompt.messages:
                message_dict = message.dict()
                message_dict["extracted_content"] = message.get_content()
                message_dict["extracted_role"] = message.get_role()
                detailed_messages.append(message_dict)
                
            detailed_prompt["detailed_messages"] = detailed_messages
            detailed_prompts.append(detailed_prompt)
            
        with open(prompts_dir / "prompts_detailed.json", "w", encoding="utf-8") as f:
            json.dump(detailed_prompts, f, indent=2)

        # Generate individual prompt directories
        for prompt in prompts:
            prompt_dir = prompts_dir / prompt.name
            prompt_dir.mkdir(exist_ok=True)

            # Save metadata
            with open(prompt_dir / "metadata.json", "w", encoding="utf-8") as f:
                # Include system field in metadata
                metadata = prompt.dict(exclude={"messages"})
                json.dump(metadata, f, indent=2)

            # Debug: Print system prompt info
            print(f"Prompt {prompt.name} (ID: {prompt.id}) system prompt: {'Present' if prompt.system else 'None'}")
            if prompt.system:
                print(f"System prompt length: {len(prompt.system)}")

            # Save system prompt if it exists
            if prompt.system:
                print(f"Saving system prompt for {prompt.name} to {prompt_dir / 'system.txt'}")
                with open(prompt_dir / "system.txt", "w", encoding="utf-8") as f:
                    f.write(prompt.system)

            # Save messages
            if prompt.messages:
                # Debug: Print message info
                print(f"Prompt {prompt.name} has {len(prompt.messages)} messages")
                
                # Save as JSON with all data
                with open(prompt_dir / "messages.json", "w", encoding="utf-8") as f:
                    # Include extracted content in JSON output
                    messages_json = []
                    for msg in prompt.messages:
                        msg_dict = msg.dict()
                        msg_dict["extracted_content"] = msg.get_content()
                        msg_dict["extracted_role"] = msg.get_role()
                        messages_json.append(msg_dict)
                    json.dump(messages_json, f, indent=2)
                
                # Save a simpler version with just role and content for readability
                with open(prompt_dir / "messages.txt", "w", encoding="utf-8") as f:
                    for i, message in enumerate(prompt.messages):
                        role = message.get_role()
                        content = message.get_content()
                        
                        f.write(f"--- Message {i+1} ---\n")
                        if role:
                            f.write(f"Role: {role}\n")
                        if content:
                            f.write(f"Content:\n{content}\n\n")
                        else:
                            f.write("Content: None\n\n")
                
                # Save system and user messages in separate files for easier reference
                system_messages = [msg for msg in prompt.messages if msg.get_role() == "system"]
                user_messages = [msg for msg in prompt.messages if msg.get_role() == "user"]
                assistant_messages = [msg for msg in prompt.messages if msg.get_role() == "assistant"]
                
                if system_messages:
                    with open(prompt_dir / "system_messages.txt", "w", encoding="utf-8") as f:
                        for i, msg in enumerate(system_messages):
                            content = msg.get_content()
                            if content:
                                f.write(f"System Message {i+1}:\n{content}\n\n")
                
                if user_messages:
                    with open(prompt_dir / "user_messages.txt", "w", encoding="utf-8") as f:
                        for i, msg in enumerate(user_messages):
                            content = msg.get_content()
                            if content:
                                f.write(f"User Message {i+1}:\n{content}\n\n")
                
                if assistant_messages:
                    with open(prompt_dir / "assistant_messages.txt", "w", encoding="utf-8") as f:
                        for i, msg in enumerate(assistant_messages):
                            content = msg.get_content()
                            if content:
                                f.write(f"Assistant Message {i+1}:\n{content}\n\n")
                
                # Create a complete prompt file that includes system prompt and all messages
                with open(prompt_dir / "complete_prompt.txt", "w", encoding="utf-8") as f:
                    f.write(f"Prompt: {prompt.name}\n")
                    f.write(f"ID: {prompt.id}\n")
                    if prompt.description:
                        f.write(f"Description: {prompt.description}\n")
                    f.write("\n")
                    
                    # Include system prompt first
                    if prompt.system:
                        f.write("SYSTEM PROMPT:\n")
                        f.write(f"{prompt.system}\n\n")
                    
                    # Then include all messages in order
                    f.write("MESSAGES:\n\n")
                    for i, message in enumerate(prompt.messages):
                        role = message.get_role()
                        content = message.get_content()
                        
                        f.write(f"--- Message {i+1} ---\n")
                        if role:
                            f.write(f"Role: {role}\n")
                        if content:
                            f.write(f"Content:\n{content}\n\n")
                        else:
                            f.write("Content: None\n\n")

        self.console.print(f"Generated prompt files ({len(prompts)} prompts)")
    
    def _generate_agents(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate agent files."""
        agents_dir = output_path / "agents"
        
        # Save all agents to a single file
        with open(agents_dir / "agents.json", "w", encoding="utf-8") as f:
            json.dump([a.dict() for a in export.agents], f, indent=2)
        
        # Create individual files for each agent
        for agent in export.agents:
            agent_dir = agents_dir / self._sanitize_filename(agent.name)
            agent_dir.mkdir(exist_ok=True)
            
            # Save agent metadata
            with open(agent_dir / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(agent.dict(), f, indent=2)
            
            # Create a text file with the agent instructions for easy viewing
            with open(agent_dir / "instructions.txt", "w", encoding="utf-8") as f:
                f.write(f"Agent: {agent.name}\n")
                if agent.description:
                    f.write(f"Description: {agent.description}\n")
                f.write("\nInstructions:\n")
                
                instruction_texts = agent.get_instruction_texts()
                for i, instruction in enumerate(instruction_texts):
                    f.write(f"\n--- Instruction {i+1} ---\n")
                    f.write(f"{instruction}\n")
        
        self.console.print(f"Generated agent files ({len(export.agents)} agents)")
    
    def _generate_buttons(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate button component files."""
        buttons_dir = output_path / "buttons"
        
        # Save all buttons to a single file
        with open(buttons_dir / "buttons.json", "w", encoding="utf-8") as f:
            json.dump([b.dict() for b in export.buttons], f, indent=2)
        
        # Create individual files for each button component
        for button in export.buttons:
            button_name = button.name or button.id
            with open(buttons_dir / f"{self._sanitize_filename(button_name)}.json", "w", encoding="utf-8") as f:
                json.dump(button.dict(), f, indent=2)
            
            # Create a text file with the button information for easy viewing
            with open(buttons_dir / f"{self._sanitize_filename(button_name)}.txt", "w", encoding="utf-8") as f:
                f.write(f"Button Component: {button_name}\n\n")
                f.write("Buttons:\n")
                for i, btn in enumerate(button.buttons):
                    f.write(f"  {i+1}. {btn.get('name', 'Unnamed Button')}\n")
                    if 'request' in btn:
                        f.write(f"     Value: {btn.get('request', '')}\n")
        
        self.console.print(f"Generated button files ({len(export.buttons)} button components)")
    
    def _generate_captures(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate capture component files."""
        captures_dir = output_path / "captures"
        
        # Save all captures to a single file
        with open(captures_dir / "captures.json", "w", encoding="utf-8") as f:
            json.dump([c.dict() for c in export.captures], f, indent=2)
        
        # Create individual files for each capture component
        for capture in export.captures:
            capture_name = capture.name or capture.id
            with open(captures_dir / f"{self._sanitize_filename(capture_name)}.json", "w", encoding="utf-8") as f:
                json.dump(capture.dict(), f, indent=2)
            
            # Create a text file with the capture information for easy viewing
            with open(captures_dir / f"{self._sanitize_filename(capture_name)}.txt", "w", encoding="utf-8") as f:
                f.write(f"Capture Component: {capture_name}\n\n")
                if capture.variable:
                    f.write(f"Variable: {capture.variable}\n")
                if capture.intent:
                    f.write(f"Intent: {capture.intent.get('name', '')}\n")
        
        self.console.print(f"Generated capture files ({len(export.captures)} capture components)")
    
    def _generate_apis(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate API component files."""
        apis_dir = output_path / "apis"
        
        # Save all APIs to a single file
        with open(apis_dir / "apis.json", "w", encoding="utf-8") as f:
            json.dump([a.dict() for a in export.apis], f, indent=2)
        
        # Create individual files for each API component
        for api in export.apis:
            api_name = api.name or api.id
            with open(apis_dir / f"{self._sanitize_filename(api_name)}.json", "w", encoding="utf-8") as f:
                json.dump(api.dict(), f, indent=2)
            
            # Create a text file with the API information for easy viewing
            with open(apis_dir / f"{self._sanitize_filename(api_name)}.txt", "w", encoding="utf-8") as f:
                f.write(f"API Component: {api_name}\n\n")
                if api.url:
                    f.write(f"URL: {api.url}\n")
                f.write(f"Method: {api.method}\n")
                if api.headers:
                    f.write("\nHeaders:\n")
                    for key, value in api.headers.items():
                        f.write(f"  {key}: {value}\n")
                if api.params:
                    f.write("\nParameters:\n")
                    for key, value in api.params.items():
                        f.write(f"  {key}: {value}\n")
        
        self.console.print(f"Generated API files ({len(export.apis)} API components)")
    
    def _generate_kb_searches(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate knowledge base search component files."""
        kb_searches_dir = output_path / "kb_searches"
        
        # Save all KB searches to a single file
        with open(kb_searches_dir / "kb_searches.json", "w", encoding="utf-8") as f:
            json.dump([k.dict() for k in export.kbSearches], f, indent=2)
        
        # Create individual files for each KB search component
        for kb_search in export.kbSearches:
            kb_name = kb_search.name or kb_search.id
            with open(kb_searches_dir / f"{self._sanitize_filename(kb_name)}.json", "w", encoding="utf-8") as f:
                json.dump(kb_search.dict(), f, indent=2)
            
            # Create a text file with the KB search information for easy viewing
            with open(kb_searches_dir / f"{self._sanitize_filename(kb_name)}.txt", "w", encoding="utf-8") as f:
                f.write(f"Knowledge Base Search Component: {kb_name}\n\n")
                if kb_search.query:
                    f.write(f"Query: {kb_search.query}\n")
        
        self.console.print(f"Generated KB search files ({len(export.kbSearches)} KB search components)")
    
    def _generate_choices(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate choice component files."""
        choices_dir = output_path / "choices"
        
        # Save all choices to a single file
        with open(choices_dir / "choices.json", "w", encoding="utf-8") as f:
            json.dump([c.dict() for c in export.choices], f, indent=2)
        
        # Create individual files for each choice component
        for choice in export.choices:
            choice_name = choice.name or choice.id
            with open(choices_dir / f"{self._sanitize_filename(choice_name)}.json", "w", encoding="utf-8") as f:
                json.dump(choice.dict(), f, indent=2)
            
            # Create a text file with the choice information for easy viewing
            with open(choices_dir / f"{self._sanitize_filename(choice_name)}.txt", "w", encoding="utf-8") as f:
                f.write(f"Choice Component: {choice_name}\n\n")
                f.write("Choices:\n")
                for i, ch in enumerate(choice.choices):
                    f.write(f"  {i+1}. {ch.get('name', 'Unnamed Choice')}\n")
        
        self.console.print(f"Generated choice files ({len(export.choices)} choice components)")
    
    def _generate_cards(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate card component files."""
        cards_dir = output_path / "cards"
        
        # Save all cards to a single file
        with open(cards_dir / "cards.json", "w", encoding="utf-8") as f:
            json.dump([c.dict() for c in export.cards], f, indent=2)
        
        # Create individual files for each card component
        for card in export.cards:
            card_name = card.name or card.id
            with open(cards_dir / f"{self._sanitize_filename(card_name)}.json", "w", encoding="utf-8") as f:
                json.dump(card.dict(), f, indent=2)
            
            # Create a text file with the card information for easy viewing
            with open(cards_dir / f"{self._sanitize_filename(card_name)}.txt", "w", encoding="utf-8") as f:
                f.write(f"Card Component: {card_name}\n\n")
                if card.title:
                    f.write(f"Title: {card.title}\n")
                if card.description:
                    f.write(f"Description: {card.description}\n")
                if card.imageUrl:
                    f.write(f"Image URL: {card.imageUrl}\n")
                if card.buttons:
                    f.write("\nButtons:\n")
                    for i, btn in enumerate(card.buttons):
                        f.write(f"  {i+1}. {btn.get('name', 'Unnamed Button')}\n")
        
        self.console.print(f"Generated card files ({len(export.cards)} card components)")
    
    def _generate_readme(self, export: VoiceflowExport, output_path: Path) -> None:
        """Generate a README file with project information."""
        project_name = export.project.name if export.project else "Voiceflow Project"
        
        with open(output_path / "README.md", "w", encoding="utf-8") as f:
            f.write(f"# {project_name}\n\n")
            f.write("This project was generated from a Voiceflow export using the Voiceflow Parser tool.\n\n")
            
            f.write("## Project Structure\n\n")
            f.write("- **diagrams/**: Contains the flow diagrams from the Voiceflow project\n")
            f.write("- **intents/**: Contains the intents defined in the project\n")
            f.write("- **variables/**: Contains the variables used in the project\n")
            f.write("- **responses/**: Contains the responses defined in the project\n")
            f.write("- **prompts/**: Contains the prompts used for LLM interactions\n")
            f.write("- **agents/**: Contains the agent configurations\n")
            f.write("- **buttons/**: Contains button components\n")
            f.write("- **captures/**: Contains capture components\n")
            f.write("- **apis/**: Contains API components\n")
            f.write("- **kb_searches/**: Contains knowledge base search components\n")
            f.write("- **choices/**: Contains choice components\n")
            f.write("- **cards/**: Contains card components\n")
            
            f.write("\n## Statistics\n\n")
            f.write(f"- Diagrams: {len(export.diagrams)}\n")
            f.write(f"- Variables: {len(export.variables)}\n")
            f.write(f"- Intents: {len(export.intents)}\n")
            f.write(f"- Responses: {len(export.responses)}\n")
            f.write(f"- Prompts: {len(export.prompts)}\n")
            f.write(f"- Prompt Messages: {len(export.promptMessages)}\n")
            f.write(f"- Agents: {len(export.agents)}\n")
            f.write(f"- Buttons: {len(export.buttons)}\n")
            f.write(f"- Captures: {len(export.captures)}\n")
            f.write(f"- APIs: {len(export.apis)}\n")
            f.write(f"- KB Searches: {len(export.kbSearches)}\n")
            f.write(f"- Choices: {len(export.choices)}\n")
            f.write(f"- Cards: {len(export.cards)}\n")
        
        self.console.print("Generated README file")
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """
        Sanitize a string to be used as a filename.
        
        Args:
            filename: The string to sanitize
            
        Returns:
            A sanitized string that can be used as a filename
        """
        # Replace invalid characters with underscores
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit the length to avoid issues with long filenames
        if len(filename) > 100:
            filename = filename[:97] + "..."
        
        # Ensure the filename is not empty
        if not filename or filename.isspace():
            filename = "unnamed"
        
        return filename
