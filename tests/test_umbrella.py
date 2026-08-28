"""Tests for bodai umbrella composition via ``bodai.apps`` entry-points."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import typer

import bodai.cli as bodai_cli

if TYPE_CHECKING:
    import pytest


@dataclass
class _FakeEntryPoint:
    """Mimics :class:`importlib.metadata.EntryPoint` for tests."""

    name: str
    value: str = "fake.module:app"
    _target: Any = None
    dist: Any = field(
        default_factory=lambda: type("Dist", (), {"name": "fake-dist"})
    )

    def load(self) -> Any:
        if self._target is _RAISE_IMPORT:
            raise ImportError(f"simulated import failure for {self.name}")
        if self._target is _RAISE_RUNTIME:
            raise RuntimeError(f"simulated runtime failure for {self.name}")
        return self._target


_RAISE_IMPORT = object()
_RAISE_RUNTIME = object()


def _make_fake_eps(
    n: int,
    *,
    break_index: int | None = None,
    break_kind: object | None = None,
) -> list[_FakeEntryPoint]:
    """Build ``n`` fake entry-points whose ``.load()`` returns a fresh Typer.

    If ``break_index`` is provided, the entry-point at that index raises
    according to ``break_kind`` (``_RAISE_IMPORT`` for ImportError,
    ``_RAISE_RUNTIME`` for RuntimeError) when ``.load()`` is called.
    """
    eps: list[_FakeEntryPoint] = []
    for i in range(n):
        target: Any = typer.Typer(name=f"app{i}")
        if break_index is not None and i == break_index:
            target = break_kind
        eps.append(
            _FakeEntryPoint(
                name=f"app{i}",
                value=f"fake_pkg.app{i}:app",
                _target=target,
            )
        )
    return eps


def _patch_entry_points(
    monkeypatch: pytest.MonkeyPatch, eps: list[_FakeEntryPoint]
) -> None:
    """Replace ``importlib.metadata.entry_points`` inside ``bodai.cli``.

    The CLI module calls :func:`importlib.metadata.entry_points` via its
    module-level reference (``importlib`` is imported at top of cli.py), so
    monkeypatching the symbol on the ``importlib.metadata`` module would
    also work. Patching the symbol the CLI uses keeps the seam tight and
    avoids cross-test leakage.
    """

    def _fake_entry_points(*, group: str = "") -> list[_FakeEntryPoint]:
        if group == "bodai.apps":
            return list(eps)
        return []

    monkeypatch.setattr(
        bodai_cli.importlib.metadata, "entry_points", _fake_entry_points
    )


def test_discover_apps_with_mock_entry_points(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """7 healthy entry-points produce 7 sub-Typers on the test app."""
    eps = _make_fake_eps(7)
    _patch_entry_points(monkeypatch, eps)

    test_app = typer.Typer(name="bodai-test")
    bodai_cli._discover_apps(test_app)

    sub_names = {t.name for t in test_app.registered_groups}
    assert sub_names == {f"app{i}" for i in range(7)}


def test_discover_apps_skips_broken_import(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """One broken entry-point is skipped; 6 attach."""
    eps = _make_fake_eps(7, break_index=3, break_kind=_RAISE_IMPORT)
    _patch_entry_points(monkeypatch, eps)

    test_app = typer.Typer(name="bodai-test")
    bodai_cli._discover_apps(test_app)

    sub_names = {t.name for t in test_app.registered_groups}
    assert sub_names == {f"app{i}" for i in range(7) if i != 3}
    assert len(sub_names) == 6


def test_discover_apps_no_entry_points(monkeypatch: pytest.MonkeyPatch) -> None:
    """Empty entry-point group: no crash, no sub-typers attached."""
    _patch_entry_points(monkeypatch, [])

    test_app = typer.Typer(name="bodai-test")
    bodai_cli._discover_apps(test_app)

    assert list(test_app.registered_groups) == []
