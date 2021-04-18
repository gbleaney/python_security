import inspect
import logging
from abc import ABC, abstractclassmethod
from collections import defaultdict
from typing import Callable, Set, Type, Dict, List, Union
from json import JSONEncoder

class Exploit(ABC):
    @abstractclassmethod
    def generate_payload(command: str) -> Union[str, List[str]]:
        pass

    @abstractclassmethod
    def run_payload(payload: str) -> None:
        pass

    vulnerable_function: Union[Callable, str] = None
    source: str = ""
    category_name: str = ""
    notes: str = ""

    @classmethod
    def get_vulnerable_function_fqn(cls):
        return (
            cls.vulnerable_function
            if isinstance(cls.vulnerable_function, str)
            else (
                cls.vulnerable_function.__module__
                + "."
                + cls.vulnerable_function.__qualname__
            )
        )


class ExploitEncoder(JSONEncoder):
    def default(self, exploit: Exploit):
        if not issubclass(exploit, Exploit):
            super().default(exploit)

        return {
            "vulnerable_function": exploit.get_vulnerable_function_fqn(),
            "source": exploit.source,
            "category_name": exploit.category_name,
            "notes": exploit.notes,
        }

def get_exploits_by_category() -> Dict[str, Type[Exploit]]:
    exploits_by_category = defaultdict(list)
    for exploit in get_exploits():
        exploits_by_category[exploit.category_name].append(exploit)

    return exploits_by_category


def get_exploit(class_name: str) -> Type[Exploit]:
    return next(exploit for exploit in get_exploits() if exploit.__name__ == class_name)


def get_exploits(starting_class: Type[Exploit] = Exploit, exclude_abstract=True) -> Set[Type[Exploit]]:
    subclasses = set()
    parents_to_process = [starting_class]
    while parents_to_process:
        parent = parents_to_process.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                parents_to_process.append(child)

    if exclude_abstract:
        subclasses = set(filter(lambda cls: not inspect.isabstract(cls), subclasses))

    return subclasses
