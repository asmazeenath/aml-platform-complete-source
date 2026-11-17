# Threat model and guardrails
Use synthetic or authorized data only. Threats include credential theft, unauthorized case changes,
PII exposure, replay/duplicate events, tampered evidence, malicious uploads and model/data poisoning.
Mitigations required before production: OIDC/JWT, RBAC, MFA, TLS, encryption at rest, secrets manager,
least privilege, field masking, immutable audit storage, retention policies, signed artifacts, input validation,
rate limiting, backups, restore tests and security review. The included role dependency is a development stub only.
