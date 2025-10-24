"""
Tests for the Excel formula beautifier.
"""

import pytest
from app.beautifier import beautify_formula, FormulaBeautifier


class TestFormulaBeautifier:
    """Tests for FormulaBeautifier class."""

    def test_simple_if_formula(self):
        """Test beautifying a simple IF formula."""
        formula = '=IF(A1>0,"Yes","No")'
        result = beautify_formula(formula)

        assert result.startswith('=')
        assert 'IF' in result
        assert 'A1>0' in result

    def test_nested_if_formula(self):
        """Test beautifying nested IF formulas."""
        formula = '=IF(A1>0,IF(B1<10,"OK","NO"),"FAIL")'
        result = beautify_formula(formula)

        assert result.startswith('=')
        assert result.count('IF') == 2
        # Should have line breaks for nested structure
        assert '\n' in result

    def test_formula_without_equals(self):
        """Test formula without leading equals sign."""
        formula = 'IF(A1>0,"Yes","No")'
        result = beautify_formula(formula)

        # Should not add = if it wasn't there
        assert not result.startswith('=')

    def test_empty_formula(self):
        """Test handling empty formula."""
        formula = ''
        result = beautify_formula(formula)

        assert result == ''

    def test_formula_with_whitespace(self):
        """Test formula with extra whitespace."""
        formula = '  =IF(A1>0,"Yes","No")  '
        result = beautify_formula(formula)

        assert result.startswith('=')
        assert not result.startswith('  ')

    def test_sumifs_formula(self):
        """Test beautifying SUMIFS formula."""
        formula = '=SUMIFS(D:D,A:A,">=2023",B:B,"Sales")'
        result = beautify_formula(formula)

        assert result.startswith('=')
        assert 'SUMIFS' in result

    def test_and_formula(self):
        """Test beautifying AND formula."""
        formula = '=AND(A1>0,B1<10,C1="Active")'
        result = beautify_formula(formula)

        assert result.startswith('=')
        assert 'AND' in result
        assert '\n' in result  # Should have line breaks

    def test_vlookup_formula(self):
        """Test beautifying VLOOKUP formula."""
        formula = '=VLOOKUP(A1,Sheet2!A:B,2,FALSE)'
        result = beautify_formula(formula)

        assert result.startswith('=')
        assert 'VLOOKUP' in result

    def test_custom_indent_size(self):
        """Test custom indentation size."""
        beautifier = FormulaBeautifier(indent_size=2)
        formula = '=IF(A1>0,IF(B1<10,"OK","NO"),"FAIL")'
        result = beautifier.beautify(formula)

        assert result.startswith('=')
        # With smaller indent, should still have indentation
        assert '  ' in result or '\n' in result

    def test_quoted_strings_with_commas(self):
        """Test handling quoted strings containing commas."""
        formula = '=IF(A1>0,"Hello, World","Goodbye")'
        result = beautify_formula(formula)

        assert result.startswith('=')
        assert '"Hello, World"' in result

    def test_multiple_functions(self):
        """Test formula with multiple function types."""
        formula = '=IF(AND(A1>0,B1<10),SUM(C1:C10),"N/A")'
        result = beautify_formula(formula)

        assert result.startswith('=')
        assert 'IF' in result
        assert 'AND' in result
        assert 'SUM' in result


class TestBeautifyFormulaFunction:
    """Tests for the convenience function."""

    def test_beautify_formula_function(self):
        """Test the convenience function works."""
        formula = '=IF(A1>0,"Yes","No")'
        result = beautify_formula(formula)

        assert isinstance(result, str)
        assert result.startswith('=')

    def test_with_custom_indent(self):
        """Test with custom indent size."""
        formula = '=IF(A1>0,"Yes","No")'
        result = beautify_formula(formula, indent_size=2)

        assert isinstance(result, str)
        assert result.startswith('=')
