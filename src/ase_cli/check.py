"""ase check — deterministic check framework."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Protocol

import typer

check_app = typer.Typer()


class Status(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class Severity(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class CheckResult:
    check_id: str
    status: Status
    message: str
    severity: Severity
    location: str | None = None
    ac_id: str | None = None

    @property
    def is_warning(self) -> bool:
        return self.status == Status.WARN

    @property
    def is_failure(self) -> bool:
        return self.status == Status.FAIL


class Checker(Protocol):
    id: str
    description: str

    def check(self, path: Path) -> CheckResult: ...


class Registry:
    def __init__(self) -> None:
        self._checkers: dict[str, Checker] = {}

    def register(self, checker: Checker) -> Checker:
        checker_id = getattr(checker, "id", None)
        if not isinstance(checker_id, str):
            raise TypeError(
                f"Checker must have 'id' attribute of type str, "
                f"got {type(checker_id).__name__}"
            )
        if not callable(getattr(checker, "check", None)):
            raise TypeError("Checker must have a callable 'check' method")
        if checker.id not in self._checkers:
            self._checkers[checker.id] = checker
        return checker

    def list_all(self) -> list[tuple[str, str]]:
        return [(c.id, c.description) for c in self._checkers.values()]

    def run_all(self, path: Path) -> list[CheckResult]:
        results: list[CheckResult] = []
        for checker in self._checkers.values():
            instance = checker() if isinstance(checker, type) else checker
            try:
                results.append(instance.check(path))
            except Exception as e:
                results.append(
                    CheckResult(
                        check_id=instance.id,
                        status=Status.FAIL,
                        message=f"Checker raised exception: {e}",
                        severity=Severity.HIGH,
                    )
                )
        return results

    def run_one(self, check_id: str, path: Path) -> CheckResult:
        if check_id not in self._checkers:
            raise KeyError(f"Unknown checker ID: {check_id}")
        checker = self._checkers[check_id]
        instance = checker() if isinstance(checker, type) else checker
        return instance.check(path)


registry = Registry()


@check_app.callback(invoke_without_command=True)
def check(
    path: str = typer.Option(
        ".", "--path", "-p", help="Target directory or file to check"
    ),
) -> None:
    """Run deterministic ASE checks against a repo.

    Options:
      --path, -p TEXT  Target directory or file to check [default: .]
      --help           Show this message and exit.
    """
    target = Path(path).resolve()
    results = registry.run_all(target)

    if not results:
        typer.echo("No checks registered.")
        raise typer.Exit(0)

    for result in results:
        typer.echo(f"[{result.status.value}] {result.check_id}: {result.message}")

    passes = sum(1 for r in results if r.status == Status.PASS)
    warns = sum(1 for r in results if r.status == Status.WARN)
    fails = sum(1 for r in results if r.status == Status.FAIL)

    parts = [f"{len(results)} check(s): {passes} passed"]
    if warns:
        parts.append(f"{warns} warning(s)")
    if fails:
        parts.append(f"{fails} failed")

    typer.echo(f"\n{', '.join(parts)}")

    if fails > 0:
        raise typer.Exit(2)
    if warns > 0:
        raise typer.Exit(1)
    raise typer.Exit(0)


def _load_checkers() -> None:
    """Import checker modules to trigger registration."""
    import ase_cli.checkers  # noqa: F401


_load_checkers()
