# coding=utf-8
import click
import os
import shutil
import subprocess
import yaml


import eulerpublisher.publisher.publisher as pb
from eulerpublisher.publisher import EP_PATH


DEFAULT_REGISTRY = EP_PATH + "container/ai/registry.yaml"
DEFAULT_WORKDIR = "/tmp/eulerpublisher/container/ai/"


def _get_tags(repository, tag, multi):
    repo_list = []
    if not multi:
        repo_list.append(repository)
    else:
        with open(multi, "r") as f:
            env = yaml.safe_load(f)
        for key in env:
            repo_list.append(str(env[key][2]))
    # tag image for all registries
    tags_bulid = ""
    tags_push = []
    for repo in repo_list:
        tags_bulid += "-t " + repo + ":" + tag
        tags_bulid += " "
        tags_push.append(repo + ":" + tag)
    return tags_bulid, tags_push


class AiPublisher(pb.Publisher):
    def __init__(
        self, repo="", registry="", tag="", arch="", dockerfile="", multi=False
    ):
        self.registry=registry
        self.dockerfile = os.path.abspath(dockerfile)
        # get multiple-registry yaml path
        if multi:
            if (not "EP_LOGIN_FILE" in os.environ) or (not os.environ["EP_LOGIN_FILE"]):
                self.multi_file = DEFAULT_REGISTRY
            else:
                self.multi_file = os.path.abspath(os.environ["EP_LOGIN_FILE"])
        else:
            self.multi_file = ""

        self.tags_build, self.tags_push = _get_tags(
            repository=registry + "/" + repo, tag=tag, multi=self.multi_file
        )

        # architecture of required image
        if arch == "aarch64":
            self.platform = "linux/arm64"
        elif arch == "x86_64":
            self.platform = "linux/amd64"
        # workdir
        if (not "EP_AI_WORKDIR" in os.environ) or (not os.environ["EP_AI_WORKDIR"]):
            self.workdir = DEFAULT_WORKDIR
        else:
            self.workdir = os.path.abspath(os.environ["EP_AI_WORKDIR"])

    def build(self):
        try:
            if not os.path.exists(self.workdir):
                os.makedirs(self.workdir)
            os.chdir(self.workdir)
            shutil.copy2(self.dockerfile, "./")
            # ensure qemu is installed
            if pb.check_qemu() != pb.PUBLISH_SUCCESS:
                return pb.PUBLISH_FAILED
            # ensure the docker is starting
            if pb.start_docker() != pb.PUBLISH_SUCCESS:
                return pb.PUBLISH_FAILED
            # build images with 'buildx'
            builder = pb.create_builder()
            if (
                subprocess.call(
                    "docker buildx build "
                    + "--platform "
                    + self.platform
                    + " "
                    + self.tags_build
                    + "--load .",
                    shell=True,
                )
                != 0
            ):
                return pb.PUBLISH_FAILED
            subprocess.call(["docker", "buildx", "stop", builder])
            subprocess.call(["docker", "buildx", "rm", builder])
        except (OSError, subprocess.CalledProcessError) as err:
            click.echo(click.style(f"[Build] {err}", fg="red"))
        click.echo("[Build] finished")
        return pb.PUBLISH_SUCCESS

    def push(self):
        try:
            # login registry
            if (
                pb.login_registry(registry=self.registry, multi=self.multi_file)
                != pb.PUBLISH_SUCCESS
            ):
                return pb.PUBLISH_FAILED
            # push
            for tag in self.tags_push:
                if (
                    subprocess.call(
                        "docker push " + tag,
                        shell=True,
                    )
                    != 0
                ):
                    return pb.PUBLISH_FAILED
        except (OSError, subprocess.CalledProcessError) as err:
            click.echo(click.style(f"[Push] {err}", fg="red"))
        click.echo("[Push] finished")
        return pb.PUBLISH_SUCCESS
