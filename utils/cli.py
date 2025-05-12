"""
Command-line interface utilities for the Traveling Salesman Problem.
Contains functions for parsing and handling command-line arguments.
"""

import argparse


import argparse


def parse_arguments():
    """
    Parse command-line arguments for the TSP visualization and tabu search optimization.
    
    Focuses on key parameters that most significantly affect solution quality:
    - Iterations and tabu tenure to balance exploration vs. exploitation
    - Time limits for practical runtime constraints
    - Visualization options for result display
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Traveling Salesman Problem solver using Tabu Search optimization',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Core tabu search parameters
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

    # Performance visualization options
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

    # Tour selection options
    parser.add_argument(
        "--tour-selection",
        action="store_true",
        default=False,
        help="When True, prompts for city selection. When False (default), randomly selects cities."
    )
    
    args = parser.parse_args()
    
    # Process the tabu tenure parameter
    if args.tabu_tenure.lower() not in ["sqrt", "log"]:
        try:
            args.tabu_tenure = int(args.tabu_tenure)
        except ValueError:
            print(f"Warning: Invalid tabu tenure '{args.tabu_tenure}'. Using 'sqrt' instead.")
            args.tabu_tenure = "sqrt"
    
    return args
