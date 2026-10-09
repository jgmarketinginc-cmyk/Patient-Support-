# Angelina output | TRIAL-P3 | Spanish, small business (usted, neutral Latin American)

SYNTHETIC SAMPLE, SHADOW MODE. Nothing sent. AI translation, not certified, not official.
Files: trial-source-email-only.txt (English as translated), trial-email-es.txt (Spanish).

## Checks
- translation_check.py --lang es: PASS (2 WARN, below)
- brand_scrub.py: PASSED, 0 hits
- WARN 1: AI translation, not certified; native-speaker review recommended.
- WARN 2: footer/unsubscribe left in English; Spanish opt-out wording pending Joaquin.

## Kept exactly as in source
$1,500; "seven business days" (translated as "siete días hábiles", same value); Friday, October 9 ("viernes 9 de octubre"); Reyes Property Management; Dana; Priya; "CEO"; signature block (Chief of Staff / Office of Joaquin Garcia, CEO); footer line (verbatim from /config/footer.md). The "Subject:" label is kept as a header field. No unsubscribe line exists in the source, so none was added.

## Glossary
| English | Spanish | Note |
|---|---|---|
| AI audit | auditoría de IA | translated; lowercase as in source |
| system | sistema | consistent throughout |
| written proposal with options | propuesta por escrito con opciones | |
| our CEO | nuestro CEO | acronym kept, as in the signature |
| business days | días hábiles | |
| tenant | inquilino | |
| lease copy | copia de contrato de arrendamiento | |
| leak ticket | reporte de fuga | "ticket" avoided (anglicism) |
| Chief of Staff, Office of Joaquin Garcia, CEO | unchanged | signature stays English per footer.md |

## Flagged sentences (back-translation, English)
1. "Hi Dana," -> "Hola Dana,". Back: "Hello Dana,". Plain greeting; first name only, as in source.
2. "...a late-night leak ticket got buried under lease copy requests" -> "...un reporte de fuga recibido a altas horas de la noche quedó perdido entre las solicitudes de copias de contratos de arrendamiento." Back: "...a leak report received late at night ended up lost among the requests for copies of lease contracts." Idiom "buried under" replaced with "quedó perdido entre". "Ticket" rendered as "reporte". "Late-night" is ambiguous in English (submitted late at night vs. handled late); I read it as received late at night.
3. "We enjoyed hearing how your office runs" -> "Disfrutamos escuchar cómo funciona su oficina". Back: "We enjoyed hearing how your office works." "Runs" is figurative; replaced with "funciona".
4. "Our CEO will follow up with you by Friday, October 9." -> "Nuestro CEO le dará seguimiento a más tardar el viernes 9 de octubre." Back: "Our CEO will follow up with you no later than Friday, October 9." "By" read as a deadline, not "on".
5. "...answers only from documents you give us and approve" -> "responde únicamente con base en los documentos que usted nos entregue y apruebe". Back: "...answers only based on the documents that you give us and approve." Subjunctive used for documents not yet supplied; meaning unchanged.
6. "Anything outside them goes to a person to review." -> "Todo lo que quede fuera de ellos pasa a una persona para que lo revise." Back: "Everything that falls outside of them goes to a person for them to review." "A person" kept (not "named"), as in source.
7. "...maps what comes in and what a system would handle before any build" -> "mapea lo que ingresa y lo que un sistema atendería, antes de construir nada". Back: "maps what comes in and what a system would handle, before building anything." "Handle" -> "atender"; "build" -> "construir", kept literal.
8. "If your accountant needs anything specific... tell us" -> "avísenos". Back: "let us know." Formal usted imperative.
9. "Thank you," (closing) -> "Gracias,". Back: "Thank you,".

Idioms replaced: "buried under" (2), "how your office runs" (3). Subject "next steps from our call" -> "próximos pasos tras nuestra llamada" (back: "next steps after our call").

## Reviewer reminder
A native-speaker review is recommended before any live send: [PENDING: reviewer, Joaquin].

## Questions to Joaquin
- Who is the native-speaker reviewer? [PENDING: reviewer]
- What is the approved Spanish unsubscribe/opt-out wording? [PENDING: Spanish unsubscribe wording] Until then the footer stays English. (The source also omits the unsubscribe line; Cody's open question 1 still applies.)
- Is Dana's company a Spanish-speaking audience? The source is a synthetic sample; confirm Spanish is actually wanted for this contact before any use.
- Keep "CEO" as is, or prefer "director ejecutivo"? I kept "CEO" to match the signature.

## Sources / Assumptions
- Sources: /home/user/Patient-Support-/outputs/shadow/2026-10-08/cody/cos-RUN-20261008-001-s3-email.md (lines 7-29, Subject through footer); /sops/angelina-sop.md; /config/business.md; /config/footer.md; /config/authority.md (Angelina: shadow, send-authorized NO).
- Assumptions: source passed Cody's gate as stated in the brief; audience small business, so plain, direct, usted; "Wednesday" kept as "miércoles" without a date, as in source; translation is AI-produced and not certified.
- Not logged to /logs/shadow-log.csv, per the brief.
