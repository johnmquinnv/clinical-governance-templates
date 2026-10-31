# Synthetic governance dashboard

**Maintainer:** John Quinn, MD, MPH, PhD, EMT-P  
**Version:** 0.2.0 · **Updated:** 31 October 2026  
**Status:** original educational demonstration; not approved operational policy. No real patient or employer data.

A small, self-contained browser demonstration showing documentation completeness and action follow-up. Every record is invented. It contains no external libraries or data upload facility. Filtering and CSV generation run locally; resource links navigate to their stated destinations.

## Run

Open the [hosted preview (account access required)](https://john-quinn-governance-demo.cuinne.chatgpt.site), or download [dashboard.html](dashboard.html) and open it locally. Filter by fictional team, inspect each numerator and denominator, export the displayed rows as CSV, and print the current view. GitHub's HTML file view shows source code. The [verification record](VERIFICATION.md) documents calculation and data checks.

## Definitions

| Field | Definition |
|---|---|
| id | Invented record identifier |
| team | Fictional team, Alpha or Beta |
| reviewed | Whether a documentation review was recorded |
| handover | Whether the required handover documentation was complete |
| action | Whether a follow-up action was required |
| closed | Whether that action was completed |
| overdue | Whether the required, open action was past its fictional due date at the snapshot |

The snapshot is fixed for demonstration; overdue flags do not depend on today's date. Handover completeness uses all displayed records as the denominator because the field is applicable to each invented record. Action closure uses only records requiring an action.

## Expected results

- All teams: 8 records; 6 reviewed (75%); 5 complete handovers (62.5%); 2 of 5 required actions closed (40%); 2 open overdue actions.
- Alpha: 4 records; 3 reviewed (75%); 3 complete handovers (75%); 1 of 2 actions closed (50%); 1 overdue.
- Beta: 4 records; 3 reviewed (75%); 2 complete handovers (50%); 1 of 3 actions closed (33.3%); 1 overdue.

These measures could inform a documentation review discussion. They cannot rank clinical safety or establish patient outcomes. No thresholds or traffic-light judgements are implied. See the [repository reuse information](../README.md).
