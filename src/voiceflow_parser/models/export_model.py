"""
Models for Voiceflow export data structures.

This module defines Pydantic models that represent the structure of a Voiceflow export.
"""
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, root_validator


class VoiceflowNode(BaseModel):
    """Base model for a Voiceflow node."""
    id: str
    type: str
    data: Dict[str, Any] = Field(default_factory=dict)
    coords: Optional[Dict[str, float]] = None


class VoiceflowDiagram(BaseModel):
    """Model for a Voiceflow diagram."""
    id: str
    name: str
    type: Optional[str] = None
    nodes: Dict[str, Any] = Field(default_factory=dict)
    variables: List[Any] = Field(default_factory=list)
    modified: Optional[int] = None
    versionID: Optional[str] = None
    offsetX: Optional[float] = None
    offsetY: Optional[float] = None
    zoom: Optional[float] = None


class VoiceflowIntent(BaseModel):
    """Model for a Voiceflow intent."""
    name: str
    id: Optional[str] = None
    slots: List[Any] = Field(default_factory=list)
    inputs: List[str] = Field(default_factory=list)


class VoiceflowVariable(BaseModel):
    """Model for a Voiceflow variable."""
    name: str
    type: str
    value: Optional[Any] = None
    id: Optional[str] = None


class VoiceflowResponse(BaseModel):
    """Model for a Voiceflow response."""
    id: str
    name: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None


class VoiceflowPromptMessage(BaseModel):
    """Representation of a prompt message."""
    id: str
    promptID: str
    content: Optional[str] = None  # Simple content (legacy format)
    role: Optional[str] = None  # Role (user, system, assistant)
    type: str = "text"  # Type of message (text, role, etc.)
    data: Optional[Dict[str, Any]] = None  # Complex data with nested content
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    
    def get_content(self) -> Optional[str]:
        """Extract content from either simple content or nested data structure."""
        if self.content:
            return self.content
        
        if self.data and "content" in self.data:
            # Extract content from nested structure
            content_parts = []
            for content_item in self.data["content"]:
                if "text" in content_item and isinstance(content_item["text"], list):
                    for text_part in content_item["text"]:
                        if isinstance(text_part, str):
                            content_parts.append(text_part)
                        elif isinstance(text_part, dict) and "variableID" in text_part:
                            # Handle variable placeholders
                            content_parts.append(f"{{{{ {text_part['variableID']} }}}}")
            
            if content_parts:
                return "".join(content_parts)
        
        return None
    
    def get_role(self) -> Optional[str]:
        """Extract role from either direct role field or nested data structure."""
        if self.role:
            return self.role
        
        if self.data and "role" in self.data:
            return self.data["role"]
        
        return None


class VoiceflowPrompt(BaseModel):
    """Model for a Voiceflow prompt."""
    id: str
    name: str
    description: Optional[str] = None
    messageOrder: List[str] = Field(default_factory=list)
    settings: Dict[str, Any] = Field(default_factory=dict)
    folderID: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    messages: List[VoiceflowPromptMessage] = Field(default_factory=list)
    system: Optional[str] = None


class VoiceflowAgentInstruction(BaseModel):
    """Model for a Voiceflow agent instruction."""
    text: Union[str, List[Any], Dict[str, Any]] = ""
    
    def get_text(self) -> str:
        """Extract text from the instruction."""
        if isinstance(self.text, str):
            return self.text
        elif isinstance(self.text, list):
            if all(isinstance(item, str) for item in self.text):
                return " ".join(self.text)
            else:
                # Handle nested structures
                result = []
                for item in self.text:
                    if isinstance(item, dict) and 'text' in item:
                        if isinstance(item['text'], list):
                            for subitem in item['text']:
                                if isinstance(subitem, str):
                                    result.append(subitem)
                        elif isinstance(subitem, str):
                            result.append(item['text'])
                return " ".join(result)
        elif isinstance(self.text, dict) and 'text' in self.text:
            if isinstance(self.text['text'], list):
                return " ".join(self.text['text'])
            return str(self.text['text'])
        return str(self.text)


class VoiceflowAgent(BaseModel):
    """Model for a Voiceflow agent."""
    id: str
    name: str
    description: Optional[str] = None
    instructions: List[Any] = Field(default_factory=list)
    settings: Dict[str, Any] = Field(default_factory=dict)
    knowledgeBaseTool: Optional[Dict[str, Any]] = None
    webSearchTool: Optional[Dict[str, Any]] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    
    def get_instruction_texts(self) -> List[str]:
        """Extract text from the instructions."""
        result = []
        for instruction in self.instructions:
            if isinstance(instruction, VoiceflowAgentInstruction):
                result.append(instruction.get_text())
            elif isinstance(instruction, dict) and 'text' in instruction:
                instr = VoiceflowAgentInstruction(text=instruction['text'])
                result.append(instr.get_text())
            elif isinstance(instruction, str):
                result.append(instruction)
            else:
                result.append(str(instruction))
        return result


class VoiceflowButton(BaseModel):
    """Model for a Voiceflow button component."""
    id: str
    name: Optional[str] = None
    buttons: List[Dict[str, Any]] = Field(default_factory=list)
    settings: Dict[str, Any] = Field(default_factory=dict)
    diagramID: Optional[str] = None
    nodeID: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class VoiceflowCapture(BaseModel):
    """Model for a Voiceflow capture component."""
    id: str
    name: Optional[str] = None
    variable: Optional[str] = None
    intent: Optional[Dict[str, Any]] = None
    settings: Dict[str, Any] = Field(default_factory=dict)
    diagramID: Optional[str] = None
    nodeID: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class VoiceflowAPI(BaseModel):
    """Model for a Voiceflow API component."""
    id: str
    name: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = "GET"
    headers: Dict[str, Any] = Field(default_factory=dict)
    params: Dict[str, Any] = Field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None
    settings: Dict[str, Any] = Field(default_factory=dict)
    diagramID: Optional[str] = None
    nodeID: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class VoiceflowKnowledgeBaseSearch(BaseModel):
    """Model for a Voiceflow knowledge base search component."""
    id: str
    name: Optional[str] = None
    query: Optional[str] = None
    settings: Dict[str, Any] = Field(default_factory=dict)
    diagramID: Optional[str] = None
    nodeID: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class VoiceflowChoice(BaseModel):
    """Model for a Voiceflow choice component."""
    id: str
    name: Optional[str] = None
    choices: List[Dict[str, Any]] = Field(default_factory=list)
    settings: Dict[str, Any] = Field(default_factory=dict)
    diagramID: Optional[str] = None
    nodeID: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class VoiceflowCard(BaseModel):
    """Model for a Voiceflow card component."""
    id: str
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    buttons: List[Dict[str, Any]] = Field(default_factory=list)
    settings: Dict[str, Any] = Field(default_factory=dict)
    diagramID: Optional[str] = None
    nodeID: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class VoiceflowProject(BaseModel):
    """Model for the Voiceflow project metadata."""
    name: Optional[str] = None
    teamID: Optional[str] = None
    projectID: Optional[str] = None
    creatorID: Optional[int] = None
    platform: Optional[str] = None
    updatedAt: Optional[str] = None
    createdAt: Optional[str] = None


class VoiceflowExport(BaseModel):
    """Model for a complete Voiceflow export."""
    _version: Optional[str] = None
    project: Optional[VoiceflowProject] = None
    diagrams: Dict[str, VoiceflowDiagram] = Field(default_factory=dict)
    variables: List[VoiceflowVariable] = Field(default_factory=list)
    intents: List[VoiceflowIntent] = Field(default_factory=list)
    responses: List[VoiceflowResponse] = Field(default_factory=list)
    prompts: List[VoiceflowPrompt] = Field(default_factory=list)
    promptMessages: List[VoiceflowPromptMessage] = Field(default_factory=list)
    agents: List[VoiceflowAgent] = Field(default_factory=list)
    buttons: List[VoiceflowButton] = Field(default_factory=list)
    captures: List[VoiceflowCapture] = Field(default_factory=list)
    apis: List[VoiceflowAPI] = Field(default_factory=list)
    kbSearches: List[VoiceflowKnowledgeBaseSearch] = Field(default_factory=list)
    choices: List[VoiceflowChoice] = Field(default_factory=list)
    cards: List[VoiceflowCard] = Field(default_factory=list)
    
    @classmethod
    def from_export(cls, export_data: Dict[str, Any]) -> 'VoiceflowExport':
        """
        Create a VoiceflowExport from raw export data.
        
        Args:
            export_data: The raw Voiceflow export data
            
        Returns:
            A VoiceflowExport instance
        """
        # Process project metadata
        project = None
        if "project" in export_data and isinstance(export_data["project"], dict):
            project = VoiceflowProject(**export_data["project"])
        
        # Process diagrams
        diagrams = {}
        for diagram_id, diagram_data in export_data.get("diagrams", {}).items():
            if isinstance(diagram_data, dict):
                diagrams[diagram_id] = VoiceflowDiagram(
                    id=diagram_id,
                    name=diagram_data.get("name", ""),
                    type=diagram_data.get("type"),
                    nodes=diagram_data.get("nodes", {}),
                    variables=diagram_data.get("variables", []),
                    modified=diagram_data.get("modified"),
                    versionID=diagram_data.get("versionID"),
                    offsetX=diagram_data.get("offsetX"),
                    offsetY=diagram_data.get("offsetY"),
                    zoom=diagram_data.get("zoom")
                )
        
        # Process variables
        variables = []
        for var_data in export_data.get("variables", []):
            if isinstance(var_data, dict):
                variables.append(VoiceflowVariable(
                    name=var_data.get("name", ""),
                    type=var_data.get("type", ""),
                    value=var_data.get("value"),
                    id=var_data.get("id")
                ))
        
        # Process intents
        intents = []
        for intent_data in export_data.get("intents", []):
            if isinstance(intent_data, dict):
                intents.append(VoiceflowIntent(
                    name=intent_data.get("name", ""),
                    id=intent_data.get("id"),
                    slots=intent_data.get("slots", []),
                    inputs=intent_data.get("inputs", [])
                ))
        
        # Process responses
        responses = []
        for response_data in export_data.get("responses", []):
            if isinstance(response_data, dict):
                responses.append(VoiceflowResponse(
                    id=response_data.get("id", ""),
                    name=response_data.get("name"),
                    content=response_data.get("content"),
                    type=response_data.get("type")
                ))
        
        # Process programResources first to extract system prompts and messages
        program_resources_prompts = {}
        if "programResources" in export_data and isinstance(export_data["programResources"], dict):
            program_resources = export_data["programResources"]
            
            # Extract prompts from programResources
            if "prompts" in program_resources and isinstance(program_resources["prompts"], dict):
                print(f"Found {len(program_resources['prompts'])} prompts in programResources")
                program_resources_prompts = program_resources["prompts"]
        
        # Process prompts
        prompts = []
        prompt_ids_map = {}  # Map to store prompt IDs for later lookup
        
        for prompt_data in export_data.get("prompts", {}):
            if isinstance(prompt_data, dict):
                # Extract prompt ID for reference
                prompt_id = prompt_data.get("id", "")
                prompt_ids_map[prompt_id] = len(prompts)  # Store the index in the prompts list
                
                # Check if this prompt has additional data in programResources
                system_prompt = None
                if prompt_id in program_resources_prompts:
                    resource_data = program_resources_prompts[prompt_id]
                    if isinstance(resource_data, dict) and "system" in resource_data:
                        system_prompt = resource_data["system"]
                        print(f"Found system prompt for {prompt_id} in programResources, length: {len(system_prompt) if system_prompt else 0}")
                
                # Create basic prompt structure
                prompts.append(VoiceflowPrompt(
                    id=prompt_id,
                    name=prompt_data.get("name", ""),
                    description=prompt_data.get("description"),
                    messageOrder=prompt_data.get("messageOrder", []),
                    settings=prompt_data.get("settings", {}),
                    folderID=prompt_data.get("folderID"),
                    createdAt=prompt_data.get("createdAt"),
                    updatedAt=prompt_data.get("updatedAt"),
                    system=system_prompt,  # Set from programResources
                    messages=[]   # Will be populated from promptMessages or programResources
                ))
        
        # Process prompt messages from the top-level promptMessages array
        prompt_messages = []
        for message_data in export_data.get("promptMessages", []):
            if isinstance(message_data, dict):
                # Create the message object with the full data structure
                message = VoiceflowPromptMessage(
                    id=message_data.get("id", ""),
                    promptID=message_data.get("promptID", ""),
                    content=message_data.get("content"),
                    type=message_data.get("type", "text"),
                    role=message_data.get("role", "user"),
                    data=message_data.get("data"),
                    createdAt=message_data.get("createdAt"),
                    updatedAt=message_data.get("updatedAt")
                )
                
                # Extract system prompt from message if it's a system message
                if message.get_role() == "system" and message.promptID:
                    prompt_idx = prompt_ids_map.get(message.promptID)
                    if prompt_idx is not None:
                        content = message.get_content()
                        if content and not prompts[prompt_idx].system:
                            print(f"Found system prompt in promptMessages for {message.promptID}, length: {len(content)}")
                            prompts[prompt_idx].system = content
                
                prompt_messages.append(message)
        
        # Process programResources.prompts to extract messages
        for prompt_id, prompt_resource in program_resources_prompts.items():
            if isinstance(prompt_resource, dict) and "messages" in prompt_resource:
                # Find the corresponding prompt in our prompts list
                prompt_index = prompt_ids_map.get(prompt_id)
                
                if prompt_index is not None:
                    prompt = prompts[prompt_index]
                    
                    # Process embedded messages
                    if isinstance(prompt_resource["messages"], list):
                        for msg in prompt_resource["messages"]:
                            if isinstance(msg, dict):
                                msg_id = msg.get("id", f"{prompt_id}_resource_{len(prompt.messages)}")
                                
                                message = VoiceflowPromptMessage(
                                    id=msg_id,
                                    promptID=prompt_id,
                                    content=msg.get("content"),
                                    type=msg.get("type", "text"),
                                    role=msg.get("role", "user"),
                                    data=msg.get("data"),
                                    createdAt=prompt.createdAt,
                                    updatedAt=prompt.updatedAt
                                )
                                
                                role = message.get_role()
                                content = message.get_content()
                                
                                print(f"Adding message to prompt {prompt_id}, role: {role}, content length: {len(content) if content else 0}")
                                
                                if role == "system" and content and not prompt.system:
                                    print(f"Using message as system prompt for {prompt_id}")
                                    prompt.system = content
                                
                                prompt.messages.append(message)
                else:
                    # This is a prompt that only exists in programResources
                    print(f"Found prompt {prompt_id} only in programResources")
                    
                    # Get the system prompt if it exists
                    system_prompt = None
                    if "system" in prompt_resource:
                        system_prompt = prompt_resource["system"]
                        print(f"Found system prompt for {prompt_id} (new prompt), length: {len(system_prompt) if system_prompt else 0}")
                    
                    new_prompt = VoiceflowPrompt(
                        id=prompt_id,
                        name=prompt_id,  # Use ID as name since we don't have a proper name
                        description=None,
                        messageOrder=[],
                        settings=prompt_resource.get("settings", {}),
                        folderID=None,
                        createdAt=None,
                        updatedAt=None,
                        system=system_prompt,
                        messages=[]
                    )
                    
                    # Process embedded messages
                    if "messages" in prompt_resource and isinstance(prompt_resource["messages"], list):
                        for msg in prompt_resource["messages"]:
                            if isinstance(msg, dict):
                                msg_id = msg.get("id", f"{prompt_id}_resource_{len(new_prompt.messages)}")
                                
                                message = VoiceflowPromptMessage(
                                    id=msg_id,
                                    promptID=prompt_id,
                                    content=msg.get("content"),
                                    type=msg.get("type", "text"),
                                    role=msg.get("role", "user"),
                                    data=msg.get("data"),
                                    createdAt=None,
                                    updatedAt=None
                                )
                                
                                # Check if this message is a system prompt
                                role = message.get_role()
                                content = message.get_content()
                                
                                if role == "system" and content and not new_prompt.system:
                                    print(f"Using message as system prompt for new prompt {prompt_id}")
                                    new_prompt.system = content
                                
                                new_prompt.messages.append(message)
                    
                    prompts.append(new_prompt)
        
        # Link prompt messages to their prompts if they're not already embedded
        for prompt in prompts:
            # Only add messages from the promptMessages array if the prompt doesn't already have embedded messages
            if not prompt.messages:
                for msg in prompt_messages:
                    if msg.promptID == prompt.id:
                        prompt.messages.append(msg)
                        
                        # Check if this message is a system prompt
                        role = msg.get_role()
                        content = msg.get_content()
                        
                        if role == "system" and content and not prompt.system:
                            print(f"Using message from promptMessages as system prompt for {prompt.id}")
                            prompt.system = content
        
        # Process agents
        agents = []
        for agent_data in export_data.get("agents", []):
            if isinstance(agent_data, dict):
                instructions = []
                for instruction in agent_data.get("instructions", []):
                    if isinstance(instruction, dict) and 'text' in instruction:
                        instructions.append(VoiceflowAgentInstruction(text=instruction['text']))
                    else:
                        instructions.append(instruction)
                agents.append(VoiceflowAgent(
                    id=agent_data.get("id", ""),
                    name=agent_data.get("name", ""),
                    description=agent_data.get("description"),
                    instructions=instructions,
                    settings=agent_data.get("settings", {}),
                    knowledgeBaseTool=agent_data.get("knowledgeBaseTool"),
                    webSearchTool=agent_data.get("webSearchTool"),
                    createdAt=agent_data.get("createdAt"),
                    updatedAt=agent_data.get("updatedAt")
                ))
        
        # Process buttons
        buttons = []
        for button_data in export_data.get("buttons", []):
            if isinstance(button_data, dict):
                buttons.append(VoiceflowButton(
                    id=button_data.get("id", ""),
                    name=button_data.get("name"),
                    buttons=button_data.get("buttons", []),
                    settings=button_data.get("settings", {}),
                    diagramID=button_data.get("diagramID"),
                    nodeID=button_data.get("nodeID"),
                    createdAt=button_data.get("createdAt"),
                    updatedAt=button_data.get("updatedAt")
                ))
        
        # Process captures
        captures = []
        for capture_data in export_data.get("captures", []):
            if isinstance(capture_data, dict):
                captures.append(VoiceflowCapture(
                    id=capture_data.get("id", ""),
                    name=capture_data.get("name"),
                    variable=capture_data.get("variable"),
                    intent=capture_data.get("intent"),
                    settings=capture_data.get("settings", {}),
                    diagramID=capture_data.get("diagramID"),
                    nodeID=capture_data.get("nodeID"),
                    createdAt=capture_data.get("createdAt"),
                    updatedAt=capture_data.get("updatedAt")
                ))
        
        # Process APIs
        apis = []
        for api_data in export_data.get("apis", []):
            if isinstance(api_data, dict):
                apis.append(VoiceflowAPI(
                    id=api_data.get("id", ""),
                    name=api_data.get("name"),
                    url=api_data.get("url"),
                    method=api_data.get("method", "GET"),
                    headers=api_data.get("headers", {}),
                    params=api_data.get("params", {}),
                    body=api_data.get("body"),
                    settings=api_data.get("settings", {}),
                    diagramID=api_data.get("diagramID"),
                    nodeID=api_data.get("nodeID"),
                    createdAt=api_data.get("createdAt"),
                    updatedAt=api_data.get("updatedAt")
                ))
        
        # Process KB searches
        kb_searches = []
        for kb_data in export_data.get("kbSearches", []):
            if isinstance(kb_data, dict):
                kb_searches.append(VoiceflowKnowledgeBaseSearch(
                    id=kb_data.get("id", ""),
                    name=kb_data.get("name"),
                    query=kb_data.get("query"),
                    settings=kb_data.get("settings", {}),
                    diagramID=kb_data.get("diagramID"),
                    nodeID=kb_data.get("nodeID"),
                    createdAt=kb_data.get("createdAt"),
                    updatedAt=kb_data.get("updatedAt")
                ))
        
        # Process choices
        choices = []
        for choice_data in export_data.get("choices", []):
            if isinstance(choice_data, dict):
                choices.append(VoiceflowChoice(
                    id=choice_data.get("id", ""),
                    name=choice_data.get("name"),
                    choices=choice_data.get("choices", []),
                    settings=choice_data.get("settings", {}),
                    diagramID=choice_data.get("diagramID"),
                    nodeID=choice_data.get("nodeID"),
                    createdAt=choice_data.get("createdAt"),
                    updatedAt=choice_data.get("updatedAt")
                ))
        
        # Process cards
        cards = []
        for card_data in export_data.get("cards", []):
            if isinstance(card_data, dict):
                cards.append(VoiceflowCard(
                    id=card_data.get("id", ""),
                    name=card_data.get("name"),
                    title=card_data.get("title"),
                    description=card_data.get("description"),
                    imageUrl=card_data.get("imageUrl"),
                    buttons=card_data.get("buttons", []),
                    settings=card_data.get("settings", {}),
                    diagramID=card_data.get("diagramID"),
                    nodeID=card_data.get("nodeID"),
                    createdAt=card_data.get("createdAt"),
                    updatedAt=card_data.get("updatedAt")
                ))
        
        return cls(
            _version=export_data.get("_version"),
            project=project,
            diagrams=diagrams,
            variables=variables,
            intents=intents,
            responses=responses,
            prompts=prompts,
            promptMessages=prompt_messages,
            agents=agents,
            buttons=buttons,
            captures=captures,
            apis=apis,
            kbSearches=kb_searches,
            choices=choices,
            cards=cards
        )
