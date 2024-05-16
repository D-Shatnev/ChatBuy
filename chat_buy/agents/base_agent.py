"""
This module contains the base Agent class.
"""

import json
from abc import ABC
from pathlib import Path
from typing import Any

from chat_buy.constants import AGENT_CONFIG


class BaseAgent(ABC):
    """
    Base class for all Agents. All Agents must inherit from this class.
    """

    def __init__(self) -> None:
        config = self.load_config(AGENT_CONFIG)
        class_name = self.__class__.__name__
        if class_name in config:
            params = config[class_name]
            self.prompt = params.get("prompt", "You are a helpful assistant.")
            self.model = params.get("model", "gpt-4-turbo")
            self.temperature = params.get("temperature", 0.5)
        else:
            raise ValueError(f"Agent {class_name} not found in config file.")

    @staticmethod
    def load_config(config_path: Path) -> Any:
        """
        Load config file.

        Args:
            config_path (Path): Path to the config file.

        Returns:
            Any: Config file content.
        """
        with config_path.open() as config:
            return json.load(config)
