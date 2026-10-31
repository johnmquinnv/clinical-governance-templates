# Synthetic dashboard verification

**Version:** 0.2.0 · **Checked:** 31 October 2026

The reproducible check is [tools/check_dashboard.mjs](../tools/check_dashboard.mjs). Run it from the repository root with: node tools/check_dashboard.mjs

It checks unique identifiers, allowed fictional teams, Boolean fields and the rules that a closed action must be required, and an overdue action must be required and open. It checks all-team, Alpha, Beta and empty-set counts, zero-denominator handling, rendered filter rows and CSV row counts. The expected metrics are recorded in the [demonstration README](README.md).

The survey has its own validation in the separate education repository. These checks verify the fixed teaching examples; they do not validate a clinical system. Browser layout and download behavior are checked separately during publication. External review and clinical sign-off have not been recorded.
