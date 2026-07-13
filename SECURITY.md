# Security Policy

## Report privately

Do not open a public issue for vulnerabilities, exposed secrets, privacy incidents, unsafe tool or model behavior, authentication or authorization failures, or unremediated exploit details.

Report privately to:

**security@altmanai.tech**

Include the affected commit or component, reproduction steps, realistic impact, preconditions, and suggested containment when safely possible. Do not send live credentials or unnecessary personal data.

## Supported code

The current default branch and explicitly identified active release branches are supported. Historical commits, forks, experiments, and archived work may not receive fixes.

This repository is a local reference engine. Its presence on GitHub does not establish that any particular version is deployed in production.

## Security and privacy boundaries

The current reference implementation:

- reads local JSON files supplied by the operator;
- performs local Python calculations;
- writes local run logs;
- does not call external models, APIs, accounts, calendars, or messaging services;
- does not provide authentication, authorization, encryption, multi-user isolation, or production data controls.

Any integration that adds network access, accounts, personal data, external AI models, tools, memory, retrieval, analytics, or cloud storage requires a separate threat model and release review.

## Contributor requirements

- Never commit tokens, passwords, private keys, certificates, production exports, or real private task lists.
- Treat task content, profile data, logs, and user routines as potentially sensitive.
- Validate untrusted JSON before use in a product boundary.
- Use least privilege for integrations and external services.
- Preserve human review, correction, override, and disable paths.
- Assess prompt injection, data exfiltration, tool misuse, and provider risk if an AI model or agent is added.
- Add tests for security-sensitive input and failure behavior.
- Document monitoring, containment, and rollback for material releases.

## Safe research boundaries

Good-faith research must avoid unauthorized access, data retention, service disruption, social engineering, persistence, destructive testing, or disclosure of private information. Stop and report if you encounter credentials, personal data, confidential information, or evidence of active compromise.

## High-impact use warning

Do not use this reference engine as the sole authority for medical, mental-health, legal, financial, employment, education, housing, safety, or other consequential decisions. Such uses require qualified domain review, additional safeguards, validated data, recourse, monitoring, and applicable legal or regulatory assessment.

## Handling

Reports are assessed based on evidence, exploitability, affected systems, user impact, and remediation complexity. No fixed response-time commitment is implied. Public disclosure should wait until remediation or a coordinated disclosure plan reduces avoidable risk.
