import inspect
from abc import ABC, abstractclassmethod
from typing import Callable, Set, Type, Dict
from collections import defaultdict

import logging

class Exploit(ABC):
    @abstractclassmethod
    def generate_payload(command: str) -> str:
        pass

    @abstractclassmethod
    def run_payload(payload: str) -> None:
        pass

    vulnerable_function: Callable
    source: str = ""
    category_name: str = ""

    @classmethod
    def get_vulnerable_function_fqn(cls):
        return cls.vulnerable_function.__module__ + '.' + cls.vulnerable_function.__qualname__


def get_exploits_by_category() -> Dict[str, Type[Exploit]]:
    exploits_by_category = defaultdict(list)
    for exploit in get_exploits():
        exploits_by_category[exploit.category_name].append(exploit)

    return exploits_by_category


def get_exploit(class_name: str) -> Type[Exploit]:
    return next(exploit for exploit in get_exploits() if exploit.__name__ == class_name)


def get_exploits() -> Set[Type[Exploit]]:
    subclasses = set()
    parents_to_process = [Exploit]
    while parents_to_process:
        parent = parents_to_process.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                parents_to_process.append(child)

    subclasses = set(filter(lambda cls: not inspect.isabstract(cls), subclasses))

    return subclasses
