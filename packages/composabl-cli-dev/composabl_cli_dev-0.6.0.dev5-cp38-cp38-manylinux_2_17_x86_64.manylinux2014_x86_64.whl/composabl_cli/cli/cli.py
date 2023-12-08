# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import typer

from composabl_cli.cli import cli_debug, cli_historian, cli_sim, cli_job, cli_benchmark

cli = typer.Typer()
cli.add_typer(cli_sim.cli, name="sim")
cli.add_typer(cli_historian.cli, name="historian")
cli.add_typer(cli_debug.cli, name="debug")
cli.add_typer(cli_job.cli, name="job")
cli.add_typer(cli_benchmark.cli, name="benchmark")


def run():
    cli()
