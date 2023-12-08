__version__ = "1.4.0"

import os
from multiprocessing import Manager, TimeoutError
from multiprocessing.managers import DictProxy
from queue import Empty, Full
from socket import socket
from threading import Condition, Timer
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    overload,
)

import tqdm
from olympipe.helpers.server import server_generator

from olympipe.pipes.batch import BatchPipe
from olympipe.pipes.debug import DebugPipe
from olympipe.pipes.explode import ExplodePipe
from olympipe.pipes.filter import FilterPipe
from olympipe.pipes.instance import ClassInstancePipe
from olympipe.pipes.limit import LimitPipe
from olympipe.pipes.reduce import ReducePipe
from olympipe.pipes.task import TaskPipe
from olympipe.pipes.timebatch import TimeBatchPipe
from olympipe.shuttable_queue import ShuttableQueue
from olympipe.types import (
    ClassType,
    InPacket,
    OutPacket,
    OptionalInPacket,
    RouteHandler,
)


class Pipeline(Generic[InPacket]):
    def __init__(
        self,
        datas: Optional[Iterable[InPacket]] = None,
        source: Optional["ShuttableQueue[Any]"] = None,
        output_queue: Optional["ShuttableQueue[InPacket]"] = None,
        father_process_dag: Optional["DictProxy[str, List[str]]"] = None,
    ):
        if father_process_dag is None:
            self._manager = Manager()
            self._father_process_dag: "DictProxy[str, List[str]]" = self._manager.dict()
            self._father_process_dag._mutex = (
                self._manager.Lock()
            )  # Important! base lock not working
        else:
            self._father_process_dag = father_process_dag

        self._source_queue = source
        self._output_queue: "ShuttableQueue[InPacket]" = (
            Pipeline.get_new_queue() if output_queue is None else output_queue
        )
        self._datas = datas
        self._last_debug_hash = ""
        self._started = True
        if father_process_dag is None:
            self._started = False
            Timer(0, self.start).start()
        waiter = Condition()
        with waiter:
            while not self._started:
                _ = waiter.wait(0.1)

    @staticmethod
    def get_new_queue() -> "ShuttableQueue[Any]":
        queue: "ShuttableQueue[Any]" = ShuttableQueue()
        return queue

    @staticmethod
    def server(
        route_handlers: List[RouteHandler[OutPacket]],
        port: int = 8000,
        host: str = "localhost",
    ) -> "Pipeline[Tuple[socket, OutPacket]]":
        return Pipeline(server_generator(route_handlers, host, port))

    def start(self):
        self._father_process_dag[self._output_queue.pid] = [str(os.getpid())]
        self._started = True
        has_grown = False
        if self._datas is not None:
            for data in tqdm.tqdm(self._datas):
                while True:
                    try:
                        _ = self._output_queue.put(data, timeout=0.1)
                        break
                    except (Full, TimeoutError):
                        pass
                    except Exception as e:
                        print("Error when feeding", e)
                        break
                    if len(self._father_process_dag) > 1:
                        has_grown = True
                    if has_grown and self._is_finished_with_errors():
                        return
                    if has_grown and len(self._father_process_dag) == 1:
                        with self._father_process_dag._mutex:
                            _ = self._father_process_dag.pop(self._output_queue.pid)
                        return
        waiter = Condition()
        with waiter:
            while not self._output_queue.empty() and len(self._father_process_dag) != 1:
                _ = waiter.wait(0.1)
            while self._source_queue is not None and not self._source_queue.empty():
                _ = waiter.wait(0.1)

        with self._father_process_dag._mutex:
            _ = self._father_process_dag.pop(self._output_queue.pid)

    def _is_finished_with_errors(self) -> bool:
        with self._father_process_dag._mutex:
            has_errors = (
                len(
                    [v for v in dict(self._father_process_dag).values() if "error" in v]
                )
                >= 1
            )
            dead = (
                len(
                    [
                        v
                        for v in dict(self._father_process_dag).values()
                        if "error" not in v
                    ]
                )
                <= 1
            )

        killme = dead and has_errors
        if killme:
            print("Pipeline has errors and will be closed")
        return killme

    def register_father_son(self, father: str, son: str):
        with self._father_process_dag._mutex:
            dag: Dict[str, List[str]] = self._father_process_dag._getvalue()
            if father not in dag:
                self._father_process_dag[father] = [son]
            else:
                self._father_process_dag[father] = [
                    *dag[father],
                    son,
                ]

    def task(
        self, task: Callable[[InPacket], OutPacket], count: int = 1
    ) -> "Pipeline[OutPacket]":
        if count < 1:
            raise ValueError("count must be greater than or equal to 1")

        output_task_queue: "ShuttableQueue[OutPacket]" = Pipeline.get_new_queue()

        for _ in range(count):
            p = TaskPipe(
                self._father_process_dag,
                self._output_queue,
                task,
                output_task_queue,
            )

            self.register_father_son(str(p.pid), self._output_queue.pid)
            self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def limit(self, packet_limit: int) -> "Pipeline[InPacket]":
        output_task_queue: "ShuttableQueue[InPacket]" = Pipeline.get_new_queue()

        p = LimitPipe(
            self._father_process_dag,
            self._output_queue,
            output_task_queue,
            packet_limit,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def class_task(
        self,
        class_constructor: Type[ClassType],
        class_method: Callable[[ClassType, InPacket], OutPacket],
        class_args: Optional[List[Any]] = None,
        close_method: Optional[Callable[[ClassType], Any]] = None,
        class_kwargs: Optional[Dict[str, Any]] = None,
        count: int = 1,
    ) -> "Pipeline[OutPacket]":
        if count < 1:
            raise ValueError("count must be greater than or equal to 1")
        output_task_queue: "ShuttableQueue[OutPacket]" = Pipeline.get_new_queue()

        for _ in range(count):
            p = ClassInstancePipe(
                self._father_process_dag,
                self._output_queue,
                class_constructor,
                class_method,
                output_task_queue,
                close_method,
                class_args or [],
                class_kwargs or {},
            )

            self.register_father_son(str(p.pid), self._output_queue.pid)
            self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def explode(
        self,
        explode_function: Optional[Callable[[InPacket], Iterable[OutPacket]]] = None,
    ) -> "Pipeline[OutPacket]":
        output_task_queue: "ShuttableQueue[OutPacket]" = Pipeline.get_new_queue()

        p = ExplodePipe(
            self._father_process_dag,
            self._output_queue,
            explode_function,
            output_task_queue,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def batch(
        self, batch_size: int = 2, keep_incomplete_batch: bool = True
    ) -> "Pipeline[List[InPacket]]":
        output_task_queue: "ShuttableQueue[List[InPacket]]" = Pipeline.get_new_queue()
        p = BatchPipe(
            self._father_process_dag,
            self._output_queue,
            output_task_queue,
            batch_size,
            keep_incomplete_batch,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def temporal_batch(self, time_interval: float) -> "Pipeline[List[InPacket]]":
        output_task_queue: "ShuttableQueue[List[InPacket]]" = Pipeline.get_new_queue()
        p = TimeBatchPipe(
            self._father_process_dag,
            self._output_queue,
            output_task_queue,
            time_interval,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    @overload
    def filter(
        self: "Pipeline[Optional[OptionalInPacket]]",
    ) -> "Pipeline[OptionalInPacket]":
        ...

    @overload
    def filter(
        self: "Pipeline[InPacket]", keep_if_true: Callable[[InPacket], bool]
    ) -> "Pipeline[InPacket]":
        ...

    def filter(self, keep_if_true: Optional[Callable[[InPacket], bool]] = None):  # type: ignore
        """Filters packets based on the result of the function applied to this packet

        Args:
            keep_if_true (Optional[Callable[[T], bool]], optional): If None is provided, the pipe will just filter None packets

        Returns:
            Pipeline[T]: OutputPipeline
        """
        output_task_queue: "ShuttableQueue[InPacket]" = Pipeline.get_new_queue()

        p = FilterPipe(
            self._father_process_dag,
            self._output_queue,
            keep_if_true,
            output_task_queue,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def debug(self) -> "Pipeline[InPacket]":
        output_task_queue: "ShuttableQueue[InPacket]" = Pipeline.get_new_queue()

        p = DebugPipe(
            self._father_process_dag,
            self._output_queue,
            output_task_queue,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def reduce(
        self,
        accumulator: OutPacket,
        reducer: Callable[[InPacket, OutPacket], OutPacket],
    ) -> "Pipeline[OutPacket]":
        output_task_queue: "ShuttableQueue[OutPacket]" = Pipeline.get_new_queue()

        p = ReducePipe(
            self._father_process_dag,
            self._output_queue,
            output_task_queue,
            accumulator,
            reducer,
        )

        self.register_father_son(str(p.pid), self._output_queue.pid)
        self.register_father_son(output_task_queue.pid, str(p.pid))

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
            father_process_dag=self._father_process_dag,
        )

    def wait_and_reduce(
        self,
        accumulator: OutPacket,
        reducer: Callable[[InPacket, OutPacket], OutPacket],
    ) -> "OutPacket":
        output_pipeline = self.reduce(accumulator, reducer)
        [[res]] = Pipeline._wait_for_all_results([output_pipeline])
        return res

    @staticmethod
    def are_pipelines_running(pipes: List["Pipeline[Any]"]) -> bool:
        mutexs: List[Any] = []
        for p in pipes:
            m = p._father_process_dag._mutex
            if m not in mutexs:
                mutexs.append(m)
        for m in mutexs:
            m.acquire()

        remaining_dag = any([len(p._father_process_dag) > 0 for p in pipes])

        full_pipe = any([not p._output_queue.empty() for p in pipes])
        for m in mutexs:
            m.release()

        return remaining_dag or full_pipe

    @staticmethod
    def _wait_for_all_completions(
        pipes: List["Pipeline[Any]"], debug_graph: Optional[str] = None
    ) -> None:
        while Pipeline.are_pipelines_running(pipes):
            if debug_graph is not None:
                pipes[0].print_graph(debug_graph)
            for i, p in enumerate(pipes):
                try:
                    _: Any = p._output_queue.get(timeout=0.1)
                except (TimeoutError, Full, Empty):
                    pass
                except Exception as e:
                    _ = pipes.pop(i)
                    print("Error waiting:", e)
                if pipes[i]._is_finished_with_errors():
                    return
                if len(p._father_process_dag) == 1:
                    try:
                        while True:
                            _ = pipes[i]._output_queue.get(timeout=0.05)
                    except Exception:
                        pass
                    return

    @staticmethod
    def _wait_for_all_results(
        pipes: List["Pipeline[Any]"], debug_graph: Optional[str] = None
    ) -> List[List[Any]]:
        final_queues: List[Optional[ShuttableQueue[Any]]] = [
            p._output_queue for p in pipes
        ]
        outputs: List[List[Any]] = [[] for _ in pipes]
        while Pipeline.are_pipelines_running(pipes):
            if debug_graph is not None:
                pipes[0].print_graph(debug_graph)
            for i, final_queue in enumerate(final_queues):
                if final_queue is None:
                    continue
                try:
                    packet: Any = final_queue.get(timeout=0.1)
                    outputs[i].append(packet)
                except (TimeoutError, Empty):
                    pass
                except Exception as e:
                    print("Error waiting:", e)
                    return outputs
                if pipes[i]._is_finished_with_errors():
                    return outputs
                if len(pipes[i]._father_process_dag) == 1:
                    try:
                        while True:
                            _ = pipes[i]._output_queue.get(timeout=0.05)
                    except Exception:
                        pass
                    return outputs

        return outputs

    def wait_for_completion(
        self,
        other_pipes: Optional[List["Pipeline[Any]"]] = None,
        debug_graph: Optional[str] = None,
    ) -> None:
        """_summary_

        Args:
            other_pipes (List[&quot;Pipeline[Any]&quot;], optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """
        return Pipeline._wait_for_all_completions(
            [self, *(other_pipes or [])], debug_graph
        )

    def wait_for_results(
        self,
        other_pipes: Optional[List["Pipeline[Any]"]] = None,
        debug_graph: Optional[str] = None,
    ) -> List[List[InPacket]]:
        """_summary_

        Args:
            other_pipes (List[&quot;Pipeline[Any]&quot;], optional): _description_. Defaults to [].

        Returns:
            List[List[R]]: _description_
        """
        return Pipeline._wait_for_all_results([self, *(other_pipes or [])], debug_graph)

    def wait_for_result(self, debug_graph: Optional[str] = None) -> List[InPacket]:
        """
        Args:

        Returns:
            Iterable[R]: _description_
        """
        res: List[List[InPacket]] = Pipeline._wait_for_all_results([self], debug_graph)

        return res[0]

    def print_graph(self, debug_graph: str):
        try:
            import hashlib

            import psutil
            from graphviz import Digraph  # type: ignore

            dot = Digraph("G", filename=debug_graph, format="png")

            def format_node_name(node: str) -> str:
                try:
                    p = psutil.Process(int(node))
                    return f"({node}) {p.name()}"
                except Exception:
                    return node

            with self._father_process_dag._mutex:
                for node, parents in self._father_process_dag.items():
                    dot.node(node, format_node_name(node))

                    for parent in parents:
                        if parent not in self._father_process_dag:
                            dot.node(parent, parent)

                        if parent:
                            dot.edge(parent, node)

                # Create a new SHA-256 hash object
                sha256 = hashlib.sha256()
                sha256.update(dot.source.encode())
                computed_hash = sha256.hexdigest()
                if computed_hash != self._last_debug_hash:
                    self._last_debug_hash = computed_hash
                    _ = dot.render(quiet=True, cleanup=True)

        except Exception as e:
            print(e)
