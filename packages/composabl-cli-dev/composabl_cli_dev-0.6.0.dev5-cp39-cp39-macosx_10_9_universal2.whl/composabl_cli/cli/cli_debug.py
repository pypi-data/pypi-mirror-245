# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential


import typer
from rich.console import Console

import composabl_core.utils.debug as debug_util
import composabl_core.utils.logger as logger_util

logger = logger_util.get_logger(__name__)
console = Console()
cli = typer.Typer()


@cli.command()
def print():
    """
    Print debug info
    """
    debug_info = debug_util.get_debug_info()
    for key in debug_info:
        logger.info("%-22s : %s" % (key, debug_info[key]))
