"""
Tests for utility functions.
"""

import pytest
from app.utils import validate_formula, sanitize_formula


class TestValidateFormula:
    """Tests for formula validation."""

    def test_valid_formula(self):
        """Test validating a valid formula."""
        is_valid, error = validate_formula('=IF(A1>0,"Yes","No")')
        assert is_valid is True
        assert error is None

    def test_empty_formula(self):
        """Test validating empty formula."""
        is_valid, error = validate_formula('')
        assert is_valid is False
        assert error is not None
        assert 'empty' in error.lower()

    def test_whitespace_only(self):
        """Test validating whitespace-only formula."""
        is_valid, error = validate_formula('   ')
        assert is_valid is False
        assert error is not None

    def test_unbalanced_parentheses_extra_open(self):
        """Test validating formula with extra opening parenthesis."""
        is_valid, error = validate_formula('=IF((A1>0,"Yes","No")')
        assert is_valid is False
        assert 'parenthes' in error.lower()

    def test_unbalanced_parentheses_extra_close(self):
        """Test validating formula with extra closing parenthesis."""
        is_valid, error = validate_formula('=IF(A1>0,"Yes","No"))')
        assert is_valid is False
        assert 'parenthes' in error.lower()

    def test_balanced_parentheses_in_string(self):
        """Test that parentheses inside strings don't affect validation."""
        is_valid, error = validate_formula('=IF(A1>0,"Yes (confirmed)","No")')
        assert is_valid is True
        assert error is None

    def test_formula_without_equals(self):
        """Test validating formula without equals sign."""
        is_valid, error = validate_formula('SUM(A1:A10)')
        assert is_valid is True  # Still valid even without =
        assert error is None


class TestSanitizeFormula:
    """Tests for formula sanitization."""

    def test_remove_leading_whitespace(self):
        """Test removing leading whitespace."""
        result = sanitize_formula('   =SUM(A1:A10)')
        assert result == '=SUM(A1:A10)'

    def test_remove_trailing_whitespace(self):
        """Test removing trailing whitespace."""
        result = sanitize_formula('=SUM(A1:A10)   ')
        assert result == '=SUM(A1:A10)'

    def test_remove_surrounding_quotes(self):
        """Test removing accidentally added quotes."""
        result = sanitize_formula('"=SUM(A1:A10)"')
        assert result == '=SUM(A1:A10)'

    def test_preserve_internal_quotes(self):
        """Test that quotes inside formula are preserved."""
        result = sanitize_formula('=IF(A1>0,"Yes","No")')
        assert result == '=IF(A1>0,"Yes","No")'

    def test_empty_formula(self):
        """Test sanitizing empty formula."""
        result = sanitize_formula('')
        assert result == ''

    def test_already_clean_formula(self):
        """Test that clean formula remains unchanged."""
        formula = '=SUM(A1:A10)'
        result = sanitize_formula(formula)
        assert result == formula
