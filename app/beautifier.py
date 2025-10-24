"""
Excel Formula Beautifier

Formats Excel formulas with proper indentation and line breaks for readability.
Handles nested functions and complex expressions.
"""

import re
from typing import Optional


class FormulaBeautifier:
    """Beautifies Excel formulas with indentation and line breaks."""

    # Functions that benefit from multi-line formatting
    MULTILINE_FUNCTIONS = {
        'IF', 'IFS', 'AND', 'OR', 'NOT', 'XOR',
        'SUMIF', 'SUMIFS', 'COUNTIF', 'COUNTIFS', 'AVERAGEIF', 'AVERAGEIFS',
        'LET', 'LAMBDA', 'FILTER', 'SORT', 'SORTBY',
        'VLOOKUP', 'HLOOKUP', 'XLOOKUP', 'INDEX', 'MATCH',
        'SWITCH', 'CHOOSE'
    }

    def __init__(self, indent_size: int = 4):
        """
        Initialize the beautifier.

        Args:
            indent_size: Number of spaces per indentation level
        """
        self.indent_size = indent_size

    def beautify(self, formula: str) -> str:
        """
        Beautify an Excel formula with proper formatting.

        Args:
            formula: The Excel formula to beautify (with or without leading =)

        Returns:
            Formatted formula string
        """
        if not formula or not formula.strip():
            return formula

        try:
            # Preserve the leading = if present
            has_equals = formula.strip().startswith('=')
            if has_equals:
                formula = formula.strip()[1:]

            # Format the formula
            formatted = self._format_expression(formula, 0)

            # Add back the = if it was there
            if has_equals:
                formatted = '=' + formatted

            return formatted
        except Exception:
            # If beautification fails, return the original formula
            return formula

    def _format_expression(self, expr: str, depth: int) -> str:
        """
        Recursively format an expression.

        Args:
            expr: Expression to format
            depth: Current nesting depth

        Returns:
            Formatted expression
        """
        expr = expr.strip()

        # Check if this is a function call
        func_match = re.match(r'^([A-Z_][A-Z0-9_.]*)\s*\(', expr, re.IGNORECASE)
        if func_match:
            func_name = func_match.group(1).upper()

            # Find the matching closing parenthesis
            args_start = func_match.end() - 1
            args_end = self._find_matching_paren(expr, args_start)

            if args_end == -1:
                return expr  # Malformed formula

            # Extract arguments
            args_str = expr[args_start + 1:args_end]
            rest = expr[args_end + 1:]

            # Split arguments
            args = self._split_arguments(args_str)

            # Format based on function type
            if func_name in self.MULTILINE_FUNCTIONS and len(args) > 1:
                formatted_args = self._format_multiline_args(args, depth)
                result = f"{func_name}(\n{formatted_args}\n{self._indent(depth)})"
            else:
                # Single line or simple functions
                formatted_args = ', '.join(self._format_expression(arg, depth + 1) for arg in args)
                result = f"{func_name}({formatted_args})"

            # Process any remaining expression
            if rest.strip():
                result += self._format_expression(rest, depth)

            return result

        return expr

    def _format_multiline_args(self, args: list[str], depth: int) -> str:
        """
        Format arguments across multiple lines with indentation.

        Args:
            args: List of argument strings
            depth: Current nesting depth

        Returns:
            Formatted arguments string
        """
        formatted = []
        for i, arg in enumerate(args):
            formatted_arg = self._format_expression(arg.strip(), depth + 1)

            # Add comma except for last argument
            if i < len(args) - 1:
                formatted_arg += ','

            formatted.append(self._indent(depth + 1) + formatted_arg)

        return '\n'.join(formatted)

    def _split_arguments(self, args_str: str) -> list[str]:
        """
        Split function arguments, respecting nested parentheses and quoted strings.

        Args:
            args_str: String containing comma-separated arguments

        Returns:
            List of argument strings
        """
        args = []
        current_arg = []
        paren_depth = 0
        in_string = False
        string_char = None

        for i, char in enumerate(args_str):
            # Handle string literals
            if char in ('"', "'") and (i == 0 or args_str[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None

            # Track parenthesis depth
            if not in_string:
                if char == '(':
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1
                elif char == ',' and paren_depth == 0:
                    # This comma separates arguments
                    args.append(''.join(current_arg))
                    current_arg = []
                    continue

            current_arg.append(char)

        # Add the last argument
        if current_arg:
            args.append(''.join(current_arg))

        return args

    def _find_matching_paren(self, text: str, start: int) -> int:
        """
        Find the matching closing parenthesis.

        Args:
            text: Text to search
            start: Index of opening parenthesis

        Returns:
            Index of matching closing parenthesis, or -1 if not found
        """
        depth = 0
        in_string = False
        string_char = None

        for i in range(start, len(text)):
            char = text[i]

            # Handle string literals
            if char in ('"', "'") and (i == 0 or text[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None

            # Track parenthesis depth
            if not in_string:
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                    if depth == 0:
                        return i

        return -1

    def _indent(self, depth: int) -> str:
        """
        Generate indentation string for given depth.

        Args:
            depth: Indentation level

        Returns:
            Indentation string
        """
        return ' ' * (depth * self.indent_size)


def beautify_formula(formula: str, indent_size: int = 4) -> str:
    """
    Convenience function to beautify an Excel formula.

    Args:
        formula: The Excel formula to beautify
        indent_size: Number of spaces per indentation level

    Returns:
        Beautified formula string
    """
    beautifier = FormulaBeautifier(indent_size=indent_size)
    return beautifier.beautify(formula)
