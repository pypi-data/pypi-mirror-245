"""
Copyright (c) 2008-2023 synodriver <diguohuangjiajinweijun@gmail.com>
"""
import re
from typing import List, Optional, Pattern, Set, Tuple, Union


# r"ArchiveEntry __dealloc__ (?P<addr>\w+?),\s+?"
class State:
    def __init__(
        self,
        pairs: Optional[
            List[Tuple[Union[str, Pattern[str]], Union[str, Pattern[str]]]]
        ] = None,
    ):
        self.pairs = []
        if pairs is not None:
            for malloc, free in pairs:  # 匹配上malloc的行表示这里进行了一次内存申请，free毅然
                if isinstance(malloc, str):
                    malloc = re.compile(malloc)
                if isinstance(free, str):
                    free = re.compile(free)
                self.pairs.append((malloc, free))
        # 记录malloc之后仍然没有free的内存地址 [(地址, 日志文件行号)]
        self._state = []  # type: List[Tuple[str, int]]

    def add_pair(self, pair: Tuple[Union[str, Pattern[str]], Union[str, Pattern[str]]]):
        malloc = re.compile(pair[0]) if isinstance(pair[0], str) else pair[0]
        free = re.compile(pair[1]) if isinstance(pair[1], str) else pair[1]
        self.pairs.append((malloc, free))

    def match(self, line: str, lineno: int):
        for malloc, free in self.pairs:
            if m := malloc.match(line):
                addr = m.group("addr")
                for previous_addr, previous_lineno in self._state:
                    if addr == previous_addr:
                        raise ValueError(
                            f"address {addr} has already been malloced at line {previous_lineno}, but line:{lineno} malloc it again"
                        )
                self._state.append((addr, lineno))
                break
            if m := free.match(line):
                addr = m.group("addr")
                index: int = 0
                for previous_addr, previous_lineno in self._state:
                    if addr == previous_addr:
                        break
                    index += 1
                    # 对应地址的被free了
                else:
                    raise ValueError(
                        f"address {addr}  been free before malloce at line {lineno}"
                    )
                del self._state[index]
                break

    @property
    def has_leak(self):
        return bool(self._state)

    def get_leak(self):
        return self._state


def parse_log(file, state: State, encoding: str = "utf-8"):
    close_fp: bool = False
    if isinstance(file, (str, bytes)):
        fp = open(file, "r", encoding=encoding)
        close_fp = True
    else:
        fp = file
    try:
        lineno: int = 1
        while line := fp.readline():
            state.match(line, lineno)
            lineno += 1
        if state.has_leak:
            raise ValueError(
                f"memory leak detected at {state.get_leak()}, those addresses are never freed"
            )

    finally:
        if close_fp:
            try:
                fp.close()
            except:
                pass
