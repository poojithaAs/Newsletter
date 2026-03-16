#!/bin/bash
# Weekly Newsletter Generator - Runs every Sunday at 6 AM
# Generates 3 newsletters (Mon/Wed/Thu) as DOCX files

echo "=========================================="
echo "Newsletter Generator - $(date)"
echo "=========================================="

export PATH="/usr/local/bin:$PATH"

TASK_DESCRIPTION=$(cat << 'TASKEOF'
You are running the automated weekly newsletter generator for "DevOps Made Simple" by Poojitha A S.

OBJECTIVE: Generate 3 newsletter editions for the upcoming week as professional DOCX files. Save to /sessions/quirky-brave-hopper/mnt/Newsletter/upcoming_newsletters/

STEP 1: DETERMINE DATES
Calculate the dates for the upcoming Monday, Wednesday, and Thursday. Use these for file naming and headers.

STEP 2: DETERMINE EDITION NUMBERS
Check /sessions/quirky-brave-hopper/mnt/Newsletter/DevOps_Made_Simple_Newsletters/ to count existing editions (83+ so far). The next editions continue from there. Also check /sessions/quirky-brave-hopper/mnt/Newsletter/upcoming_newsletters/ for any already generated editions to avoid overlap.

STEP 3: PICK TOPICS
Use web search to find the most current DevOps/SRE/Kubernetes/AI trends. Pick topics that are timely and have NOT been covered in existing editions. Rotate through: Kubernetes ops, observability, AI in DevOps, container security, platform engineering, incident response, cloud cost optimization, CI/CD.

Read at least 3 existing newsletters from /sessions/quirky-brave-hopper/mnt/Newsletter/DevOps_Made_Simple_Newsletters/ to study Poojitha's writing voice before writing.

STEP 4: WRITE 3 NEWSLETTERS
Use npm docx package (docx-js) to create professional DOCX files:

Monday Deep Dive (800+ words):
- One topic, deep analysis
- Action plan with timelines (Day 1, Day 2, Week 1, Week 2)
- Quantify impact with numbers

Wednesday Quick Win (400 words):
- One fix you can do today
- A command, tool, or config change
- Copy paste ready steps

Thursday Industry Pulse (500 words):
- 3 things that matter this week
- News, trends, what to watch
- Brief but insightful

DOCX FORMATTING:
- Arial font throughout
- Color coded type badge (blue=Deep Dive, green=Quick Win, orange=Industry Pulse)
- Date and edition number in header
- Left border quote block for the hook
- Key Takeaway box at the end
- Call to Action question at the end
- Header: "DevOps Made Simple | Poojitha A S"

POOJITHA'S VOICE:
1. Start with a surprising stat or contrarian statement. NEVER "New edition is live"
2. Short punchy sentences. 5 to 10 words when emphasizing
3. Use metaphors. "Think of Jenkins as an old factory."
4. Signature pattern: "X is not Y. It is Z."
5. Action frameworks with timelines
6. Quantify impact: "30 to 40% savings" not "significant savings"
7. Close with a memorable quotable principle
8. End with a call to action question

STEP 5: GENERATE QUICK RECAP
Create QUICK_RECAP.docx summarizing all 3 editions in one page so Poojitha can review in 2 minutes.

STEP 6: VALIDATE
Check every generated DOCX for:
- The word "real" must NOT appear anywhere
- No hyphens anywhere in text content
- Word counts meet minimums
- No corporate jargon (leverage, synergy, circle back)
- No hedging (might, perhaps, probably)
- No passive voice

FILE NAMING: YYYYMMDD_type_Title.docx
Example: 20260323_deep_dive_Why_Your_Platform_Team_Is_Building_The_Wrong_Thing.docx

CRITICAL RULES:
- NEVER use the word "real"
- NEVER use hyphens (use "to" instead, like "20 to 40 percent")
- Write in natural human language everyone can understand
- Content must sound like Poojitha, not a template

SUCCESS: 3 DOCX newsletter files + QUICK_RECAP.docx saved, all validated clean.
TASKEOF
)

claude --print \
  --dangerously-skip-permissions \
  --allowedTools "WebSearch,WebFetch,Read,Write,Bash,Glob,Grep,Edit" \
  "$TASK_DESCRIPTION"

echo ""
echo "Completed at $(date)"
