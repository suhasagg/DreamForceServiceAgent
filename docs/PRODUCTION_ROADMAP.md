# Production substitutions
DemoCRM/Orders/Knowledge are local runnable adapters. Replace through interfaces with Salesforce REST/GraphQL APIs or
another CRM, order-management APIs, and a tenant-filtered hybrid search service. Use PostgreSQL-backed LangGraph
checkpoints for durable threads, Kafka + transactional outbox for events, Redis only for ephemeral coordination,
KMS/Vault for credentials, OPA/Cedar for policy, OpenTelemetry Collector for traces, and a dedicated human-agent console.
Do not put OAuth tokens, payment data or raw secrets in graph state.
