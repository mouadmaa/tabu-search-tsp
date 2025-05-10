"""
Command-line interface utilities for the Traveling Salesman Problem.
Contains functions for parsing and handling command-line arguments.
"""

import argparse


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Visualize Moroccan cities for the Traveling Salesman Problem')

    parser.add_argument('--save-plot', action='store_true',
                       help='Save the visualization to a file instead of displaying it')
    parser.add_argument('--output', type=str, default='morocco_cities.png',
                       help='Output filename for the visualization (if --save-plot is used)')
    parser.add_argument('--verbose', action='store_true',
                       help='Print detailed progress information')
    parser.add_argument('--start-city', type=int, 
                       help='Starting city index for the nearest neighbor tour (random if not specified)')

    # Add optimization-related arguments
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=1000,
        help="Maximum number of iterations for optimization"
    )
    
    parser.add_argument(
        "--time-limit",
        type=int,
        default=60,
        help="Time limit in seconds for optimization"
    )
    
    parser.add_argument(
        "--no-swap",
        action="store_true",
        help="Disable city swap operations (use only 2-opt)"
    )
    
    parser.add_argument(
        "--no-prioritize-2opt",
        action="store_true",
        help="Don't prioritize 2-opt moves over city swaps"
    )
    
    # Add tabu search specific arguments
    parser.add_argument(
        "--tabu-tenure",
        type=int,
        default=10,
        help="Number of iterations a move remains tabu"
    )
    
    parser.add_argument(
        "--no-aspiration",
        action="store_true",
        help="Disable aspiration criteria in tabu search"
    )
    
    return parser.parse_args()
