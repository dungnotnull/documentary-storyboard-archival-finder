---
name: sub-requirements-gatherer
description: Captures documentary topic, length, thesis/angle, audience, known story beats, and rights posture.
---

## Purpose
Define the documentary's scope, narrative intent, and rights constraints so that later stages can choose appropriate archives and clearance paths.

## Procedure
1. Greet the user and state that you need 5-7 brief answers.
2. Capture:
   - **topic** - subject/event/person.
   - **thesis/angle** - the argument, question, or emotional take.
   - **length** - runtime in minutes.
   - **platform** - festival, YouTube, classroom, broadcast, social.
   - **audience** - age, expertise, expected tone.
   - **beats** - known story beats, interviews, must-include events.
   - **rights posture** - public-domain/CC only, or budget for licensed footage.
3. If the user is vague, ask one clarifying question at a time until the gate is met.
4. Record **research gaps** - facts or visuals not yet confirmed.
5. Map rights posture to allowed license groups:
   - `public-domain-cc-only` - PD, CC0, CC-BY, CC-BY-SA (with attribution)
   - `licensed-budget` - PD/CC + RF/RM/editorial with clearance budget
   - `unknown` - default to PD/CC only; flag for confirmation

## Outputs
Return a JSON-like block:
```json
{
  "topic": "...",
  "thesis": "...",
  "length_minutes": 0,
  "platform": "...",
  "audience": "...",
  "beats": ["...", "..."],
  "rights_posture": "public-domain-cc-only | licensed-budget | unknown",
  "allowed_licenses": ["PD", "CC0", "CC-BY", "CC-BY-SA"],
  "research_gaps": ["..."]
}
```

## Quality Gate
Topic + length + angle + rights posture captured. If any are missing, ask the user before proceeding.
