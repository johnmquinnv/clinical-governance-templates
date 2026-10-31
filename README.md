# Clinical Governance Templates

**Maintainer:** John Quinn, MD, MPH, PhD, EMT-P  
**Version:** 1.2.0 · **Last editorial update:** 31 October 2026  
**Clinical review status:** educational draft; independent clinical sign-off is not recorded. Local review and approval are required before operational use.

Blank, reusable templates for clinical audit, patient safety incident review, and quality improvement projects.

> Educational and general. Templates are blank. **Never enter patient-identifiable information, staff names or employer-confidential details in a public copy.** Adapt to local policy, reporting systems and legal requirements before use.

## Templates

1. [Clinical audit](templates/clinical-audit.md): standards, data collection, results, action plan and re-audit.
2. [Incident review](templates/incident-review.md): a systems-focused learning review.
3. [QI project plan](templates/qi-project-plan.md): Model for Improvement and PDSA cycles.

## Open, print and download

- [Hosted synthetic dashboard preview (account access required)](https://john-quinn-governance-demo.cuinne.chatgpt.site) - filter fictional teams, inspect calculations and export CSV.
- [Printable template pack](downloads/clinical-governance-templates.pdf)
- [Print-friendly HTML](downloads/clinical-governance-templates.html)

The editable Markdown templates above remain the source for adaptation.

## Additional portfolio collections

- [Medical assistance and evacuation governance](assistance-governance/README.md): generic responsibility and assurance worksheet.
- [Health security and medical interoperability](health-security/README.md): public-source evidence and analysis framework.
- [Synthetic governance dashboard](data-demo/README.md): downloadable browser demonstration with invented records and documented metrics.

These examples contain no employer materials or patient data and are not approved operational policies.

## Background reading

- [HQIP: Documenting local clinical audit](https://www.hqip.org.uk/wp-content/uploads/2020/05/Final-Clinical-Audit-Reporting-guide-2020.pdf)
- [NHS England: Patient Safety Incident Response Framework (PSIRF)](https://www.england.nhs.uk/patient-safety/patient-safety-insight/incident-response-framework/)
- [NHS England: Patient safety learning response toolkit](https://www.england.nhs.uk/publication/patient-safety-learning-response-toolkit/)
- [IHI: Model for Improvement](https://www.ihi.org/library/model-for-improvement)
- [IHI: PDSA worksheet](https://www.ihi.org/library/tools/plan-do-study-act-pdsa-worksheet)

These frameworks are UK/US-origin. Check which apply in your jurisdiction.

## Contributing

Suggestions are welcome via issues or pull requests. Please do not submit real incidents or patient data.

## Reuse and attribution

Original educational content and synthetic datasets are available under [CC BY-NC 4.0](LICENSE): noncommercial sharing and adaptation with attribution and identification of changes. Demonstration and maintenance code uses the [MIT license](LICENSE-CODE). Third-party publications, images, provider resources, names and logos retain their own rights. Private DCP materials are outside this release. For commercial content reuse, contact the maintainer through a repository issue.

## Maintenance

See [CHANGELOG.md](CHANGELOG.md) for dated changes. When suggesting a correction, include the affected file, the proposed wording and a current primary source. Use synthetic examples only. Content should be checked again when relevant guidance changes.

To rebuild the printable editions from Markdown, install ReportLab in a local Python environment and run `python3 tools/build_print_pack.py` from the repository root.
