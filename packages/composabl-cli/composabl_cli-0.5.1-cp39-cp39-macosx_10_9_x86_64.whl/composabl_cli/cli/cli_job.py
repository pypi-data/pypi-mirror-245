# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import asyncio
import datetime
import threading
import time
import os
import traceback
from typing import Optional

import typer

from composabl_core.utils import dependency_util, kubernetes_util, logger as logger_util
from composabl_cli.k8s import kubernetes_job_mgr


logger = logger_util.get_logger(__name__)
cli = typer.Typer()


def wait_until_status(client, job_id, status_to_wait_for, timeout_seconds=1000):
    start = time.time()

    logger.info(f"Waiting for job {job_id} to finish")

    while time.time() - start <= timeout_seconds:
        status = client.get_job_status(job_id)
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # We poll more, but let the user know less when we are polling
        if int(time.time()) % 60 == 0:
            logger.info(f"[{job_id}][{t}] {status}")

        if status in status_to_wait_for:
            break

        time.sleep(1)


async def tail_logs(client, job_id):
    async for lines in client.tail_job_logs(job_id):
        lines = lines.strip()
        lines_splitted = lines.split("\n")

        for line in lines_splitted:
            logger.info(line)


def get_dependencies(path_sdk: Optional[str] = None):
    """
    Get the dependencies for the test
    """
    dependencies = ["composabl"]

    if path_sdk:
        path_sdk_abs = os.path.realpath(path_sdk)

        # Gather and install our entire SDK on the cluster
        dependencies = dependency_util.generate_requirements_from_pyprojects(
            [
                f"{path_sdk_abs}/composabl_core/pyproject.toml",
                f"{path_sdk_abs}/composabl_train/pyproject.toml",
                f"{path_sdk_abs}/composabl/pyproject.toml",
            ]
        )

        # Remove all entries that start with composabl from the dependencies list
        dependencies = [
            dependency
            for dependency in dependencies
            if not dependency.startswith("composabl")
        ]

    return dependencies


@cli.command()
def list():
    """
    List all the running jobs
    """
    # Submit the Job to the cluster
    # TODO: This is dangerous, as we expect ray as a dependency to be installed locally
    # while this is not part (and should not) of the composabl_core package
    from ray.job_submission import JobSubmissionClient

    # Start Port Forwarding the cluster API
    logger.info("Forwarding the Ray Dashboard port")
    port_forward_thread = kubernetes_util.PortForwarder(
        "service/raycluster-kuberay-head-svc", 8265, namespace="composabl-ray"
    )
    port_forward_thread.start()
    time.sleep(2)

    # Create a submission client
    client = JobSubmissionClient("http://localhost:8265")

    # List all the jobs
    # See: https://docs.ray.io/en/latest/cluster/running-applications/job-submission/doc/ray.job_submission.JobDetails.html#ray.job_submission.JobDetails
    jobs = client.list_jobs()

    for job in jobs:
        if job.status != "RUNNING" and job.status != "PENDING":
            continue

        logger.info(f"[{job.submission_id}][{job.job_id}] {job.status}")

    port_forward_thread.stop()


@cli.command()
def stop(job_id: str):
    """
    Stop the provided job
    """
    # Submit the Job to the cluster
    # TODO: This is dangerous, as we expect ray as a dependency to be installed locally
    # while this is not part (and should not) of the composabl_core package
    from ray.job_submission import JobSubmissionClient

    # Start Port Forwarding the cluster API
    logger.info("Forwarding the Ray Dashboard port")
    port_forward_thread = kubernetes_util.PortForwarder(
        "service/raycluster-kuberay-head-svc", 8265, namespace="composabl-ray"
    )
    port_forward_thread.start()
    time.sleep(2)

    # Create a submission client
    client = JobSubmissionClient("http://localhost:8265")

    # List all the jobs
    # See: https://docs.ray.io/en/latest/cluster/running-applications/job-submission/doc/ray.job_submission.JobDetails.html#ray.job_submission.JobDetails
    client.stop_job(job_id)

    port_forward_thread.stop()


@cli.command()
def submit(path: str = ".", path_sdk: Optional[str] = None, json: Optional[str] = None):
    """
    Submit the current agent in the provided directory to the cluster

    Args:
        path (str, optional): The path to the agent. Defaults to ".".
        path_sdk (Optional[str], optional): The path to the SDK directory for the SDK. Defaults to None. This is used in debugging mode for development
        json (Optional[str], optional): A job, json serialized, from the nocode app
    """
    try:
        # Ensure the license key is set
        if "COMPOSABL_LICENSE" not in os.environ:
            raise Exception(
                "You must set the COMPOSABL_LICENSE environment variable to run this command"
            )

        if json:
            # Submit the Job as a RayJob using k8s_job_mgr
            job_mgr = kubernetes_job_mgr.KubernetesJobManager()
            if not job_mgr.check_kuberay():
                logger.error("Current cluster does not have kuberay installed - rerun the install script for composabl")
                return
            job_mgr.submit_rayjob("test", json)
            job_mgr.print_logs("test")
            return

        # Parse the relative path as absolute one
        file_path_root = os.path.abspath(path)

        # Submit the Job to the cluster
        # TODO: This is dangerous, as we expect ray as a dependency to be installed locally
        # while this is not part (and should not) of the composabl_core package
        from ray.job_submission import JobStatus, JobSubmissionClient

        # Start Port Forwarding the cluster API
        logger.info("Forwarding the Ray Dashboard port")
        port_forward_thread = kubernetes_util.PortForwarder(
            "service/raycluster-kuberay-head-svc", 8265, namespace="composabl-ray"
        )
        port_forward_thread.start()
        time.sleep(2)

        # Create a submission client
        client = JobSubmissionClient("http://localhost:8265")
        license_key = os.environ["COMPOSABL_LICENSE"]

        entrypoint_cmd = (
            # Set the license key and agree to the EULA
            f"export COMPOSABL_LICENSE='{license_key}';"
            "export COMPOSABL_EULA_AGREED=1;"
            # Run the demo agent
            "LOGLEVEL=debug python main.py"
        )

        dependencies = get_dependencies(path_sdk)

        logger.info(f"Using dependencies: {dependencies}")

        runtime_env = {
            "working_dir": file_path_root,  # path what we are executing"
            "pip": {"packages": dependencies},
        }

        if path_sdk:
            path_sdk_abs = os.path.realpath(path_sdk)

            logger.info(f"Using SDK at '{path_sdk_abs}'")

            runtime_env["py_modules"] = [
                f"{path_sdk_abs}/composabl_core/composabl_core",
                f"{path_sdk_abs}/composabl_train/composabl_train",
                f"{path_sdk_abs}/composabl/composabl",
            ]

        # Create the job
        job_id = client.submit_job(
            entrypoint=str(entrypoint_cmd),
            runtime_env=runtime_env,
        )

        # Start a watcher for the test status
        thread_watcher = threading.Thread(
            target=wait_until_status,
            args=(
                client,
                job_id,
                {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED},
            ),
        )

        thread_watcher.daemon = True
        thread_watcher.start()

        # Show the logs
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tail_logs(client, job_id))

        # Stop when the thread stops
        thread_watcher.join()

    except Exception as e:
        logger.debug(traceback.format_exc())
        logger.error(f"Failed to submit the job: {e}")
    finally:
        # Kill the job (make sure client and job_id are defined)
        if "client" in locals() and "job_id" in locals():
            logger.info("Killing the job")
            client.stop_job(job_id)

        # Kill the port forwarding
        logger.info("Stopping the port forwarding")
        if "port_forward_thread" in locals():
            port_forward_thread.stop()
