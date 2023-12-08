"""
Wrapper Base Module.

This module introduces the `BaseWrapper` class, which serves as the
fundamental structure for wrappers in the experimental framework. Wrappers
manage experiment variations based on the global experiment state. They are
crucial components to control and monitor different variations during an
experiment's lifecycle.
"""

from typing import Any, Dict, Optional, Type

from ..schemas.wrapper_configs import BaseWrapperConfig
from ..states.experiment_state import ExperimentState


class BaseWrapper:
    """
    Base class for wrappers that manage experiment variations based on the
    global experiment state.
    
    This class provides the fundamental structure and methods for wrappers.
    Specific wrappers should inherit from this class and implement the
    necessary methods.
    
    Attributes:
        name (str): The name of the wrapper.
        experiment_state (ExperimentState): The global state of the experiment.
        config (BaseWrapperConfig): The configuration for the wrapper.
    """
    _registry: Dict[str, Dict[str, Any]] = {}
    default_config: Optional[BaseWrapperConfig] = None

    @classmethod
    def decorator_register(cls, name: str):
        """Decorator to register new wrappers."""

        def inner(subclass: Type[BaseWrapper]):
            cls._registry[name] = {
                "class": subclass,
                "default_config": subclass.default_config
            }
            return subclass

        return inner

    def __init__(
        self,
        name: str,
        config: Optional[BaseWrapperConfig] = None,
        state: Optional[ExperimentState] = None,
    ) -> None:
        self.name = name
        self.experiment_state = state if state else ExperimentState()
        self.config = config

    def get_variation(self) -> Optional[Any]:
        """
        Retrieve the next variation for the experiment based on the wrapper's
        name.

        Returns:
            Optional[Any]: The next variation if the experiment is active,
            otherwise None.
        """
        if self.experiment_state.active:
            return self.experiment_state.get_next_variation(self.name)
        return None

    @classmethod
    def get_wrapper(cls, name: str) -> Optional[Type['BaseWrapper']]:
        return cls._registry.get(name, {}).get("class")

    @classmethod
    def get_default_config(cls, name: str) -> Optional[BaseWrapperConfig]:
        return cls._registry.get(name, {}).get("default_config")

    @classmethod
    def get_config_class(cls, name: str) -> Optional[Type[BaseWrapperConfig]]:
        return cls._registry.get(name, {}).get("config_cls")

    def get_active_config(self, name: str) -> Optional[BaseWrapperConfig]:
        if self.experiment_state.active and self.experiment_state.config and self.experiment_state.config.wrapper_configs:
            config = self.experiment_state.config.wrapper_configs.get(name)
            if config:
                config_cls = BaseWrapper.get_config_class(name)
                if config_cls:
                    return config_cls(**config.asdict())
        return None

    @classmethod
    def register_wrapper(
        cls,
        name: str,
        wrapper_cls: Type['BaseWrapper'],
        config_cls: Optional[Type[BaseWrapperConfig]] = None
    ):
        cls._registry[name] = {
            "class": wrapper_cls,
            "default_config": wrapper_cls.default_config,
            "config_cls": config_cls
        }
