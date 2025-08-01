"""
NiFi NL Builder - Natural Language to Apache NiFi Flow Generator

A CrewAI-powered system that converts natural language descriptions
into Apache NiFi flows using specialized agents.
"""

from .crew import NiFiNLCrew

__version__ = "0.1.0"
__author__ = "NiFi NL Builder Team"

__all__ = [
    'NiFiNLCrew'
] 