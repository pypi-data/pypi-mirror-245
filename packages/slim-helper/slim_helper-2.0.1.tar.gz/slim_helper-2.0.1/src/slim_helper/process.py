import shlex
import subprocess
from typing import Sequence


def execute_command(
    cmd: Sequence[str],
    stdin: bytes | None = None,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    dry: bool = False,
) -> tuple[int, bytes, bytes]:
    """execute command

    Args:
        cmd (Sequence[str]): command and arguments
        stdin (bytes | None, optional): stdin. Defaults to None.
        stdout (optional): stdout. Defaults to subprocess.PIPE.
        stderr (optional): stderr. Defaults to subprocess.PIPE.
        dry (bool, optional): dry run. Defaults to False.

    Returns:
        tuple[int, bytes, bytes]: exit_code,stdout,stderr
    """
    if dry:
        print(shlex.join(cmd))
        return 0, b"", b""
    completed: subprocess.CompletedProcess = subprocess.run(
        cmd, stdout=stdout, stderr=stderr, input=stdin
    )
    return completed.returncode, completed.stdout, completed.stderr
