"""
AI Agent for Excel Formula Optimization

Uses Claude (Anthropic) to suggest optimized and simplified Excel formulas.
"""

import os
from typing import Optional
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FormulaOptimizerAgent:
    """AI agent that optimizes and simplifies Excel formulas using Claude."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the optimizer agent.

        Args:
            api_key: Anthropic API key. If not provided, reads from ANTHROPIC_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def optimize_formula(self, formula: str, beautified: str) -> dict[str, str]:
        """
        Optimize and simplify an Excel formula using Claude.

        Args:
            formula: The original Excel formula
            beautified: The beautified version of the formula

        Returns:
            Dictionary with keys:
                - simplified: The optimized formula
                - comment: Explanation of the optimization
        """
        try:
            prompt = self._create_optimization_prompt(formula, beautified)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse the response
            result = self._parse_response(response.content[0].text)
            return result

        except Exception as e:
            # If AI fails, return fallback response
            return {
                "simplified": formula,
                "comment": f"Unable to optimize formula: {str(e)}"
            }

    def _create_optimization_prompt(self, formula: str, beautified: str) -> str:
        """
        Create the prompt for Claude to optimize the formula.

        Args:
            formula: Original formula
            beautified: Beautified version

        Returns:
            Prompt string
        """
        return f"""You are an Excel formula optimization expert. Your task is to analyze and improve Excel formulas.

Given this Excel formula:
{formula}

Beautified version:
{beautified}

Please provide:
1. A simplified/optimized version of this formula using modern Excel best practices
2. A brief explanation of what improvements you made and why

Guidelines:
- Use modern Excel functions when possible (IFS instead of nested IF, XLOOKUP instead of VLOOKUP/INDEX-MATCH, LET for clarity, etc.)
- Simplify complex nested structures
- Improve readability and maintainability
- Keep the same logical behavior
- If the formula is already optimal, say so and suggest minor improvements if any

Format your response EXACTLY as follows:
SIMPLIFIED:
[put the optimized formula here, on a single line, starting with =]

COMMENT:
[put your explanation here]

Important:
- The SIMPLIFIED formula must be a valid Excel formula on a single line
- Start the simplified formula with =
- Be concise in your explanation (2-3 sentences max)
- If no optimization is possible, return the original formula and explain why it's already optimal"""

    def _parse_response(self, response_text: str) -> dict[str, str]:
        """
        Parse Claude's response into simplified formula and comment.

        Args:
            response_text: Raw response from Claude

        Returns:
            Dictionary with 'simplified' and 'comment' keys
        """
        lines = response_text.strip().split('\n')

        simplified = ""
        comment = ""
        current_section = None

        for line in lines:
            line_stripped = line.strip()

            if line_stripped == "SIMPLIFIED:":
                current_section = "simplified"
                continue
            elif line_stripped == "COMMENT:":
                current_section = "comment"
                continue

            if current_section == "simplified" and line_stripped:
                # Collect simplified formula (should be one line)
                if not simplified:
                    simplified = line_stripped
            elif current_section == "comment" and line_stripped:
                # Collect comment lines
                if comment:
                    comment += " " + line_stripped
                else:
                    comment = line_stripped

        # Ensure simplified formula starts with =
        if simplified and not simplified.startswith('='):
            simplified = '=' + simplified

        # Fallback if parsing fails
        if not simplified or not comment:
            return {
                "simplified": simplified or "Unable to parse response",
                "comment": comment or "Unable to parse optimization explanation"
            }

        return {
            "simplified": simplified,
            "comment": comment
        }


def optimize_formula(formula: str, beautified: str, api_key: Optional[str] = None) -> dict[str, str]:
    """
    Convenience function to optimize a formula.

    Args:
        formula: Original Excel formula
        beautified: Beautified version of the formula
        api_key: Optional Anthropic API key

    Returns:
        Dictionary with 'simplified' and 'comment' keys
    """
    agent = FormulaOptimizerAgent(api_key=api_key)
    return agent.optimize_formula(formula, beautified)
