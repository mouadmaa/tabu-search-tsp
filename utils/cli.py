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

    return parser.parse_args()
