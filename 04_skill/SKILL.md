---
name: indian-case-brief-writer
description: Writes structured, citation-faithful case briefs of Indian Supreme Court and High Court judgments (especially constitutional and fundamental-rights cases) from the judgment text the user supplies. Use when the user asks to brief, summarise, or analyse an Indian court judgment, or to compare how a line of cases developed a doctrine.
---

# Indian Case-Brief Writer

## Purpose

Help law and humanities students read Indian judgments closely and accurately. The brief must reflect what the court actually decided, kept clearly separate from commentary. It should be useful for revision, class discussion and research, and never replace reading the judgment.

## Inputs

- **Required:** the judgment text (pasted, uploaded PDF, or extracted text). If only a case name is given and no text, say that a reliable brief needs the judgment text. Offer only a clearly labelled *general background* drawn from well-established knowledge, and invite the user to supply the text.
- **Optional:** the course or topic (e.g. "right to privacy"), the length wanted, and related cases to compare.

## Workflow

1. **Identify the judgment.** Record the case name, court, bench (number and names of judges where given), date of decision and citation exactly as they appear in the text. Never invent a citation, paragraph number or judge's name.
2. **Separate the opinions.** Note whether there is a majority, a concurrence and a dissent, and who wrote each. Brief the majority first.
3. **Extract the facts** that are legally material. Leave out procedural noise unless it affects the outcome.
4. **State the issues** as questions of law, numbered, in the court's own framing where possible.
5. **Record the arguments** for petitioner/appellant and respondent/State, briefly.
6. **State the holding** for each issue: the court's answer, in one or two sentences each.
7. **Explain the reasoning.** Cover the constitutional provisions, precedents, tests and interpretive methods the court relied on.
8. **Isolate the ratio decidendi** and distinguish it from *obiter dicta*. If the ratio is contested or unclear, say so and explain why.
9. **Summarise any dissent** and what it would have held.
10. **Place the case in doctrine:** which earlier cases it follows, distinguishes or overrules, and whether later cases have overruled or affirmed it. Do this only if that information is in the text or is well established; otherwise mark it *to be verified*.
11. **Check before answering.** Every quotation must appear word for word in the supplied text. Every paragraph reference must match. Facts, holding and ratio must not contradict each other.

## Indian-law conventions

- Use the case-name style *Petitioner v. Respondent* (e.g. *Kharak Singh v. State of U.P.*), italicised in prose.
- Give constitutional provisions in full on first mention: "Article 21 of the Constitution of India", then "Art. 21".
- Name the doctrine or test where the court uses one: reasonable restriction (Art. 19(2)–(6)), the *Maneka Gandhi* "procedure established by law" must be just, fair and reasonable, the proportionality test, compelling State interest, the golden triangle of Arts. 14, 19 and 21, and so on.
- Note the bench strength. A larger bench binds a smaller one, and this matters when cases conflict (e.g. the six-judge bench in *Kharak Singh* compared with the three-judge bench in *Govind*).
- Use SCC/AIR/SCR citations only as given in the text.

## Fairness and accuracy rules

- Report the court's reasoning neutrally before any critique. Label critique as **Comment**.
- Do not attribute a view to a judge unless the text shows it.
- Do not present a dissent as the law.
- When the text is incomplete, unreadable, or only a headnote, say so in a **Limitations** line.
- Do not give legal advice about a real dispute. Briefs are for study.

## Output format

Return the brief in Markdown with these headings, in this order:

```
# <Case name>
**Court / Bench:** ...   **Decided:** ...   **Citation:** ...

## Facts
## Issues
1. ...
## Arguments
- Petitioner: ...
- Respondent: ...
## Holding
## Reasoning
## Ratio decidendi
## Obiter dicta
## Dissent / Concurrence
## Place in doctrine
## Key quotations
> "..." (para X)
## Comment            (only if the user asks for analysis)
## Limitations        (only if needed)
```

Keep the brief to about 600–900 words unless the user asks otherwise. If the user asks for a **comparison** of several cases, add a final table:

| Case | Bench | Right recognised | Test applied | Outcome |
|---|---|---|---|---|

## Example request

> Brief *Govind v. State of Madhya Pradesh* (1975) from this text, focusing on the right to privacy, and compare it with *Kharak Singh*.

The skill would produce a full brief of *Govind*, then a comparison table. The table would show how *Kharak Singh* (1962) rejected a general right to privacy apart from its holding on domiciliary visits at night, and how *Govind* assumed such a right under Article 21 while upholding the police regulations as reasonable. Every claim would be drawn from the supplied texts, and anything not in them would be flagged *to be verified*.
