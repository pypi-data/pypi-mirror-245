from multiprocessing.managers import BaseManager, DictProxy
from typing import Any, Callable, Dict, List, Optional, Type

from olympipe.shuttable_queue import ShuttableQueue
from olympipe.types import ClassType, InPacket, OutPacket

from .generic import GenericPipe


class ClassInstancePipe(GenericPipe[InPacket, OutPacket]):
    def __init__(
        self,
        father_process_dag: "DictProxy[str, List[str]]",
        source: "ShuttableQueue[InPacket]",
        constructor_class: Type[ClassType],
        use_method: Callable[[ClassType, InPacket], OutPacket],
        target: "ShuttableQueue[OutPacket]",
        close_method: Optional[Callable[[ClassType], Any]] = None,
        args_class: Optional[List[Any]] = None,
        kwargs_class: Optional[Dict[str, Any]] = None,
    ):
        BaseManager.register(constructor_class.__name__, constructor_class)
        self._constructor_class = constructor_class
        self._use_method = use_method
        self._close_method = close_method
        self._args_class = args_class or []
        self._kwargs_class = kwargs_class or {}
        super().__init__(father_process_dag, source, target)

    @property
    def shortname(self) -> str:
        return f"{self._constructor_class.__name__}:{self._use_method.__name__}"

    def start(self) -> None:
        self._instance = self._constructor_class(
            *self._args_class, **self._kwargs_class
        )
        self._task = getattr(self._instance, self._use_method.__name__)
        if self._close_method is not None:
            self._close_method = getattr(self._instance, self._close_method.__name__)
        else:
            self._close_method = None
        return super().start()

    def _perform_task(self, data: InPacket) -> OutPacket:
        return self._task(data)

    def _kill(self):
        if self._close_method is not None:
            self._close_method()  # type: ignore
        super()._kill()
