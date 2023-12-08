# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from typing import Optional

import typer
from rich import print
from rich.console import Console
from rich.table import Table

import composabl_core.utils.docker as docker_util
import composabl_core.utils.grpc as grpc_util
import composabl_core.utils.logger as logger_util
import composabl_core.utils.space_obs_util as space_obs_util

logger = logger_util.get_logger(__name__)
console = Console()
cli = typer.Typer()


@cli.command()
def list():
    """
    List all the supported sim images
    """
    images = docker_util.sim_list_images()

    table = Table("Sim Name", "Docker URL", "Version")

    for image in images:
        image_name = image.get("name")

        table.add_row(image_name, f"composabl/{image_name}", image.get("last_updated"))

    console.print(table)


@cli.command()
def start(
    sim_container: str,
    enable_historian: bool = True,
    stream: bool = False,
    show_name: bool = False,
):
    """
    Start the given sim

    Args:
        sim_container (str): The sim container name to start
        enable_historian (bool, optional): Whether to enable the historian. Defaults to True.
        stream (bool, optional): Whether to stream the logs. Defaults to False.
    """
    sim_name = docker_util.sim_start(
        sim_container, enable_historian, show_output=not show_name
    )

    if stream:
        docker_util.sim_logs(sim_container, stream=True)
        return

    print(sim_name)


@cli.command()
def logs(
    sim_id: str,
    stream: bool = False,
):
    """
    Get the logs of the given sim
    """
    docker_util.sim_logs(sim_id, stream=stream)


@cli.command()
def stop(sim_id: Optional[str] = None):
    """
    Stop the given sim or all sims.

    Args:
        sim_id (str, optional): The sim id to stop.
    """
    if sim_id is None:
        console.log("Getting all sims to stop")

        sims = docker_util.sim_list_running()

        with console.status("Stopping all sims"):
            idx = 0
            for sim in sims:
                sim_id = sim.get("name")
                console.log(f"[{idx + 1}/{len(sims)}] stopping {sim_id}")
                docker_util.sim_stop(sim_id)
                idx += 1

        console.log("Stopped all sims")
    else:
        docker_util.sim_stop(sim_id)


@cli.command()
def status(sim_name: Optional[str] = None, moniker: bool = False):
    """
    Get the status of the sims running

    Args:
        sim_name (str, optional): The sim name to get the status for. Defaults to None.
        moniker (bool, optional): Whether to get the moniker. Defaults to False.
    """
    if sim_name is None:
        status_all()
        return

    sim = docker_util.get_info_container(sim_name)

    if moniker:
        print(sim.get("moniker"))
        return

    print(sim)


def status_all():
    try:
        sims = docker_util.sim_list_running()

        table = Table(
            "Name", "Image", "Address", "Ports", "Historian Enabled", "Version"
        )

        for sim in sims:
            name = sim.get("name")

            sim_info = docker_util.get_info_container(name)

            # Get from the ENV VAR if the historian is enabled
            is_historian_enabled = (
                any("IS_HISTORIAN_ENABLED=1" in entry for entry in sim.get("env", []))
                or False
            )

            table.add_row(
                sim_info["name"],
                sim_info["image"],
                sim_info["moniker"],
                sim.get("ports"),
                f"{is_historian_enabled}",
                sim.get("version"),
            )

        console.print(table)
    except Exception as e:
        print(f"[red]Error ({type(e)}): {e}[/red]")


@cli.command()
def info(
    address: Optional[str] = "",
    name: Optional[str] = "",
    env_id: Optional[str] = "",
):
    """
    Get more info about a running sim

    Args:
        address (str): The address of the sim
        env_id (str): The env id of the sim (e.g., "InvertedPendulum-v4")
    """
    if address == "" and name == "":
        raise ValueError("Either address or sim must be provided")

    # If a sim is specified, start it up and get the address
    if name != "":
        sim_id = docker_util.sim_start(name, enable_historian=False)
        sim = docker_util.get_info_container(sim_id)
        address = sim.get("moniker")

    logger.debug(f"Getting sim info for '{address}' and '{env_id}'")

    # Perform the checks to see if the sim is available
    is_port_opened = grpc_util.is_port_opened(address)
    is_channel_available = grpc_util.is_channel_available(address)

    # Import the client here to avoid loading it earlier and requiring Ray
    from composabl_core.grpc.client.client import make

    c = make(
        run_id="cli",
        sim_id="cli",
        env_id=env_id,  # the env id
        env_init={},
        address=address,
    )

    c.init()

    # Gather information
    info_space_obs = c.observation_space
    info_space_action = c.action_space

    sensors = space_obs_util.convert_to_sensors(info_space_obs)

    output = f"""
    [bold]Simulator Info[/bold]
    - [bold]Address: [/bold] {address}
    - [bold]Env ID: [/bold] {env_id}
    - [bold]Is Port Opened? [/bold] {is_port_opened}
    - [bold]Is Channel Available? [/bold] {is_channel_available}

    [bold]Space Info[/bold]
    - [bold]Observation Space: [/bold] {info_space_obs}
    - [bold]Action Space: [/bold] {info_space_action}

    [bold]Sensors[/bold]
    """

    for sensor in sensors:
        output += f'\tSensor("{sensor.name}", "")\n'

    # Sensors depend on the observation space
    # - Discrete -> n sensors
    # - Box -> (https://gymnasium.farama.org/api/spaces/fundamental/#box

    print(output)
    c.close()

    # Stop the container if it was started
    if name != "":
        docker_util.sim_stop(sim_id)
