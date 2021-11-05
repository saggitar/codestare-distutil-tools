from abc import ABC
from distutils.cmd import Command
from distutils.errors import DistutilsOptionError
from pathlib import Path
from typing import Optional, List

PathList = Optional[List[Path]]


class PathCommand(Command, ABC):
    def ensure_path_list(self, option):
        val = getattr(self, option)
        if val is None:
            return

        if not isinstance(val, list) or not all(isinstance(o, Path) for o in val):
            self.ensure_string_list(option)
            val = [Path(s) for s in getattr(self, option)]

        not_exist = [p for p in val if not p.exists()]
        if any(not_exist):
            raise DistutilsOptionError(f"Paths {', '.join(str(o.absolute()) for o in not_exist)} don't exist.")

        setattr(self, option, val)

    def ensure_dir_list(self, option):
        self.ensure_path_list(option)
        val = getattr(self, option)
        if val is None:
            return

        not_dir = [p for p in val if not p.is_dir()]
        if any(not_dir):
            raise DistutilsOptionError(f"Paths {', '.join(str(o.absolute()) for o in not_dir)} are not directories.")
