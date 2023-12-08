# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import subprocess
import json

import pkg_resources
from jinja2 import Template

import composabl_core.utils.logger as logger_util

logger = logger_util.get_logger(__name__)


class KubernetesJobManager:

    def __init__(self, namespace="composabl-train"):
        self.namespace = namespace

    def check_kuberay(self):
        """
        Check that kuberay is installed
        """
        cmd = [
            "kubectl",
            "get",
            "deployment",
            "kuberay-operator",
            "-n",
            self.namespace,
            "-o",
            "name",
        ]

        try:
            out = subprocess.check_output(cmd)
            return out is not None
        except subprocess.CalledProcessError:
            return False

    def submit_rayjob(self, job_id, job_config_str):
        """
        Submit a RayJob resource to the cluster, using kubectl to apply a RayJob manifest
        """
        job_config = json.loads(job_config_str)

        # template_path = "../../templates/rayjob-template.yaml"
        template_path = pkg_resources.resource_filename("composabl_cli", "templates/rayjob-template.yaml")
        with open(template_path) as f:
            template = Template(f.read())
        # render template
        # variables:
        # - job_id: the job id
        # - composabl_version: version of the composabl SDK
        # - script_payload: the agent.py script
        # - worker_replicas: the amount of replicas
        # todo: define more variables
        # - definition for workers (resources/replicas/...)
        # - dependencies
        # - ray version
        # - configmap contents (code)

        runtime = job_config.get("runtime", {})
        additional_packages = []
        for i in range(len(job_config.get("additional_packages", []))):
            additional_packages[i] = job_config["additional_packages"][i]

        rendered = template.render(
            job_id=job_id,
            composabl_version="0.5.0",
            script_payload=job_config.get("payload", ""),
            worker_replicas=runtime.get("workers", "1"),
            worker_cpu=runtime.get("cpu", "1"),
            worker_memory=runtime.get("memory", "4Gi"),
            additional_packages=additional_packages
        )

        print(rendered)

        cmd = ["kubectl", "apply", "-f", "-", "-n", self.namespace]
        try:
            out = subprocess.check_output(cmd, input=rendered, text=True)
            return out is not None
        except subprocess.CalledProcessError:
            return False

    def print_logs(self, job_id):
        """
        Gets the logs of a RayJob using kubectl as described in the Ray documentation:
        https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/rayjob-quick-start.html#step-5-check-the-output-of-the-ray-job
        """
        cmd = [
            "kubectl",
            "logs",
            "-l",
            f"job-name=composabl-job-{job_id}",
            "-n",
            self.namespace,
            "-f",
        ]

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while process.poll() is None:
                stdout = process.stdout.readline()
                stderr = process.stderr.readline()
                if stdout:
                    logger.info(stdout.strip())
                if stderr:
                    logger.info(stderr.strip())

            # Todo: determine if this is actually needed
            final_stdin, final_stderr = process.communicate()
            if final_stdin:
                logger.info(final_stdin.strip())
            if final_stderr:
                logger.info(final_stderr.strip())
        except subprocess.CalledProcessError:
            return False
