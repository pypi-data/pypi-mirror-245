from multiprocessing.managers import DictProxy
from typing import Callable, Iterable, List, Optional, cast

from olympipe.pipes.task import TaskPipe
from olympipe.shuttable_queue import ShuttableQueue
from olympipe.types import InPacket, OutPacket


class ExplodePipe(TaskPipe[InPacket, OutPacket]):
    def __init__(
        self,
        father_process_dag: "DictProxy[str, List[str]]",
        source: "ShuttableQueue[InPacket]",
        task: Optional[Callable[[InPacket], Iterable[OutPacket]]],
        target: "ShuttableQueue[OutPacket]",
    ):
        task = (lambda x: cast(Iterable[OutPacket], x)) if task is None else task
        super().__init__(father_process_dag, source, task, target)  # type: ignore

    @property
    def shortname(self) -> str:
        return f"explode:{self._task.__name__}"

    def _send_to_next(self, processed: Iterable[OutPacket]):  # type: ignore
        for p in processed:
            super()._send_to_next(p)
