# UK SAR Generator

**AI that writes compliance reports 77% faster - then catches its own mistakes.**

**🔴 [Live Demo](https://huggingface.co/spaces/Raga10/UK-SAR-Generator)**

---

## The Problem

Banks write thousands of Suspicious Activity Reports (SARs) every year. Each takes **30 minutes** - same structure, same legal citations, just different transaction details.

I wondered: can AI generate the draft so humans just review instead of writing from scratch?

---

## What I Built

![Architecture](architecture.svg)

Fine-tuned **Flan-T5-base** (250M parameters) to generate SAR drafts automatically.

**Result:** 30 minutes → **7 minutes** per report (77% time saved)

---

## The Interesting Part

The model generates beautiful, professional reports. Perfect structure, proper legal citations, everything looks great.

Then I noticed: **it makes up customer IDs 90% of the time.**

Input: `CUST12345`  
Output: `CUST8686` (completely invented)

Sometimes it had favorites - `CUST6980` appeared multiple times. One test was off by a single digit: `CUST66666` → `CUST6666`.

The model learned to write **like** a SAR, but not that the customer ID in the output should match the customer ID in the input.

---

## The Solution

Built a validation layer:

```python
def check_hallucination(alert_input, generated_sar):
    input_ids = re.findall(r'CUST\d+', alert_input)
    output_ids = re.findall(r'CUST\d+', generated_sar)
    
    for output_id in output_ids:
        if output_id not in input_ids:
            return f"⚠️ WARNING: Hallucinated {output_id}"
    
    return "✅ Looks good"
```

**Detection rate: 100%**

Now the workflow is:
1. AI generates draft (30 seconds)
2. Validation flags errors
3. Human fixes warnings (5 seconds)
4. Submit (7 minutes total)

---

## What I Learned

**The model doesn't need to be perfect.** It needs to be good enough that reviewing a draft is faster than writing from scratch.

**System design > Model accuracy.** An imperfect model with proper validation is more useful than chasing 99% accuracy.

**Small models work.** 250M parameters (not billions) can handle real-world tasks with the right design.

---

## Technical Details

- **Model:** Flan-T5-base (250M params) + LoRA fine-tuning
- **Training:** 4.2M trainable parameters, 3 epochs, 2.3 min on A100
- **Validation:** Regex-based hallucination detection
- **Testing:** 10 diverse test cases, 90% hallucination rate, 100% detection

---

## Business Impact

**Bank with 500 SARs/month:**
- Current: 250 hours/month (£12,500)
- With AI: 58 hours/month (£2,900)
- **Savings: £115,200/year**

---

## What's Next

1. **RAG for regulatory citations** - Stop the model from inventing SAR codes
2. **On-premise deployment** - Package for banks' own servers (GDPR compliance)

---

## Try It

**[Live Demo](https://huggingface.co/spaces/Raga10/UK-SAR-Generator)** - Put in an alert, watch it generate a SAR, see validation catch hallucinations

---

## Why I Built This

I wanted to see if small language models can reduce real human effort. Not chase benchmarks - actually help someone's job.

The answer: yes, if you design the system correctly. The 90% hallucination rate taught me more about production ML than any perfect model would have.

---

---

**Connect:** [Live Demo](https://huggingface.co/spaces/Raga10/UK-SAR-Generator)

---

*Built with synthetic data. No real customer information used.*

Want to try it on your own machine? Here's how:

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Ragasree10/uk-sar-generator.git
cd uk-sar-generator

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

**First Run:** Downloads the fine-tuned model from Hugging Face (~250MB). Takes 2-3 minutes.  
**Subsequent Runs:** Starts instantly.

### System Requirements

- **Python:** 3.8 or higher
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** 500MB for model files
- **Internet:** Required for first-time model download
