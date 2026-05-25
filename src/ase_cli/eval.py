"""ase eval — YAML-driven agent eval suite runner."""

from __future__ import annotations

import glob
import re
from dataclasses import dataclass, field
from pathlib import Path

import typer
import yaml

from ase_cli.check import CheckResult, Severity, Status

eval_app = typer.Typer()


@dataclass
class EvalCheck:
    id: str
    description: str
    type: str
    path: str | None = None
    file: str | None = None
    pattern: str | None = None
    severity: Severity = Severity.HIGH


@dataclass
class EvalTask:
    name: str
    checks: list[EvalCheck] = field(default_factory=list)


def _run_check(check: EvalCheck, root: Path) -> CheckResult:
    sev = check.severity

    if check.type == "file_exists":
        matches = glob.glob(str(root / (check.path or "")))
        if matches:
            return CheckResult(check.id, Status.PASS, f"{check.path} found", sev)
        return CheckResult(check.id, Status.FAIL, f"{check.path} not found", sev)

    if check.type == "directory_exists":
        target = root / (check.path or "")
        if target.is_dir():
            return CheckResult(check.id, Status.PASS, f"{check.path} found", sev)
        return CheckResult(check.id, Status.FAIL, f"{check.path} not found", sev)

    if check.type in ("file_contains", "file_not_contains"):
        file_path = root / (check.file or "")
        if not file_path.is_file():
            return CheckResult(
                check.id, Status.FAIL, f"file not found: {check.file}", sev
            )
        content = file_path.read_text(encoding="utf-8")
        found = bool(re.search(check.pattern or "", content, re.MULTILINE))
        if check.type == "file_contains":
            if found:
                return CheckResult(
                    check.id,
                    Status.PASS,
                    f"{check.file} matches {check.pattern!r}",
                    sev,
                )
            return CheckResult(
                check.id,
                Status.FAIL,
                f"{check.file} does not match {check.pattern!r}",
                sev,
            )
        else:  # file_not_contains
            if not found:
                return CheckResult(
                    check.id,
                    Status.PASS,
                    f"{check.file} does not contain {check.pattern!r}",
                    sev,
                )
            return CheckResult(
                check.id,
                Status.FAIL,
                f"{check.file} contains {check.pattern!r}",
                sev,
            )

    return CheckResult(
        check.id, Status.FAIL, f"unknown check type: {check.type}", Severity.HIGH
    )


def _parse_severity(raw: str | None) -> Severity:
    if raw is None:
        return Severity.HIGH
    try:
        return Severity[raw.upper()]
    except KeyError:
        return Severity.HIGH


def _load_tasks(eval_dir: Path) -> list[tuple[EvalTask, list[CheckResult]]]:
    """Load eval tasks from subdirectories of eval_dir.

    Returns (task, results) pairs where results is non-empty only for parse errors.
    Normal tasks return an empty results list; checks are run separately.
    """
    if not eval_dir.is_dir():
        return []

    tasks: list[tuple[EvalTask, list[CheckResult]]] = []
    for entry in sorted(eval_dir.iterdir()):
        if not entry.is_dir():
            continue
        checks_file = entry / "checks.yaml"
        if not checks_file.is_file():
            continue
        try:
            data = yaml.safe_load(checks_file.read_text(encoding="utf-8"))
            checks: list[EvalCheck] = []
            for item in data.get("checks", []):
                checks.append(
                    EvalCheck(
                        id=item["id"],
                        description=item.get("description", ""),
                        type=item["type"],
                        path=item.get("path"),
                        file=item.get("file"),
                        pattern=item.get("pattern"),
                        severity=_parse_severity(item.get("severity")),
                    )
                )
            tasks.append((EvalTask(name=entry.name, checks=checks), []))
        except Exception as e:
            error_task = EvalTask(name=entry.name, checks=[])
            error_result = CheckResult(
                check_id="checks-yaml-parse",
                status=Status.FAIL,
                message=f"checks.yaml parse error: {e}",
                severity=Severity.HIGH,
            )
            tasks.append((error_task, [error_result]))

    return tasks


def run_eval(root: Path, eval_dir: Path) -> list[tuple[EvalTask, list[CheckResult]]]:
    task_pairs = _load_tasks(eval_dir)
    results: list[tuple[EvalTask, list[CheckResult]]] = []
    for task, parse_errors in task_pairs:
        if parse_errors:
            results.append((task, parse_errors))
        else:
            task_results = [_run_check(c, root) for c in task.checks]
            results.append((task, task_results))
    return results


@eval_app.callback(invoke_without_command=True)
def eval_cmd(
    path: str = typer.Option(".", "--path", "-p", help="Repo root to check against"),
    eval_dir: str = typer.Option(
        "eval", "--eval-dir", "-e", help="Directory containing eval tasks"
    ),
) -> None:
    """Run an eval suite against agent output and print a score."""
    root = Path(path).resolve()
    tasks_dir = Path(eval_dir).resolve()

    task_pairs = run_eval(root, tasks_dir)

    if not task_pairs:
        typer.echo(f"No eval tasks found in {eval_dir}")
        raise typer.Exit(0)

    col = 30
    header = f"{'Task':<{col}}  {'Pass':>4}  {'Warn':>4}  {'Fail':>4}"
    sep = "-" * len(header)
    typer.echo(header)
    typer.echo(sep)

    total_pass = total_warn = total_fail = 0
    failures: list[str] = []

    for task, results in task_pairs:
        p = sum(1 for r in results if r.status == Status.PASS)
        w = sum(1 for r in results if r.status == Status.WARN)
        f = sum(1 for r in results if r.status == Status.FAIL)
        total_pass += p
        total_warn += w
        total_fail += f
        typer.echo(f"{task.name:<{col}}  {p:>4}  {w:>4}  {f:>4}")
        for r in results:
            if r.status == Status.FAIL:
                failures.append(f"  {task.name} / {r.check_id}: {r.message}")

    typer.echo(sep)
    typer.echo(f"{'Total':<{col}}  {total_pass:>4}  {total_warn:>4}  {total_fail:>4}")

    total = total_pass + total_warn + total_fail
    pct = int(100 * total_pass / total) if total else 0
    typer.echo(f"\nScore: {total_pass}/{total} ({pct}%)")

    if failures:
        typer.echo("\nFailures:")
        for line in failures:
            typer.echo(line)

    if total_fail > 0:
        raise typer.Exit(2)
    if total_warn > 0:
        raise typer.Exit(1)
    raise typer.Exit(0)
