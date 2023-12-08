from queue import Queue
from pathlib import Path
from typing import Sequence, Any, IO
from common import nvl


class Buffer:
    """Queue bytes buffer"""

    def __init__(self, size: int):
        """

        Args:
            size (int): max size
        """
        self.__size = size
        self.__queue = Queue(maxsize=size)
        self.__overflow: bool = False

    def add(self, byte: bytes):
        """add a byte

        Args:
            byte (bytes): one byte
        """
        if not self.full:
            self.__queue.put(byte)
        else:
            self.__queue.get()
            self.__queue.put(byte)
            if not self.__overflow:
                self.__overflow = True

    def clear(self):
        """clear queue"""
        while not self.__queue.empty():
            self.__queue.get()
        self.__overflow = False

    @property
    def empty(self) -> bool:
        return self.__queue.empty()

    @property
    def full(self) -> bool:
        return self.__queue.full()

    @property
    def overflow(self) -> bool:
        return self.__overflow

    def to_bytes(self) -> bytes:
        ba = bytearray()
        for b in self.__queue.queue:
            ba.extend(b)
        return bytes(ba)


class LineReader:
    r"""
    Read large file by line.

    constructor:
        file (pathlib.Path): File path
        max_line (int): Maximum length of the line
        sep (bytes): Separate byte, default b'\n'
        start_pos (int): start position, default 0
        end_pos (int): end position
    usage:
        with LineReader(file, max_line, sep) as reader:
            # line is <class 'bytes'>
            for line in reader:
                if line:
                    print(line)
                elif line == sep:
                    print('empty line.')
                else:
                    # line == None
                    print('too long.')
    """

    def __init__(
        self,
        file: Path,
        max_line_size: int,
        sep: bytes = b"\n",
        start_pos: int = 0,
        end_pos: int | None = None,
    ):
        """

        Args:
            file (Path): target file path
            max_line_size (int): Maximum length of line
            sep (bytes, optional): line sep . Defaults to b"\n".
            start_pos (int, optional): start position. Defaults to 0.
            end_pos (int | None, optional): end position. Defaults to None.
        """
        self.__file_path = file
        self.__file = None
        self.__max_line_size = max_line_size
        self.__sep = sep
        self.__pos = start_pos
        file_size = file.stat().st_size
        self.__end_pos = end_pos if end_pos is not None else file_size
        self.__is_finished = False

    def __open(self):
        if not self.__file:
            self.__file = open(self.__file_path, "rb")

    def __close(self):
        if self.__file:
            self.__file.close()

    def __del__(self):
        self.__close()

    def __enter__(self):
        self.__open()
        return self

    def __exit__(self, type, value, traceback):
        self.__close()

    @staticmethod
    def __get_line(line_buffer: Buffer) -> bytes | None:
        if line_buffer.overflow:
            return None
        elif line_buffer.empty:
            return b""
        else:
            return line_buffer.to_bytes()

    def __next__(self) -> bytes:
        if self.__is_finished:
            raise StopIteration
        spe_buffer = Buffer(len(self.__sep))
        line_buffer = Buffer(size=self.__max_line_size + len(self.__sep))
        self.__file.seek(self.__pos)
        line = None
        # read byte by byte
        while self.__pos < self.__end_pos:
            byte = self.__file.read(1)
            self.__pos = self.__file.tell()
            spe_buffer.add(byte)
            line_buffer.add(byte)
            if spe_buffer.to_bytes() == self.__sep:
                break
        line = LineReader.__get_line(line_buffer=line_buffer)
        if self.__pos == self.__end_pos:
            self.__is_finished = True
        return line

    def __iter__(self):
        return self


def __find_sep(f: IO[Any], file_size: int, sep: bytes, start: int) -> int:
    buff = Buffer(len(sep))
    f.seek(start)
    r = None
    while (byte := f.read(1)) != b"":
        buff.add(byte)
        if buff.full and buff.to_bytes() == sep:
            r = f.tell() - len(sep) + 1
            break
    return r


def read_range_distribute(file: Path, n: int, sep: bytes | None = None) -> Sequence:
    """Get the reading range

    Args:
        file (Path): target file path
        n (int): Number of range
        sep (bytes | None, optional): line sep. Defaults to None.

    Returns:
        Sequence: ranges
    """
    file_size = file.stat().st_size
    sep_len = len(sep) if sep is not None else 0
    rem = file_size % n
    part_size = file_size // n
    parts = [part_size] * n
    parts[-1] += rem
    pos = -1
    ranges = []
    # 均分范围
    for s in parts:
        start = pos + 1
        end = pos + s
        pos += s
        ranges.append((start, end))
    r = [ranges]
    if sep_len == 0:
        return ranges
    if sep_len >= file_size:
        return [(0, file_size - 1)]
    # 调整范围
    max_end = 0
    new_ranges = []
    with open(file=file, mode="rb") as f:
        for rng in ranges:
            _, end = rng
            start = max_end if max_end == 0 else max_end + 1
            if start >= file_size:
                break
            if max_end > end:
                continue
            next_sep = __find_sep(f=f, file_size=file_size, sep=sep, start=end)
            next_sep = nvl(next_sep, file_size - 1)
            max_end = next_sep
            new_ranges.append((start, next_sep))
    ranges = new_ranges
    r.append(ranges)
    return r
