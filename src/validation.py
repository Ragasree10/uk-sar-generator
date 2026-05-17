"""
Validation module for UK SAR Generator
Detects hallucinations in generated SAR narratives
"""

import re
from typing import List, Dict, Tuple


def extract_identifiers(text: str) -> Dict[str, List[str]]:
    """
    Extract customer IDs and account numbers from text.
    
    Args:
        text: Input text containing identifiers
        
    Returns:
        Dictionary with 'customers' and 'accounts' lists
    """
    customers = re.findall(r'CUST\d+', text)
    accounts = re.findall(r'\d{2}[A-Z]\d[A-Z0-9]\d[A-Z0-9]\d[A-Z0-9]', text)
    
    return {
        'customers': list(set(customers)),  # Remove duplicates
        'accounts': list(set(accounts))
    }


def validate_identifiers(alert_input: str, generated_sar: str) -> Tuple[bool, List[str]]:
    """
    Check if generated SAR contains hallucinated identifiers.
    
    Args:
        alert_input: Original alert text with correct identifiers
        generated_sar: AI-generated SAR narrative
        
    Returns:
        Tuple of (is_valid, list_of_warnings)
        - is_valid: False if hallucinations detected
        - warnings: List of warning messages
    """
    warnings = []
    
    # Extract identifiers from both texts
    input_ids = extract_identifiers(alert_input)
    output_ids = extract_identifiers(generated_sar)
    
    # Check customer IDs
    for customer_id in output_ids['customers']:
        if customer_id not in input_ids['customers']:
            warnings.append(f"⚠️ HALLUCINATED CUSTOMER ID: {customer_id} (not in input)")
    
    # Check account numbers
    for account in output_ids['accounts']:
        if account not in input_ids['accounts']:
            warnings.append(f"⚠️ HALLUCINATED ACCOUNT: {account} (not in input)")
    
    # Check if any input identifiers are missing from output
    for customer_id in input_ids['customers']:
        if customer_id not in output_ids['customers']:
            warnings.append(f"⚠️ MISSING CUSTOMER ID: {customer_id} (should be in output)")
    
    is_valid = len(warnings) == 0
    
    return is_valid, warnings


def format_validation_report(is_valid: bool, warnings: List[str]) -> str:
    """
    Format validation results for display.
    
    Args:
        is_valid: Whether validation passed
        warnings: List of warning messages
        
    Returns:
        Formatted validation report
    """
    if is_valid:
        return "✅ VALIDATION PASSED\n\nAll identifiers match the input alert."
    
    report = "❌ VALIDATION FAILED\n\n"
    report += "The following issues were detected:\n\n"
    
    for i, warning in enumerate(warnings, 1):
        report += f"{i}. {warning}\n"
    
    report += "\n⚠️ Please review and correct before submitting."
    
    return report


# Example usage and test
if __name__ == "__main__":
    # Test case: Model hallucinates customer ID
    alert = """
    ALERT TYPE: High-Value Transaction
    CUSTOMER ID: CUST12345
    ACCOUNT NUMBER: 80A1B2C3D
    AMOUNT: £125,000.00
    DATE: 2025-03-15
    """
    
    # Simulated AI output with hallucinated ID
    generated = """
    Monitoring systems identified suspicious activity on account 80A1B2C3D 
    (customer CUST8686) on 2025-03-15. Transaction amount of £125,000.00 
    exhibits characteristics consistent with high-value transaction monitoring 
    under POCA 2002 Section 330.
    """
    
    is_valid, warnings = validate_identifiers(alert, generated)
    report = format_validation_report(is_valid, warnings)
    
    print("=== VALIDATION TEST ===")
    print(report)
    print("\nExpected: Should detect CUST8686 as hallucinated")
    print(f"Result: {'✅ PASSED' if not is_valid else '❌ FAILED'}")
