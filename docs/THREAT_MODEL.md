# Threat model
Trust boundaries: client/channel, model, retrieved content, tools, CRM/order systems, human console.
Threats: prompt injection, excessive agency, cross-tenant retrieval, IDOR, confused deputy, refund fraud,
PII leakage, malicious knowledge content, tool-output injection, replay, SSRF, credential exfiltration,
model/provider outage, poisoned memory, supply-chain compromise.
Controls: deterministic authorization outside model; tenant-scoped retrieval; minimum OAuth scopes;
human approval for writes/communications/financial actions; RBAC for refunds; idempotency; immutable audit;
PII redaction; egress allowlists; sandboxed browser workers; KMS/Vault; signed webhooks; provenance;
evaluation/red-team suites; kill switches and per-tool circuit breakers.
