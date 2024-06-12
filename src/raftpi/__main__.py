import click
import logging

@click.command()
@click.option('--verbose', '-v', is_flag=True, help="Will print verbose messages.")
def raftpi(verbose):
    """Begin a raft node instance."""
    if verbose:
        logging.basicConfig(level=logging.INFO)
        logging.info("Verbose mode on")
    else:
        logging.basicConfig(level=logging.WARNING)
    logging.info("Raft node started")
    
if __name__ == "__main__":
    raftpi()

