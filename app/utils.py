"""
Utility functions for the Excel Formula Optimizer application.
"""

from typing import Optional


def validate_formula(formula: str) -> tuple[bool, Optional[str]]:
    """
    Validate an Excel formula.

    Args:
        formula: The formula to validate

    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is None
    """
    if not formula or not formula.strip():
        return False, "Formula cannot be empty"

    formula = formula.strip()

    # Basic validation - must contain some content
    if len(formula) < 1:
        return False, "Formula is too short"

    # Check for balanced parentheses
    if not _has_balanced_parentheses(formula):
        return False, "Unbalanced parentheses in formula"

    return True, None


def _has_balanced_parentheses(formula: str) -> bool:
    """
    Check if parentheses are balanced in the formula.

    Args:
        formula: Formula to check

    Returns:
        True if balanced, False otherwise
    """
    depth = 0
    in_string = False
    string_char = None

    for i, char in enumerate(formula):
        # Handle string literals
        if char in ('"', "'") and (i == 0 or formula[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None

        # Track parenthesis depth (only outside strings)
        if not in_string:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                # If we go negative, we have a closing paren without opening
                if depth < 0:
                    return False

    # Must end at depth 0
    return depth == 0


def sanitize_formula(formula: str) -> str:
    """
    Sanitize a formula for processing.

    Args:
        formula: Formula to sanitize

    Returns:
        Sanitized formula
    """
    # Remove excessive whitespace
    formula = formula.strip()

    # Remove any leading/trailing quotes that might have been added accidentally
    if formula.startswith('"') and formula.endswith('"'):
        formula = formula[1:-1]

    return formula
