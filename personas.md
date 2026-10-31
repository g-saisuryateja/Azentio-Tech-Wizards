# Personas: Digital Fraud Investigation System

Personas for building, testing and demoing the Level 1 solution. Section A covers who uses the system. Sections B and C cover the customer and fraudster behaviour to generate as test data. The sample data in `sample_data/` implements every persona in B and C, and `ground_truth.csv` holds the labels.

---

## A. System users

| Persona | Goal | What they need from the app |
|---|---|---|
| Fraud analyst (L1) | Triage alerts quickly | Case queue, risk filters, reason codes, one-click "False Positive" or "Requires Investigation" |
| Senior investigator (L2) | Dig into complex rings | Entity links (shared device, phone, account), event timeline, notes |
| Fraud operations manager | Monitor volume and workload | Risk distribution, alerts by category, case ageing, false-positive rate |
| Compliance or audit officer | Prove decisions were sound | Immutable original alerts, decision history, retained evidence |
| Rule or model admin | Tune detection | Configurable thresholds, rule weights, shared-device allowlist |
| Data or integration engineer | Load data | CSV, Excel and JSON upload, validation errors, reject queue |

**Level 1 priority:** build the fraud analyst and data engineer flows fully. Add a simple investigator view if time allows. The other roles can be a label plus a stats page.

---

## B. Fraud personas (must be flagged)

| ID | Persona | Scenario | Data signature | Expected |
|---|---|---|---|---|
| C9001 | Account takeover attacker | Login failures, then transfer | 6 failed logins in 6 minutes, success from a new device and IP, password reset, new beneficiary added, then a transfer at about 14x the usual amount | High |
| C9101-C9105 | Device-sharing ring | Coordinated fraud | 5 customers with different names, addresses and phones, one `device_id`, recently onboarded, loan applications on the same day | High |
| C9201-C9203 | Synthetic identity builder | Identity fraud | Same phone and email across profiles, near-identical names ("Rohan Mehta", "Rohan Mehtaa"), different addresses, newly onboarded | High |
| C9301-C9304 | Loan farmer | Cross-system fraud | One device submits 4 loan applications under different identities, loans are cashed out to a shared beneficiary within hours | High |

### Extension personas (not in the sample data yet)

| Persona | Scenario | Data signature |
|---|---|---|
| Mule account | Organised fraud | New account receives many inbound transfers and forwards them within minutes, balance near zero after each hop |
| Insurance claim duplicator | Duplicate claims | Same incident date, vehicle or policy across multiple claims, shared bank account or phone across claimants |
| Slow-burn fraudster | Structuring | Amounts kept just under a reporting limit and spread across days |

---

## C. Legitimate lookalikes (must not be Medium or High)

| ID | Persona | Why it looks suspicious | Why it is legitimate | Expected |
|---|---|---|---|---|
| C9401-C9403 | Family sharing one phone | 3 customers on one device | Same surname and address, long-standing usage | Low |
| C9501 | Salaried customer paying rent | High-value transfer | Same beneficiary and amount every month | Low |
| C9502 | Small business owner | Many rapid transfers | Daily burst pattern to established suppliers | Low |
| C9503 | Forgetful user | 4 failed logins | Known device and IP, success on the next attempt, no sensitive action | Not flagged |
| C9504 | Frequent traveller | New device and new IP | No beneficiary change, no large transfer | Not flagged |
| C9505 | Festival spender | Amount spike (about 10x median) | One-off purchase at a merchant already used | Low |

---

## D. How to use these in a demo

1. Seed about 150 ordinary customers as background noise (the generator does this).
2. Inject the B and C personas and tag each with a hidden ground-truth label.
3. Run detection, then compare alerts against the labels. All of B should be Medium or High. None of C should be Medium or High. `pytest -q` automates this check.
4. Tell the demo as stories:
   - Open the account takeover case (C9001) and read the reasons aloud: repeated failures, new device, password reset, new beneficiary, large transfer.
   - Show the family-phone case (C9401-C9403) scored Low because they share a surname and address.
   - Show the rent payer (C9501) that is not escalated because the payment is regular.
