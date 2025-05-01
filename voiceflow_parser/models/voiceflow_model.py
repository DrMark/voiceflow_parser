"""
Models for Voiceflow export data structures.

This module defines Pydantic models that represent the structure of a Voiceflow export.
"""
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class VoiceflowNode(BaseModel):
    """Base model for a Voiceflow node."""
    id: str
    type: str
    data: Dict[str, Any] = Field(default_factory=dict)
    coords: Optional[Dict[str, float]] = None


class VoiceflowStep(BaseModel):
    """Model for a Voiceflow step."""
    nodeID: str
    type: str
    data: Dict[str, Any] = Field(default_factory=dict)


class VoiceflowDiagram(BaseModel):
    """Model for a Voiceflow diagram."""
    id: str
    name: str
    nodes: List[VoiceflowNode] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)
    steps: List[VoiceflowStep] = Field(default_factory=list)


class VoiceflowProject(BaseModel):
    """Model for a complete Voiceflow project."""
    name: str
    version: Optional[str] = None
    diagrams: Dict[str, VoiceflowDiagram] = Field(default_factory=dict)
    variables: Dict[str, Any] = Field(default_factory=dict)
    intents: List[Dict[str, Any]] = Field(default_factory=list)
    slots: List[Dict[str, Any]] = Field(default_factory=list)
    settings: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_export(cls, export_data: Dict[str, Any]) -> "VoiceflowProject":
        """
        Create a VoiceflowProject from raw export data.
        
        Args:
            export_data: The raw Voiceflow export data
            
        Returns:
            A VoiceflowProject instance
        """
        # Extract diagrams from the export data
        diagrams = {}
        for diagram_id, diagram_data in export_data.get("diagrams", {}).items():
            diagrams[diagram_id] = VoiceflowDiagram(
                id=diagram_id,
                name=diagram_data.get("name", ""),
                nodes=diagram_data.get("nodes", []),
                variables=diagram_data.get("variables", {}),
                steps=diagram_data.get("steps", [])
            )
        
        return cls(
            name=export_data.get("name", "Unknown Project"),
            version=export_data.get("version"),
            diagrams=diagrams,
            variables=export_data.get("variables", {}),
            intents=export_data.get("intents", []),
            slots=export_data.get("slots", []),
            settings=export_data.get("settings")
        )
