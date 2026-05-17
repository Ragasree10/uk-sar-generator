"""
UK SAR Generator - Source Package

Core modules for SAR generation and validation.
"""

from .validation import validate_identifiers, format_validation_report, extract_identifiers

__version__ = "1.0.0"
__all__ = ['validate_identifiers', 'format_validation_report', 'extract_identifiers']
