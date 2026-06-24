---
name: sub-storyboard-builder
description: Develops the narrative arc into scenes, shots (A-roll/B-roll), and a shot list with shot types and notes.
---

## Purpose
Produce a production-ready storyboard and shot list that drives archival search and original production.

## Procedure
1. Map the selected structure onto 3-7 **scenes/sequences** aligned with story beats.
2. For each scene, list **shots** with:
   - **shot #** - scene.shot notation (e.g., 1.1, 1.2).
   - **shot type** - WS (wide), MS (medium), CU (close-up), ECU, POV, aerial, archival still, archival motion.
   - **roll** - A-roll (interview/primary narration) or B-roll (supporting visuals).
   - **required visual** - exactly what must appear on screen (drives archival search).
   - **notes** - camera movement, pacing, transition, Ken Burns on stills, etc.
3. Mark which shots are candidates for **archival footage** vs. **original production**.
4. Add transitions and pacing notes.
5. Produce a consolidated shot list.

## Shot-type taxonomy
| Code | Meaning |
|---|---|
| WS | Wide shot / establishing |
| MS | Medium shot |
| CU | Close-up |
| ECU | Extreme close-up |
| POV | Point of view |
| AERIAL | Drone/helicopter |
| ARCHIVE-STILL | Historical still image |
| ARCHIVE-MOTION | Historical moving footage |
| ANIMATION | Motion graphics / map |
| INTERVIEW | A-roll talking head |
| VO | Voice-over / narration |

## Outputs
Storyboard + shot list table:
```markdown
| Scene | Beat | Shot | Type | Roll | Required visual | Source plan | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Hook | 1.1 | WS | B-roll | ... | archive | ... |
```

Also return a JSON-like block:
```json
{
  "scenes": [
    {
      "scene_number": 1,
      "title": "...",
      "beats": ["..."],
      "shots": [
        {
          "shot_id": "1.1",
          "type": "WS",
          "roll": "B-roll",
          "required_visual": "...",
          "source_plan": "archive | original",
          "notes": "..."
        }
      ]
    }
  ]
}
```

## Quality Gate
Arc covered; each shot has a type and a required-visual note that can be used for sourcing.
