# Implementation plan and architecture

## 1. Priorities, effort, dependencies

The sequence below follows the user's requested order; estimates are engineering and test time, excluding external clinical/legal review and telephone verification.

| Order | Task ID | Task | Priority | Estimate |
|---|---|---|---|---:|---:|
| 1 | 1 | Indirect crisis detection | P0 | L / 16 h |
| 2 | 2 | Crisis response and direct safety check | P0 | M / 8 h |
| 3 | 5 | PHQ-9 item 9 safety logic and sourcing | P1 | M / 10 h |
| 4 | 3 | Short, non-judgmental system prompt | P1 | M / 8 h |
| 5 | 4 | Privacy controls and hard-delete UX | P1 | L / 20 h |
| 6 | 6 | Facility data verification workflow | P2 | L / 24 h |
| 7 | 7 | Audio and breathing attributions | P2 | M / 10 h |
| 8 | 8 | Age-appropriate education and references | P3 | M / 12 h |

Dependency graph and implementation sequence: `Task 1 -> Task 2 -> Task 5 -> Task 3 -> Task 4 -> Task 6 -> Task 7 -> Task 8`. Screening data remains local and is not persisted by the server.

Milestones:

1. Safety baseline: tasks 1–2, deterministic response, crisis tests.
2. Screening safety: task 5, item 9 override, source and disclaimer tests.
3. Language and privacy: tasks 3–4, concise prompt, local hard delete, no shared public health-data APIs.
4. Content compliance: tasks 6–8, verification states, attribution metadata, age audit.
5. Release gate: accessibility review, legal/clinical approval, official hotline and facility confirmation, deployment reliability review.

## 2. Architecture

```text
Mobile/desktop browser
  ├─ Static HTML/CSS/ES6 UI and in-memory crisis dialog state
  ├─ Chat history: browser localStorage (obfuscated, not encrypted)
  └─ HTTPS
       └─ FastAPI
            ├─ Rule-based crisis check -> deterministic SSE response
            ├─ Ordinary chat/summary -> external AI processing service
            ├─ Read-only education, screening, facilities and attribution data
            └─ Privacy deletion receipt (application server stores no health history)
```

No database migration is needed. The previous chat/mood/quiz CRUD used process-global, unauthenticated in-memory collections; those APIs are removed rather than pretending they can securely delete one user's records. `DELETE /api/privacy/data` reports that the application server has zero retained health records; browser localStorage is deleted by the client. This endpoint cannot erase provider or hosting logs.

### API surface

- `POST /api/chat`: SSE; the latest user message is checked before provider readiness or AI invocation.
- `POST /api/summary`: sends the selected conversation to the AI provider for summarization.
- `GET /api/knowledge`, `GET /api/facilities`, `GET /api/health`.
- `DELETE /api/privacy/data`: explicit deletion-scope receipt; no server records are retained.
- `GET /static/audio/{file}`: serves only files with a completed source/license record; current assets are blocked.
- The previous unauthenticated `/api/sessions`, `/api/moods`, and `/api/quizzes/results` APIs are removed.

### Frontend state and components

```text
Application
  ├─ CrisisBanner + CrisisSupportDialog (ephemeral; no crisis text stored separately)
  ├─ ChatPanel
  │    ├─ ChatHistory (localStorage)
  │    └─ PrivacyInfo + HardDeleteConfirmation
  ├─ AssessmentPanel (PHQ-9 item 9 -> same crisis dialog)
  ├─ EducationPanel (article references)
  ├─ RelaxationPanel (license-gated audio + breathing references)
  └─ FacilityDirectory (verification status; no unverified contact details)
```

No PHI is needed in a database. Crisis state is computed locally for immediate UI and independently at the API boundary for a deterministic response. Local phrase rules are not a clinical triage system and require ongoing human review.

## 3. Implemented behavior and examples

- Indirect examples such as “ngủ không dậy nữa”, “mọi người nhẹ nhõm khi không có mình”, “không muốn tồn tại nữa”, and “mọi chuyện sẽ ổn khi mình không ở đây” open the crisis dialog. The server independently returns the safety template without calling the model.
- The first response content lists 111, 115, and Ngày Mai, then asks directly whether the student is in immediate danger, has prepared to self-harm, or is alone.
- PHQ-9 item 9 > 0 overrides a low total-score label with “Cần hỗ trợ ngay”, shows the same crisis support, and does not display “không có biểu hiện trầm cảm”.
- PHQ-9 includes an explicit screening disclaimer and cites the original instrument plus a Vietnam study. The app's current Vietnamese wording is disclosed as an unvalidated adaptation, not represented as a validated translation.
- Facility contacts, hours, addresses, and specialties are published only when their individual fields are verified against the facility's own website. The Central Psychiatric Hospital No. 2 record remains unverified; several other records still need direct confirmation of missing fields and schedules.
- Audio metadata records source, license, verification time, and publishability. Since provenance is missing for all bundled tracks, playback and direct static serving are blocked.
- Student examples replace workplace/interview examples; articles expose source links.

## 4. Testing and accessibility

Automated tests cover crisis phrases/negations, deterministic crisis response, deletion API behavior, disabled legacy data APIs, PHQ-9 metadata, facility verification flags, audio license gates, and education references. Release testing should additionally include:

- Integration checks with AI provider unavailable and crisis response still available.
- Phrase variants, missing diacritics, whitespace/punctuation, negated intent, quoted/educational discussion, and false-positive review by a qualified Vietnamese-speaking safeguarding reviewer.
- PHQ-9 item 9 values 0, 1, 2, and 3 across low and high total scores.
- Keyboard-only and screen-reader testing, visible focus, modal labels, live crisis announcements, telephone links, reflow at 320 CSS px, contrast, and reduced motion against WCAG 2.1 AA.

Automated checks do not certify WCAG conformance or clinical safety.

## 5. Risk assessment

| Risk | Mitigation / remaining work |
|---|---|
| Missed or false-positive crisis phrase | Deterministic API plus client check; curated tests; regular human review; transparent non-diagnostic dialog. |
| Hotline unavailable or inaccurate | No claim of availability for Ngày Mai; confirm all numbers with official operators before release; preserve emergency alternatives. |
| AI/provider retention of sensitive content | Minimize and redact user input; disclose external processing; verify provider configuration/terms; the app cannot delete provider-side data. |
| Shared health data exposure | Removed public unauthenticated CRUD APIs; no server-side health-history persistence. |
| Wrong clinic contact/address | Hide contact/hour/address until sourced and verified; current entries remain on hold. |
| Unlicensed media | Block audio delivery until source/license evidence is added and reviewed. |
| Privacy claims stronger than implementation | Disclose that browser history is not strongly encrypted and deleting it locally does not erase external copies or browser backups. |
| Uptime below 99.9% | Current in-memory limiter and single-service deployment do not meet that SLO; requires redundant hosting, independent monitoring and on-call coverage. |
| Legal/medical non-compliance | Obtain Vietnamese privacy, minors/safeguarding, medical-content and copyright review before production; documentation is not legal advice. |

## 6. Documentation deliverables

- [README](../README.md): actual API, data flow, test commands, and limitations.
- [Crisis runbook](./crisis-runbook.md): routine checks and incident response.
- [Privacy policy](../static/privacy-policy.html) and [terms of use](../static/terms-of-use.html): user-facing drafts that require legal review.
