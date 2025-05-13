import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Traveling Salesman Problem using Tabu Search optimization',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--show-performance",
        action="store_true",
        default=False,
        help="Display a simple performance report figure after optimization"
    )

    parser.add_argument(
        "--tour-selection",
        action="store_true",
        default=False,
        help="When True, prompts for city selection. When False (default), randomly selects cities."
    )
    
    return parser.parse_args()
