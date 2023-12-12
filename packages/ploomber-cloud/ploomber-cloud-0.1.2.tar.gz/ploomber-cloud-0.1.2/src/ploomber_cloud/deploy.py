import click

from ploomber_cloud import api, zip_
from ploomber_cloud.config import PloomberCloudConfig


def deploy():
    """Deploy a project to Ploomber Cloud, requires a project to be initialized"""
    client = api.PloomberCloudClient()
    config = PloomberCloudConfig()
    config.load()

    with zip_.zip_app(verbose=True) as path_to_zip:
        click.echo("Deploying...")
        client.deploy(
            path_to_zip=path_to_zip,
            project_type=config.data["type"],
            project_id=config.data["id"],
        )
