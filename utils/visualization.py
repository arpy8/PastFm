"""Visualization utilities for the PastFm application."""

import random
from typing import List


def generate_css_bar(num_bar: int = 75) -> str:
    """
    Generate CSS for animated audio visualization bars.

    Args:
        num_bar: Number of bars to generate

    Returns:
        CSS string for the animated bars
    """
    css_elements: List[str] = []
    left_position = 1

    for i in range(1, num_bar + 1):
        animation_duration = random.randint(350, 500)
        css_elements.append(
            f".bar:nth-child({i}) {{ left: {left_position}px; animation-duration: {animation_duration}ms; }}"
        )
        left_position += 4

    return "\n".join(css_elements)


def generate_bar_elements(num_bar: int = 75) -> str:
    """
    Generate HTML div elements for visualization bars.

    Args:
        num_bar: Number of bar elements to generate

    Returns:
        HTML string containing div elements
    """
    return "".join(["<div class='bar'></div>" for _ in range(num_bar)])
