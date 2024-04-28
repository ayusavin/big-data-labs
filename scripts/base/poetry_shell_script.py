"""Base PoetryShellScript class implementation"""

import subprocess


class PoetryShellScript:
    command: str = ""

    def __init__(self) -> None:
        try:
            return_code: int = (
                subprocess
                .run(self.command, shell=True, check=True)
                .returncode
            )
        except subprocess.CalledProcessError as e:
            return_code = e.returncode
        except KeyboardInterrupt:
            return_code = 0
        exit(return_code)
