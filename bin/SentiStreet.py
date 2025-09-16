import yaml
import os
import argparse
import logging

from SentiStreet.lib.utils import run_all


def _args():
    parser = argparse.ArgumentParser(
        description="CLI tool to generate and analyze daily reports",
    )

    parser.add_argument(
        'c', '--config',
        required=True,
        help='Path to config file'
    )

    return parser.parse_args()


def _logger(verbose=False):
    logger = logging.getLogger(__name__)

    # Set log level based on verbose flag
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)

    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


def main():
    
    clargs = _args()
    config_file = clargs.config
    verbose = clargs.verbose

    logger = _logger(verbose)

    if not os.path.exists(config_file):
        raise FileNotFoundError("Error: invalid config file path")

    with open(config_file) as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    return run_all(cfg, logger)


if __name__ == "__main__":
    main()