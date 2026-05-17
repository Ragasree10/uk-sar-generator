"""
UK SAR Generator - Gradio Demo Application

AI-assisted Suspicious Activity Report generation with hallucination detection.
"""

import gradio as gr
import re

# Import validation module from src folder
try:
    from src.validation import validate_identifiers, format_validation_report
except ImportError:
    # Fallback if running from different directory
    from validation import validate_identifiers, format_validation_report


# NOTE: In production, you would load your fine-tuned model here:
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# from peft import PeftModel
#
# model_name = "google/flan-t5-base"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# base_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
# model = PeftModel.from_pretrained(base_model, "path/to/lora/adapter")


def generate_sar_demo(alert_input: str) -> str:
    """
    DEMO VERSION: Generates a simulated SAR narrative.
    
    In production, this would use the fine-tuned Flan-T5 + LoRA model.
    This demo version intentionally includes the hallucination behavior
    to demonstrate the validation system.
    
    Args:
        alert_input: Alert details (customer, account, amount, date)
        
    Returns:
        Generated SAR narrative (with intentional hallucination for demo)
    """
    # Extract key information from alert
    customer_match = re.search(r'CUST\d+', alert_input)
    account_match = re.search(r'\d{2}[A-Z]\d[A-Z0-9]\d[A-Z0-9]\d[A-Z0-9]', alert_input)
    amount_match = re.search(r'£[\d,]+\.?\d*', alert_input)
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', alert_input)
    
    customer_id = customer_match.group(0) if customer_match else "CUST00000"
    account = account_match.group(0) if account_match else "UNKNOWN"
    amount = amount_match.group(0) if amount_match else "£0.00"
    date = date_match.group(0) if date_match else "2025-01-01"
    
    # DEMO: Simulate the 90% hallucination behavior
    # Intentionally use wrong customer ID to demonstrate validation
    hallucinated_id = "CUST8686"  # This will be caught by validation!
    
    sar_narrative = f"""SUSPICIOUS ACTIVITY REPORT

TRANSACTION DETAILS:
Monitoring systems identified suspicious activity on account {account} (customer {hallucinated_id}) on {date}.

TRANSACTION SUMMARY:
A high-value transaction of {amount} was processed through the above account. The transaction exhibits characteristics consistent with patterns requiring regulatory disclosure.

SUSPICIOUS INDICATORS:
- Transaction amount significantly above customer's normal activity profile
- Timing and structure of transaction raises concerns under current monitoring thresholds
- Activity pattern warrants further investigation under AML protocols

REGULATORY ASSESSMENT:
This activity demonstrates reasonable grounds to suspect money laundering as defined under the Proceeds of Crime Act 2002 (POCA), Section 330. The transaction characteristics necessitate disclosure to the UK Financial Intelligence Unit (UKFIU) in accordance with the Money Laundering Regulations 2017.

RECOMMENDED ACTIONS:
Submit SAR to UKFIU via the online reporting portal. Consider Defense Against Money Laundering (DAML) procedures under POCA Section 335 for any pending related transactions. Implement enhanced monitoring of account {account} for a minimum period of 90 days per FCA guidance.

Report generated: {date}
Classification: HIGH-RISK
Status: PENDING REVIEW

---
⚠️ NOTE: This is a DEMO version. In production, this would use the fine-tuned Flan-T5-base + LoRA model.
The customer ID hallucination (CUST8686 instead of {customer_id}) is INTENTIONAL to demonstrate the validation system.
"""
    
    return sar_narrative


def process_alert(alert_input: str) -> tuple:
    """
    Process alert: Generate SAR and validate for hallucinations.
    
    Args:
        alert_input: Alert details from monitoring system
        
    Returns:
        Tuple of (generated_sar, validation_report)
    """
    if not alert_input.strip():
        return "⚠️ Please provide alert details.", "❌ No input to validate"
    
    # Generate SAR (in production, this would use the fine-tuned model)
    generated_sar = generate_sar_demo(alert_input)
    
    # Validate for hallucinations
    is_valid, warnings = validate_identifiers(alert_input, generated_sar)
    validation_report = format_validation_report(is_valid, warnings)
    
    return generated_sar, validation_report


# Example alerts for testing
example_alerts = [
    """ALERT TYPE: High-Value Transaction
CUSTOMER ID: CUST12345
ACCOUNT NUMBER: 80A1B2C3D
AMOUNT: £125,000.00
DATE: 2025-03-15
DESCRIPTION: Large cash deposit""",
    
    """ALERT TYPE: Structuring
CUSTOMER ID: CUST99999
ACCOUNT NUMBER: 45X2Y3Z4A
AMOUNT: £9,900.00 (6 transactions)
DATE: 2025-03-10 to 2025-03-15
DESCRIPTION: Multiple deposits just below reporting threshold""",
    
    """ALERT TYPE: PEP Transaction
CUSTOMER ID: CUST55555
ACCOUNT NUMBER: 12B3C4D5E
AMOUNT: £250,000.00
DATE: 2025-03-20
DESCRIPTION: Wire transfer from offshore jurisdiction"""
]


# Build Gradio interface
with gr.Blocks(title="UK SAR Generator", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # UK SAR Generator
    
    **AI-assisted Suspicious Activity Report generation with hallucination detection.**
    
    This system generates SAR drafts in 30 seconds (vs 30 minutes manually) and validates for hallucinations.
    
    ### How it works:
    1. **Input:** Alert from transaction monitoring system
    2. **Generate:** AI creates SAR draft using fine-tuned Flan-T5
    3. **Validate:** System checks for hallucinated identifiers
    4. **Review:** Human reviews and corrects any warnings
    
    ⚠️ **Demo Note:** This version uses simulated generation to demonstrate the validation system.
    The model intentionally hallucinates customer IDs to show the 90% hallucination behavior and 100% detection accuracy.
    """)
    
    with gr.Row():
        with gr.Column():
            alert_input = gr.Textbox(
                label="Alert Input",
                placeholder="Paste alert details from monitoring system...",
                lines=10,
                value=example_alerts[0]
            )
            
            generate_btn = gr.Button("Generate SAR", variant="primary", size="lg")
            
            gr.Markdown("### Example Alerts")
            gr.Examples(
                examples=example_alerts,
                inputs=alert_input,
                label="Click to load example"
            )
        
        with gr.Column():
            sar_output = gr.Textbox(
                label="Generated SAR Draft",
                lines=20,
                show_copy_button=True
            )
            
            validation_output = gr.Textbox(
                label="Validation Report",
                lines=8
            )
    
    gr.Markdown("""
    ---
    ### Key Findings
    
    Through systematic testing:
    - **90% hallucination rate** on customer identifiers
    - **100% detection accuracy** with validation layer
    - **77% time savings** (30 min → 7 min per SAR)
    
    ### Technical Details
    - **Model:** Flan-T5-base (250M params) + LoRA fine-tuning
    - **Training:** 4.2M trainable parameters, 3 epochs
    - **Validation:** Regex-based identifier verification
    
    **GitHub:** [github.com/Ragasree10/uk-sar-generator](https://github.com/Ragasree10/uk-sar-generator)
    """)
    
    # Event handlers
    generate_btn.click(
        fn=process_alert,
        inputs=alert_input,
        outputs=[sar_output, validation_output]
    )


# Launch the app
if __name__ == "__main__":
    demo.launch()
