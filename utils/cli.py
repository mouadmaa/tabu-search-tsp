import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Traveling Salesman Problem solver using Tabu Search optimization',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--max-iterations", "-i",
        type=int,
        default=3000,
        help="Maximum number of iterations (1000-5000 recommended)"
    )

    parser.add_argument(
        "--tabu-tenure", "-tt",
        type=str,
        default="sqrt",
        help="Tabu tenure: Either a number, 'sqrt' (√n), or 'log' (log(n) * 3)"
    )

    parser.add_argument(
        "--time-limit", "-t",
        type=int,
        default=60,
        help="Time limit in seconds for optimization"
    )

    parser.add_argument(
        "--max-no-improvement",
        type=int,
        default=None,
        help="Stop after N iterations without improvement"
    )

    parser.add_argument(
        "--show-performance",
        action="store_true",
        default=False,
        help="Display a simple performance report figure after optimization"
    )

    parser.add_argument(
        "--save-performance",
        type=str,
        metavar="FILENAME",
        help="Save the performance report to a file"
    )

    parser.add_argument(
        "--tour-selection",
        action="store_true",
        default=False,
        help="When True, prompts for city selection. When False (default), randomly selects cities."
    )
    
    args = parser.parse_args()

    if args.tabu_tenure.lower() not in ["sqrt", "log"]:
        try:
            args.tabu_tenure = int(args.tabu_tenure)
        except ValueError:
            print(f"Warning: Invalid tabu tenure '{args.tabu_tenure}'. Using 'sqrt' instead.")
            args.tabu_tenure = "sqrt"

    return args
