# coding=utf-8
import click
import docker
import os
import re
import shutil
import subprocess
import yaml


import eulerpublisher.publisher.publisher as pb
from eulerpublisher.publisher import EP_PATH
from eulerpublisher.publisher import OPENEULER_REPO

CACHE_DATA_PATH = "/tmp/eulerpublisher/container/openeuler/"
DOCKERFILE_PATH = EP_PATH + "container/openeuler/Dockerfile"
TAGS = EP_PATH + "container/openeuler/tags.yaml"
DEFAULT_REGISTRY = EP_PATH + "container/openeuler/registry.yaml"


# tag image
def _get_tags(repository, version, multi):
    repo_list = []
    if not multi:
        repo_list.append(repository)
    else:
        with open(multi, "r") as f:
            env = yaml.safe_load(f)
        for key in env:
            repo_list.append(str(env[key][2]))
    # tag image for all registries
    tags = ""
    for repo in repo_list:
        tags += "-t " + repo + ":" + version.lower()
        with open(TAGS, "r") as f:
            data = yaml.safe_load(f)
        version = version.upper()
        if version in data:
            for tag in data[version]:
                tags += " -t " + repo + ":" + str(tag)
        tags += " "
    return tags


# Run container and compare the result with 'param'
def _run(tag="", cmd="", param=""):
    ret = pb.PUBLISH_FAILED
    try:
        client = docker.from_env()
        container = client.create_container(image=tag, command=cmd, detach=True)
        client.start(container)
        subprocess.call("docker logs " + container["Id"] + " >>logs.txt", shell=True)
        logs = open("logs.txt")
        for line in logs:
            if param in line:
                ret = pb.PUBLISH_SUCCESS
        logs.close()
        subprocess.call(["rm", "-rf", "logs.txt"])
        client.stop(container)
    except docker.errors.DockerException as err:
        click.echo(click.style(f"[run_container] {err}", fg="red"))
    return ret


# Class for publishing openEuler container images
class OePublisher(pb.Publisher):
    def __init__(
        self, repo="", version="", registry="", index="", dockerfile="", multi=False
    ):
        self.repo = repo
        self.version = version
        self.registry = registry
        self.index = index
        # get Dockerfile path
        if dockerfile:
            self.dockerfile = os.path.abspath(dockerfile)
        else:
            self.dockerfile = DOCKERFILE_PATH

        # get multiple-registry yaml path
        if multi:
            if (not "EP_LOGIN_FILE" in os.environ) or (not os.environ["EP_LOGIN_FILE"]):
                self.multi_file = DEFAULT_REGISTRY
            else:
                self.multi_file = os.path.abspath(os.environ["EP_LOGIN_FILE"])
        else:
            self.multi_file = ""

        # get all tags
        self.tags = _get_tags(
            repository=self.registry + "/" + self.repo,
            version=self.version,
            multi=self.multi_file,
        )

    def prepare(self):
        os.makedirs(CACHE_DATA_PATH, exist_ok=True)
        os.chdir(CACHE_DATA_PATH)
        os.makedirs(self.version, exist_ok=True)
        shutil.copy2(self.dockerfile, self.version + "/Dockerfile")
        os.chdir(self.version)

        for arch in pb.ARCHS:
            if arch == "x86_64":
                docker_arch = "amd64"
            elif arch == "aarch64":
                docker_arch = "arm64"
            # download base images
            index = (
                "openEuler-"
                + self.version.upper()
                + "/"
                + self.index
                + "/"
                + arch
                + "/"
            )
            file_name = "openEuler-docker." + arch + ".tar.xz"
            if not os.path.exists(file_name):
                download_url = OPENEULER_REPO + index + file_name
                if pb.download(download_url) != pb.PUBLISH_SUCCESS:
                    return pb.PUBLISH_FAILED
                click.echo("\n[Prepare] Download %s successfully." % file_name)
            # check
            sha256sum = file_name + ".sha256sum"
            subprocess.call(["rm", "-rf", sha256sum])
            sha256sum_url = OPENEULER_REPO + index + sha256sum
            if pb.download(sha256sum_url) != pb.PUBLISH_SUCCESS:
                return pb.PUBLISH_FAILED
            click.echo("\n[Prepare] Download %s successfully." % sha256sum)
            subprocess.call(["shasum", "-c", sha256sum])
            # get rootfs
            rootfs = "openEuler-docker-rootfs." + docker_arch + ".tar.xz"
            if os.path.exists(rootfs):
                continue
            tar_cmd = [
                "tar",
                "-xf",
                file_name,
                "--exclude",
                "layer.tar",
            ]
            subprocess.call(tar_cmd)
            for file in os.listdir("."):
                if file.endswith(".tar") and not re.search("openEuler", file):
                    os.rename(file, "openEuler-docker-rootfs." + docker_arch + ".tar")
                    subprocess.call(
                        ["xz", "-z", "openEuler-docker-rootfs." + docker_arch + ".tar"]
                    )
        click.echo("[Prepare] finished")
        return pb.PUBLISH_SUCCESS

    def build_and_push(self):
        try:
            os.chdir(CACHE_DATA_PATH)
            # ensure qemu is installed so that it can build multi-platform images
            if pb.check_qemu() != pb.PUBLISH_SUCCESS:
                return pb.PUBLISH_FAILED
            # ensure the docker is starting
            if pb.start_docker() != pb.PUBLISH_SUCCESS:
                return pb.PUBLISH_FAILED
            # login registry
            if (
                pb.login_registry(registry=self.registry, multi=self.multi_file)
                != pb.PUBLISH_SUCCESS
            ):
                return pb.PUBLISH_FAILED
            # build mutil-platform images with 'buildx'
            builder = pb.create_builder()
            # build and push docker image
            os.chdir(self.version)
            if (
                subprocess.call(
                    "docker buildx build "
                    + "--platform linux/arm64,linux/amd64 "
                    + self.tags
                    + " --push "
                    + ".",
                    shell=True,
                )
                != 0
            ):
                return pb.PUBLISH_FAILED
            subprocess.call(["docker", "buildx", "stop", builder])
            subprocess.call(["docker", "buildx", "rm", builder])
        except (OSError, subprocess.CalledProcessError) as err:
            click.echo(click.style(f"[Build and Push] {err}", fg="red"))
        click.echo("[Build and Push] finished")
        return pb.PUBLISH_SUCCESS

    # To test the new image，you should first pull it
    def check(self):
        result = pb.PUBLISH_SUCCESS
        try:
            client = docker.from_env()
            if self.registry == "docker.io":
                image_tag = self.repo + ":" + self.version
            else:
                image_tag = self.registry + "/" + self.repo + ":" + self.version
            image = client.images(name=image_tag)
            if image == []:
                click.echo("Pulling " + image_tag + "...")
                client.pull(image_tag)
            # check basic information of new image
            image = client.images(name=image_tag)
            image_info = client.inspect_image(image[0]["Id"])
            for tag in image[0]["RepoTags"]:
                if tag == image_tag:
                    # check OS type
                    if image_info["Os"] != "linux":
                        click.echo(
                            click.style(
                                "[Check] OS type <%s> is unknown." % image_info["Os"],
                                fg="red",
                            )
                        )
                        result = pb.PUBLISH_FAILED
                    # check platform type
                    if (
                        image_info["Architecture"] != "amd64"
                        and image_info["Architecture"] != "arm64"
                    ):
                        click.echo(
                            click.style(
                                "[Check] Architecture <%s> is not expected."
                                % image_info["Architecture"],
                                fg="red",
                            )
                        )
                        result = pb.PUBLISH_FAILED

            # test time zone settings
            if _run(tag=image_tag, cmd="date", param="UTC") != pb.PUBLISH_SUCCESS:
                click.echo(
                    click.style("[Check] time zone setting is not UTC", fg="red")
                )
                result = pb.PUBLISH_FAILED
        except docker.errors.DockerException as err:
            click.echo(click.style(f"[Check] {err}", fg="red"))
        click.echo("[Check] finished")
        return result

    # Publish with one click
    def publish(self):
        click.echo("\n[Publish] start to publish openEuler-" + self.version + "...")
        if self.prepare() != pb.PUBLISH_SUCCESS:
            click.echo(click.style("[Publish] Download failed.", fg="red"))
            return pb.PUBLISH_FAILED
        if self.build_and_push() != pb.PUBLISH_SUCCESS:
            click.echo(click.style("[Publish] Build and push failed.", fg="red"))
            return pb.PUBLISH_FAILED
        click.echo("[Publish] finished")
        return pb.PUBLISH_SUCCESS
