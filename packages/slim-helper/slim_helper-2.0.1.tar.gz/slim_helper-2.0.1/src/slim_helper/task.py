import multiprocessing as mp
from typing import Callable, Sequence


class ParallelWorker:
    r"""
    Parallel executor
    with ParallelWorker(callback=work, parallel=4) as w:
        for i in range(100):
            w.input.put((1,))
        for i in range(100):
            print(w.output.get())
    """

    def __init__(
        self,
        callback: Callable,
        parallel: int = 1,
        max_input: int = 0,
        max_output: int = 0,
    ):
        """
        Args:
            callback (Callable): callback function
            parallel (int, optional): parallel number. Defaults to 1.
            max_input (int, optional): input queue capacity. Defaults to 0.
            max_output (int, optional): output queue capacity. Defaults to 0.
        """
        self.__parallel = parallel
        self.__callback = callback
        self.__input = mp.Queue(maxsize=max_input)
        self.__output = mp.Queue(maxsize=max_output)
        self.__processes: Sequence[mp.Process] = []
        self.reset()

    def reset(self):
        """reset"""
        self.kill()
        self.clear()
        self.__processes = []
        for _ in range(self.__parallel):
            p = mp.Process(target=self.__work, daemon=True)
            self.__processes.append(p)
            p.start()

    def __work(self):
        for arg in iter(self.__input.get, None):
            try:
                r = self.__callback(*arg)
                self.__output.put((arg, r))
            except Exception as e:
                self.__output.put((arg, e))

    def stop(self):
        """stop processes"""
        for _ in self.__processes:
            self.__input.put(None)

    def kill(self):
        """kill processes"""
        for p in self.__processes:
            p.terminate()

    @property
    def is_running(self) -> bool:
        for p in self.__processes:
            if p.is_alive():
                return True
        return False

    @property
    def input(self) -> mp.Queue:
        """get input queue

        Returns:
            Queue: Queue
        """
        return self.__input

    @property
    def output(self) -> mp.Queue:
        """get output queue

        Returns:
            Queue: Queue
        """
        return self.__output

    def clear_input(self):
        """clear input queue"""
        while not self.__input.empty():
            self.__input.get()

    def clear_output(self):
        """clear output queue"""
        while not self.__output.empty():
            self.__output.get()

    def clear(self):
        """clear inputa nd output queue"""
        self.clear_input()
        self.clear_output()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.kill()

    def __del__(self):
        self.kill()
