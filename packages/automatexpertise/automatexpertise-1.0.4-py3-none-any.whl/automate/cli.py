# automate/cli.py

import click
from automate.core import create_container, list_containers, start_container, stop_container, delete_container

@click.group()
def cli():
    pass

@cli.command()
@click.argument('name')
def create(name):
    create_container(name)

@cli.command()
def list():
    list_containers()

@cli.command()
@click.argument('container_name')
def start(container_name):
    start_container(container_name)

@cli.command()
@click.argument('container_name')
def stop(container_name):
    stop_container(container_name)

@cli.command()
@click.argument('container_name')
def delete(container_name):
    delete_container(container_name)