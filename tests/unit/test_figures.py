"""Offline tests for chapter-figure resolution (no network, no matplotlib)."""

import httpx
import pytest

from bookgen.crew.moon_content import CHAPTER_FIGURES
from bookgen.latex.figures import _http_fetch, _is_valid_image, ensure_figures

_FAKE_JPEG = b"\xff\xd8" + b"0" * 90_000


def _write_bundle(bundled_dir):
    bundled_dir.mkdir(parents=True, exist_ok=True)
    for filename, _urls, _caption in CHAPTER_FIGURES:
        (bundled_dir / filename).write_bytes(_FAKE_JPEG)


def test_ensure_figures_prefers_bundled_without_network(tmp_path) -> None:
    latex_root = tmp_path / "latex"
    latex_root.mkdir()
    bundled = tmp_path / "bundled"
    _write_bundle(bundled)

    def forbidden_fetch(_urls, _target):
        raise AssertionError("network fetch must not happen when bundled exists")

    saved = ensure_figures(
        latex_root, fetch=forbidden_fetch, bundled_dir=bundled, make_plot=False
    )
    assert len(saved) == len(CHAPTER_FIGURES)
    assert all(path.exists() for path in saved)


def test_ensure_figures_falls_back_to_fetch(tmp_path) -> None:
    latex_root = tmp_path / "latex"
    latex_root.mkdir()

    def fake_fetch(_urls, target):
        target.write_bytes(_FAKE_JPEG)
        return True

    saved = ensure_figures(
        latex_root, fetch=fake_fetch, bundled_dir=tmp_path / "missing", make_plot=False
    )
    assert len(saved) == len(CHAPTER_FIGURES)


def test_ensure_figures_raises_when_unresolvable(tmp_path) -> None:
    latex_root = tmp_path / "latex"
    latex_root.mkdir()

    with pytest.raises(RuntimeError):
        ensure_figures(
            latex_root,
            fetch=lambda _urls, _target: False,
            bundled_dir=tmp_path / "missing",
            make_plot=False,
        )


def test_is_valid_image_rejects_small_and_non_image(tmp_path) -> None:
    small = tmp_path / "small.jpg"
    small.write_bytes(b"\xff\xd8tiny")
    assert _is_valid_image(small) is False
    assert _is_valid_image(tmp_path / "missing.jpg") is False
    good = tmp_path / "good.jpg"
    good.write_bytes(_FAKE_JPEG)
    assert _is_valid_image(good) is True


def test_http_fetch_with_mock_transport(tmp_path, monkeypatch) -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=_FAKE_JPEG)

    real_client = httpx.Client  # capture before patching to avoid recursion
    monkeypatch.setattr(
        httpx, "Client", lambda *_a, **_k: real_client(transport=httpx.MockTransport(handler))
    )
    target = tmp_path / "img.jpg"
    assert _http_fetch(["https://example.test/a.jpg"], target) is True
    assert target.read_bytes() == _FAKE_JPEG
