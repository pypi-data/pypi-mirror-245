# coding=utf-8
import click
import sys


import eulerpublisher.publisher.publisher as pb
from eulerpublisher.container.ai.ai import AiPublisher


@click.group(
    name="ai",
    help="Command for publishing openeuler AI container images"
)
def group():
    pass


@group.command(
    name="build",
    help="Build openEuler AI image"
)
@click.option(
    "-p",
    "--repo",
    default="",
    help="The target repository to push AI image to. "
    "This option is required while option `--multiPublish`"
    " is not set.",
)
@click.option(
    "-g",
    "--registry",
    default="docker.io",
    help="The registry where to push the built AI "
    "image. The default registry is `docker.io`"
    ", users can choose others such like `quay.io`,"
    " `hub.oepkgs.net`, etc.. While option `--multiPublish`"
    " is set, `--registry` is no longer needed.",
)
@click.option(
    "-a", "--arch", required=True, help="The architecture of required AI image."
)
@click.option(
    "-f",
    "--dockerfile",
    required=True,
    help="The dockerfile to define AI image, "
    "users must enter the path of dockerfile.",
)
@click.option(
    "-t",
    "--tag",
    required=True,
    help="The AI container image tag, it usually consists of "
    "SDK, AI framework, and/or LLM information.",
)
@click.option(
    "-m",
    "--mpublish",
    is_flag=True,
    help="This option decides whether to publish the image product to "
    "multiple repositories. While using this option, users may first "
    "provide the yaml file by `export EP_LOGIN_FILE=your_yaml_path`, "
    "which includes login information of all target repositories. "
    "The default target repositories are provided in "
    "etc/container/registry.yaml. In this situation,the options "
    "`--repo` and `--registry` are no longer needed.",
)
def build(repo, registry, arch, dockerfile, tag, mpublish):
    if (not mpublish) and (not repo):
        raise TypeError("[Build] `--repo` option is required. ")
    obj = AiPublisher(
        repo=repo,
        registry=registry,
        arch=arch,
        dockerfile=dockerfile,
        tag=tag,
        multi=mpublish,
    )
    ret = obj.build()
    if ret != pb.PUBLISH_SUCCESS:
        sys.exit(1)
    sys.exit(0)


@group.command(
    name="push",
    help="Push openEuler AI image to target repository(s)"
)
@click.option(
    "-p",
    "--repo",
    default="",
    help="The target repository to push AI image to. "
    "This option is required while option `--multiPublish`"
    " is not set.",
)
@click.option(
    "-g",
    "--registry",
    default="docker.io",
    help="The registry where to push the built AI "
    "image. The default registry is `docker.io`"
    ", users can choose others such like `quay.io`,"
    " `hub.oepkgs.net`, etc.. While option `--multiPublish`"
    " is set, `--registry` is no longer needed.",
)
@click.option(
    "-t",
    "--tag",
    required=True,
    help="Tag of the AI container image needs to push",
)
@click.option(
    "-m",
    "--mpublish",
    is_flag=True,
    help="This option decides whether to publish the image product to "
    "multiple repositories. While using this option, users may first "
    "provide the yaml file by `export EP_LOGIN_FILE=your_yaml_path`, "
    "which includes login information of all target repositories. "
    "The default target repositories are provided in "
    "etc/container/registry.yaml. In this situation,the options "
    "`--repo` and `--registry` are no longer needed.",
)
def push(repo, registry, tag, mpublish):
    if (not mpublish) and (not repo):
        raise TypeError("[Push] `--repo` option is required. ")
    obj = AiPublisher(repo=repo, registry=registry, tag=tag, multi=mpublish)
    ret = obj.push()
    if ret != pb.PUBLISH_SUCCESS:
        sys.exit(1)
    sys.exit(0)


@group.command(
    name="publish",
    help="Publish openEuler AI image to target repository(s)"
)
@click.option(
    "-a",
    "--arch",
    required=True,
    help="The architecture of required AI image."
)
@click.option(
    "-p",
    "--repo",
    default="",
    help="The target repository to push AI image to. "
    "This option is required while option `--multiPublish`"
    " is not set.",
)
@click.option(
    "-g",
    "--registry",
    default="docker.io",
    help="The registry where to push the built AI "
    "image. The default registry is `docker.io`"
    ", users can choose others such like `quay.io`,"
    " `hub.oepkgs.net`, etc.. While option `--multiPublish`"
    " is set, `--registry` is no longer needed.",
)
@click.option(
    "-f",
    "--dockerfile",
    required=True,
    help="The dockerfile to define AI image, "
    "users must enter the path of dockerfile.",
)
@click.option(
    "-t",
    "--tag",
    required=True,
    help="The AI container image tag, it usually consists of "
    "SDK, AI framework, and/or LLM information.",
)
@click.option(
    "-m",
    "--mpublish",
    is_flag=True,
    help="This option decides whether to publish the image product to "
    "multiple repositories. While using this option, users may first "
    "provide the yaml file by `export EP_LOGIN_FILE=your_yaml_path`, "
    "which includes login information of all target repositories. "
    "The default target repositories are provided in "
    "etc/container/registry.yaml. In this situation,the options "
    "`--repo` and `--registry` are no longer needed.",
)
def publish(arch, repo, registry, dockerfile, tag, mpublish):
    if (not mpublish) and (not repo):
        raise TypeError("[Publish] `--repo` option is required. ")
    obj = AiPublisher(
        arch=arch,
        repo=repo,
        registry=registry,
        dockerfile=dockerfile,
        tag=tag,
        multi=mpublish,
    )
    ret = obj.build()
    if ret != pb.PUBLISH_SUCCESS:
        sys.exit(1)
    ret = obj.push()
    if ret != pb.PUBLISH_SUCCESS:
        sys.exit(1)
    sys.exit(0)
