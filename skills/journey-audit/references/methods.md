# Research behind the methods

The skill family uses established UX research methods. Numbers in the load model are a simulation with open weights; the sources below explain where each feature comes from.

| Area | Method | Source |
|---|---|---|
| Journey maps and service blueprints | Stages × lanes (doing, thinking, feeling, frontstage, backstage, support) | Shostack, "Designing Services That Deliver", Harvard Business Review, 1984; Bitner, Ostrom, Morgan, "Service Blueprinting", California Management Review, 2008 |
| Emotion curve | One action per time unit, cumulative feeling −2…+2 | Common journey-mapping practice; Kahneman's peak–end rule for why late dips weigh more |
| Usability heuristics | 10 heuristics (H1–H10) | Nielsen, "Enhancing the explanatory power of usability heuristics", CHI 1994 |
| "Don't make me think" principles | K1–K4, trunk test | Krug, "Don't Make Me Think", 3rd ed., 2014 |
| Keystroke-Level Model | Operators K, P, B, H, M, W | Card, Moran, Newell, "The Psychology of Human-Computer Interaction", 1983 |
| Choice time | Logarithmic growth with options | Hick, 1952; Hyman, 1953 |
| Working memory | ~4 chunks | Cowan, "The magical number 4", Behavioral and Brain Sciences, 2001 |
| Intrinsic vs extraneous load | Cut extraneous, present intrinsic clearly | Sweller, "Cognitive load during problem solving", Cognitive Science, 1988 |
| Fix classification | Must-be, performance, attractive | Kano et al., 1984 |
| Edge cases | Boundary value analysis, state and ordering, authorization | Software testing practice (ISTQB syllabus) |
| Synthetic users | Simulated personas as hypothesis generators, not evidence | Recent LLM-simulation literature; every simulated finding is labelled `synthetic` |

## What the skill does not claim

- The load index is not a prediction of conversion or task time for novices.
- Synthetic personas are not users. Their findings are hypotheses to validate with people.
- Severity and priority are judgements with stated rules, not measurements.
