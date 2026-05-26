# Persona B — Professional services (ProServ)

**Journey name:** `Scrawler_ProServ_LeadNurture_Appointment`  
**Archetype:** Advisor, association, local services; relationship-first, low frequency  
**Objective:** Nurture leads + drive consultation booking; reduce no-show risk

## Evidence (why this flow)

- ProServ = 11/21 HeyMarvin UR cohort (largest)
- Pre-built templates lean e-commerce (BET 3; Hannah→Chris Rich UR quote)
- Top jobs: welcome/nurture + appointment reminders (UR jobs #2, #10)

## Playbook steps

| step_id | Stage | Action | Expected |
|---------|-------|--------|----------|
| proserv_00_nav | 1 | Create journey; **avoid** abandoned cart / cross-sell templates | Non-ecom intent visible or blank path |
| proserv_01_template | 1 | Note template catalog skew | ProServ-relevant options OR document gap |
| proserv_02_trigger | 2 | Tag `scrawler-proserv-lead` or test audience join | Test-only entry |
| proserv_03_email1 | 4 | Personal intro; low promo tone | Professional voice |
| proserv_04_delay1 | 3 | Delay 3 days | |
| proserv_05_email2 | 4 | Value content (checklist/FAQ); **no cart language** | |
| proserv_06_delay2 | 3 | Delay 2 days | |
| proserv_07_email3 | 4 | Book a call / consultation CTA | Single clear CTA |
| proserv_08_branch | 5 | If/else on tag `appointment-booked` (optional) | Branch works OR log segmentation gap |
| proserv_09_review | 6 | Review; **do not Turn on** | Draft only |
| proserv_10_save | 6 | Save | Draft in automations list |

## Email stubs

1. **Subject:** Thanks for connecting — what happens next  
2. **Subject:** A short guide before we talk  
3. **Subject:** Ready to schedule your consultation?  

## Watch-for

- Only e-commerce templates promoted in gallery
- Cart/product merge fields suggested inappropriately
- No appointment-reminder template category (BET 3 gap)
- Advanced segmentation required for simple tag branch
- Frequency-cap concerns if multiple flows imagined (note only)
- Vertical benchmarking absent (note as barrier if UI offers no guidance)

## Avoid as primary

Abandoned cart, cross-sell, product-review, replenishment templates.
