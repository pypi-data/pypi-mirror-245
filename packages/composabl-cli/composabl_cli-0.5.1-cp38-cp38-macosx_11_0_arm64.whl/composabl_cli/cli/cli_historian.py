# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import typer
from rich.console import Console
from rich.table import Table

import composabl_core.utils.docker as docker_util
import composabl_core.utils.docker_historian as docker_historian_util

console = Console()
cli = typer.Typer()


@cli.command()
def clean():
    """
    Cleanup the resources used by the historian
    """
    docker_historian_util.clean()


@cli.command()
def stop():
    """
    Stop the Historian
    """
    docker_historian_util.stop()


@cli.command()
def status(
    moniker_historian: bool = False,
    moniker_emqx: bool = False,
    moniker_timescaledb: bool = False,
    is_docker_host: bool = False,
    return_str: bool = False
):
    """
    View the status of the running containers and the ports they are using

    Args:
        moniker_historian (bool, optional): Whether to show the moniker of the historian. Defaults to False.
        moniker_emqx (bool, optional): Whether to show the moniker of the emqx container. Defaults to False.
        moniker_timescaledb (bool, optional): Whether to show the moniker of the timescaledb container. Defaults to False.
        is_docker_host (bool, optional): Whether to show the docker host or system host to connect. Defaults to False.
    """
    output = None

    info_emqx = docker_util.get_info_container(
        docker_historian_util.CONTAINER_EMQX_NAME, is_docker_host=is_docker_host
    )
    info_timescaledb = docker_util.get_info_container(
        docker_historian_util.CONTAINER_TIMESCALEDB_NAME, is_docker_host=is_docker_host
    )
    info_historian = docker_util.get_info_container(
        docker_historian_util.CONTAINER_HISTORIAN_NAME, is_docker_host=is_docker_host
    )

    if moniker_historian:
        console.print(info_historian.get("moniker"))
        output = info_historian.get("moniker")
        if return_str:
            return output

    if moniker_emqx:
        console.print(info_emqx.get("moniker"))
        output = info_emqx.get("moniker")
        if return_str:
            return output

    if moniker_timescaledb:
        console.print(info_timescaledb.get("moniker"))
        output = info_timescaledb.get("moniker")
        if return_str:
            return output

    table = Table("Service", "Container Name", "Status", "Connection Details", "Ports")
    table.add_row(
        "EMQX",
        "emqx",
        info_emqx.get("status"),
        info_emqx.get("moniker"),
        info_emqx.get("ports"),
    )
    table.add_row(
        "TimescaleDB",
        "timescaledb",
        info_timescaledb.get("status"),
        info_timescaledb.get("moniker"),
        info_timescaledb.get("ports"),
    )
    table.add_row(
        "Historian",
        "historian",
        info_historian.get("status"),
        info_historian.get("moniker"),
        info_historian.get("ports"),
    )
    console.print(table)
    if return_str:
        return output

@cli.command()
def start():
    """
    Start the Historian
    """

    with console.status("Initializing Historian"):
        try:
            # First start all the dependency containers
            console.log("Creating EMQX")
            docker_historian_util.start_emqx()
            console.log("Creating TimescaleDB")
            docker_historian_util.start_timescaledb()
            # console.log("Creating Historian")

            # Then get the info
            console.log("Getting info for EMQX")
            info_emqx = docker_util.get_info_container(
                docker_historian_util.CONTAINER_EMQX_NAME,
                is_docker_host=True,
            )
            console.log("Getting info for TimescaleDB")
            info_timescaledb = docker_util.get_info_container(
                docker_historian_util.CONTAINER_TIMESCALEDB_NAME,
                is_docker_host=True,
            )

            # Finally start the historian itself
            console.log("Starting the Historian Sink")
            docker_historian_util.start_historian(
                info_timescaledb["moniker"], info_emqx["moniker"]
            )

            console.log("Created the containers.")

            # Run the status command
            status()
        except Exception as e:
            console.log(f"[red]Error ({type(e)}): {e}[/red]")
