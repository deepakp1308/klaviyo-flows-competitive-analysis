# Persona A — E-commerce SMB (DSB)

**Journey name:** `Scrawler_Ecom_Welcome_FirstPurchase`  
**Archetype:** Shopify/Woo-connected merchant; first automation, not power user  
**Objective:** New subscribers → first purchase (welcome + incentive)

## Evidence (why this flow)

- #1 live/building UR use case (mailchimp.html HeyMarvin jobs table)
- Safer than abandoned cart (high try-and-stall in UR)
- ECU cohort: highest CJB adoption (cjb-workflow-health.html)

## Playbook steps

| step_id | Stage | Action | Expected |
|---------|-------|--------|----------|
| ecom_00_nav | 1 | Automations → Create / Customer Journey | CJB entry; template gallery or blank |
| ecom_01_intent | 1 | Pick welcome-oriented template OR start blank | Relevant template visible without ecom-only dead ends |
| ecom_02_trigger | 2 | Starting point: tag `scrawler-ecom-test` OR joins audience / signup | Trigger saved; test-only audience |
| ecom_03_email1 | 4 | Email 1 immediate: welcome + brand intro | Subject/body editable; saves |
| ecom_04_delay1 | 3 | Delay 2 days after email 1 | Delay node on canvas |
| ecom_05_email2 | 4 | Email 2: social proof / bestsellers | Product blocks or manual content OK |
| ecom_06_delay2 | 3 | Delay 3 days | Second delay configured |
| ecom_07_email3 | 4 | Email 3: first-purchase offer (~10% off) | Clear CTA; promo copy |
| ecom_08_review | 6 | Review map; **do not Turn on** | Draft status; activation gated or easy to mis-click → log |
| ecom_09_save | 6 | Save / exit | Journey in list as Draft |

## Email stubs (copy-paste)

1. **Subject:** Welcome to {{company}} — here's what to expect  
2. **Subject:** What our customers love most  
3. **Subject:** Your exclusive 10% off — first order inside  

## Watch-for

- Trigger list not searchable
- Store/purchase triggers missing without integration
- Brand Kit not applied to automation emails
- Minimum 1-hour delay if testing sub-hour follow-up
- Turn On before content complete
- Legacy editor opens instead of NEB

## Stretch (only if smooth)

Second journey: abandoned cart starting point — separate run, separate findings file suffix `-cart`.
