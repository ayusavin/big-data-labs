from scripts.base import PoetryShellScript


class LintScript(PoetryShellScript):
    command = "poetry run ruff check && poetry run mypy"


class FormatScript(PoetryShellScript):
    command = "poetry run ruff check --select I --fix "
    "&& poetry run ruff format"
