import click
import uvicorn
import logging
from raftpi.node.node import Node
import socket
import asyncio


def _get_ip():
    return socket.gethostbyname(socket.gethostname())


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Will print verbose messages.")
@click.option("--neighbors", "-n", default=[], help="List of neighbors of the node.")
def raftpi(verbose: bool, neighbors: list[str]):
    """Begin a raft node instance."""
    if verbose:
        logging.basicConfig(level=logging.INFO)
        logging.info("Verbose mode on")
    else:
        logging.basicConfig(level=logging.WARNING)
    logging.info("Raft node started")

    node = Node(neighbors)
    asyncio.run(node.start())


if __name__ == "__main__":
    raftpi()
