"""Define the configurable parameters for the agent."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Optional

from langchain_core.runnables import RunnableConfig


@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    # Changeme: Add configurable values here!
    # these values can be pre-set when you
    # create assistants (https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/)
    # and when you invoke the graph
    my_configurable_param: str = "changeme"
    model_name: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    system_message: str = """You are a helpful AI assistant with access to a user database. 
    The database contains user information including firstname, surname, and email address.
    When asked about user information, provide the information in a clear format."""

    # Database related prompts
    database_system_message: str = """You are a helpful AI assistant with access to a user database. 
    The database contains user information including firstname, surname, and email address.
    When asked about user information, query the database and provide the information in a clear format.
    If you need to write SQL queries, make sure they are safe and only SELECT from the users table."""

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        configurable = (config.get("configurable") or {}) if config else {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})
