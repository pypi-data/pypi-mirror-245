from __future__ import annotations

from typing import Optional

import typer
from pytest import LogCaptureFixture
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from harbor_cli.deprecation import check_deprecated_options
from harbor_cli.deprecation import Deprecated
from harbor_cli.deprecation import get_deprecated_params
from harbor_cli.deprecation import used_deprecated

app = typer.Typer()
runner = CliRunner(mix_stderr=False)


def test_check_deprecated_options(
    mocker: MockerFixture, caplog: LogCaptureFixture
) -> None:
    @app.command()
    def main(
        ctx: typer.Context,
        option1: Optional[str] = typer.Option(
            None,
            "--option1",
            "-o",
            Deprecated("--long-option1", replacement="--option1"),
            help="Option 1.",
        ),
        option2: Optional[str] = typer.Option(
            None,
            "--option2",
            "-O",
            "--long-option2",
            help="Option 1.",
        ),
    ) -> None:
        # test everything inside this command for simplicity
        deprecated = get_deprecated_params(ctx)
        assert len(deprecated) == 1
        assert deprecated[0] == "--long-option1"
        assert deprecated[0].replacement == "--option1"

        used = used_deprecated(ctx)
        assert len(used) == 1
        assert used[0] == "--long-option1"

        check_deprecated_options(ctx)

    args = ["--long-option1", "arg", "--long-option2", "arg"]
    # patch sys.argv to simulate the user passing in the deprecated option
    mocker.patch("sys.argv", args)

    runner.invoke(app, args)

    # We don't test the _exact_ message because it's not important
    assert "--long-option1" in caplog.text  # deprecated
    assert "--option1" in caplog.text  # replacement
    assert "deprecated" in caplog.text
