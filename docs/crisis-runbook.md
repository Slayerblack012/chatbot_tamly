# Crisis system runbook

## Scope and limitations

The client shows an urgent support dialog for configured Vietnamese/English phrases. The FastAPI chat route independently checks the latest user message and returns a deterministic safety response before calling the AI provider. This is a lightweight rule-based safeguard, not clinical triage; it can miss indirect wording and can trigger on benign discussion.

## Routine checks

- Check `GET /api/health` and the deployment's external uptime monitor.
- Run `pytest` after changes to `core/crisis.py`, `server.py`, or the client crisis flow.
- Periodically have a trained Vietnamese-speaking reviewer test direct and indirect examples, negations, misspellings, and ordinary non-crisis chat. Do not use real user transcripts in test fixtures.
- Confirm 111, 115, and the Ngày Mai contact details with their official operators before each production release. The application cannot verify telephone availability itself.
- Confirm the crisis response renders the phone links and direct safety questions on narrow mobile screens and with keyboard/screen-reader navigation.

## Incident response

1. Treat a missing or delayed crisis response as a safety incident. Alert the on-call engineer and the designated clinical/safeguarding reviewer; do not wait for an AI-provider response.
2. Verify the static crisis banner is visible and phone links work. The `/api/chat` crisis branch does not depend on AI provider availability.
3. If detection or response is broken, disable ordinary chat if necessary, retain the static emergency contacts, and deploy the last known-good version. Do not remove crisis contacts while chat remains available.
4. Test with synthetic phrases only. Do not copy crisis text, IP addresses, or other identifying user data into issue trackers, logs, or chat messages.
5. After recovery, run the focused crisis tests and a manual mobile/accessibility check. Record the incident without personal data.

## Availability caveat

The current application has no multi-region failover, durable queue, external paging, or measured 99.9% SLO. A production SLO requires redundant hosting, independent monitoring, reviewed escalation coverage, and a tested fallback channel.
