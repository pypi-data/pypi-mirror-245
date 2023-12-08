# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import time
from typing import Optional

import typer
from rich.console import Console

import composabl_core.utils.docker as docker_util
import composabl_core.utils.logger as logger_util
from composabl_core.grpc.client.client import make

logger = logger_util.get_logger(__name__)
console = Console()
cli = typer.Typer()


@cli.command()
def protocol(
    sim_name="sim-mujoco",
    env_name="walker2d",
    running_time_s: int = 10,
    sim_address: Optional[str] = None,
):
    """
    Gets the benchmark for the gRPC protocol overhead

    Args:
        sim_name (str, optional): The sim name to use. Defaults to "sim-mujoco".
        env_name (str, optional): The env name to use. Defaults to "walker2d".
        running_time_s (int, optional): The amount of time to run the benchmark. Defaults to 10.
        sim_address (Optional[str], optional): By default, we check on the Docker Hub for the sim_name
        in the composabl organization. If you want to use a custom sim, you can pass the address here.
    """
    try:
        logger.debug(f"Starting Simulator: {sim_name}")

        if sim_address is None:
            sim_id = docker_util.sim_start(sim_name, False, show_output=False)
            sim_info = docker_util.get_info_container(sim_id)
            sim_address = sim_info.get("moniker", "localhost:1337")

        logger.debug(f"Creating Client for Simulator: {sim_name} on {sim_address}")
        c = make(
            "run-benchmark",
            "sim-benchmark",
            env_name,
            sim_address,
            {"render_mode": "rgb_array"},
        )

        c.init()
        c.reset()

        logger.debug("Running benchmark")
        start_time = time.time()
        iterations = 0

        while time.time() - start_time < running_time_s:
            a = c.action_space_sample()
            c.step(a[0])
            iterations += 1

        print(iterations)
    except Exception as e:
        print(e)  # we just print it as the output is used in the benchmark test
