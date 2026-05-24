# UK SAR Generator

**AI that writes compliance reports 77% faster - then catches its own mistakes.**

**🔴 [Try the Live Demo](https://huggingface.co/spaces/Raga10/UK-SAR-Generator)**

---

## The Story

Banks write thousands of Suspicious Activity Reports (SARs) every year. Each takes **30 minutes** of manual work - same structure, same legal citations, just different transaction details.

I wondered: can AI generate the draft in 30 seconds, so humans just review instead of writing from scratch?

### I fine-tuned a model

Fine-tuned **Flan-T5-base** to generate SAR drafts automatically.

**Result:** 30 minutes → **7 minutes** per report.

### Then I discovered something interesting

The model generates beautiful, professional reports. Perfect structure, proper legal citations, everything looks great.

Then I noticed: **it makes up customer IDs 90% of the time.**

- Input: `CUST12345`  
- Output: `CUST8686` (completely invented)

Sometimes it had favorites - `CUST6980` appeared multiple times. One test was off by a single digit: `CUST66666` → `CUST6666`.

**The model learned to write _like_ a SAR, but not that IDs in the output should match IDs in the input.**

### The fix

Built a validation layer that catches every hallucination:

```python
def check_hallucination(input, output):
    input_ids = extract_ids(input)
    output_ids = extract_ids(output)
    
    for output_id in output_ids:
        if output_id not in input_ids:
            return f"⚠️ WARNING: Hallucinated {output_id}"
    
    return "✅ Verified"
```

**Detection rate: 100%**

Now the workflow is: AI generates (30s) → Validation flags errors → Human reviews (7 min total).

### What I learned

**The model doesn't need to be perfect.** It needs to be good enough that reviewing a draft is faster than writing from scratch.

**System design > Model accuracy.** An imperfect model with proper validation beats chasing 99% accuracy.

The 90% hallucination rate taught me more about production ML than any perfect model would have.

---

## Try It

**[Live Demo](https://huggingface.co/spaces/Raga10/UK-SAR-Generator)** - Put in an alert, watch it generate a SAR, see validation catch hallucinations

---

## Technical Details

<details>
<summary>Click to expand</summary>

**Model:**
- Flan-T5-base (250M parameters)
- LoRA fine-tuning (4.2M trainable params)
- 3 epochs, 2.3 min training on A100

**Validation:**
- Regex-based identifier verification
- Modular design (`src/validation.py`)
- 100% detection accuracy

**Architecture:**

![Architecture](architecture.svg)

**Business Impact:**  
For a bank with 500 SARs/month: £115,200/year savings

</details>

---

## Running Locally

```bash
git clone https://github.com/Ragasree10/uk-sar-generator.git
cd uk-sar-generator
pip install -r requirements.txt
python app.py
```

**First run:** Downloads fine-tuned model from Hugging Face (~250MB, 2-3 min)  
**After that:** Starts instantly

**Requirements:** Python 3.8+, 2GB RAM

---

**Built with synthetic data. No real customer information used.**
