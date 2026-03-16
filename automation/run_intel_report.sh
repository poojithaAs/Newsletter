#!/bin/bash
# Content Intelligence Report - Runs every 2 days
# Searches conferences, blogs, podcasts and emails Poojitha a summary

echo "=========================================="
echo "Content Intel Report - $(date)"
echo "=========================================="

export PATH="/usr/local/bin:$PATH"

TASK_DESCRIPTION=$(cat << 'TASKEOF'
You are running an automated content intelligence report for Poojitha A S, who runs the "DevOps Made Simple" LinkedIn newsletter.

STEP 1: SCAN EXISTING NEWSLETTERS
Read the filenames from /sessions/quirky-brave-hopper/mnt/Newsletter/DevOps_Made_Simple_Newsletters/ to build a list of topics already covered (83+ editions). You must NEVER suggest topics that overlap with existing editions.

STEP 2: RESEARCH CONFERENCES AND EVENTS
Use web search to find upcoming conferences, summits, and meetups in:
- SRE / DevOps / Platform Engineering
- AI / ML Infrastructure / LLMOps
- Cloud / Kubernetes / Container Security
- System Design / Distributed Systems
Look for events in the next 90 days. Capture: name, dates, location, key sessions, why it matters.

STEP 3: FIND LATEST ENGINEERING BLOGS
Use web search to find recent posts from: Netflix Tech Blog, Uber Engineering Blog, Google Cloud Blog, AWS Architecture Blog, Kubernetes Blog, CNCF Blog, HashiCorp Blog, Datadog Engineering Blog, Grafana Labs Blog.
Also search for: Kubernetes releases, OpenTelemetry updates, Prometheus changes, Terraform updates, GitHub Actions features, ArgoCD releases, container security advisories, AI infrastructure tooling.

STEP 4: FIND RELEVANT PODCASTS
Search for recent episodes from: Ship It! (Changelog), SRE Prodcast, ShipTalk, Kubernetes Podcast, The New Stack Podcast, Software Engineering Daily (DevOps), Agentic DevOps.

STEP 5: GENERATE 6 TO 10 NEWSLETTER CONTENT IDEAS
For each idea: suggested title (bold, contrarian, no hyphens), format type (Monday Deep Dive 800+ words, Wednesday Quick Win 400 words, or Thursday Industry Pulse 500 words), why it matters now. Cross check against existing newsletter list. No repeats.

STEP 6: CHECK PREVIOUS REPORT NUMBER
Search Gmail for "Content Intel Report" to find the latest report number, then increment by 1.

STEP 7: CREATE GMAIL DRAFT
Create a Gmail draft to pooja.as2011@gmail.com with subject: "Your Content Intel Report #N (DATE)"
Use text/html content type. Structure:

Content Intel Report #N
DATE | DevOps Made Simple

THIS WEEK: What You Must Know
[Top 3 to 5 items]

CONFERENCE CALENDAR (Next 90 Days)
[Upcoming conferences with dates, locations, highlights]

PODCAST PICKS
[3 to 5 recent episodes worth listening to]

NEWSLETTER CONTENT IDEAS
[6 to 10 ideas with titles, format type, and why it matters]

THINGS TO LOOK INTO THIS WEEK
[3 to 5 actionable items]

CRITICAL RULES:
- NEVER suggest topics already in existing newsletters
- Keep scannable, under 2 minute read
- Plain language, no corporate jargon
- Include links to sources

SUCCESS: Gmail draft created with fresh, non duplicate content ideas.
TASKEOF
)

claude --print \
  --dangerously-skip-permissions \
  --allowedTools "WebSearch,WebFetch,Read,Bash,Glob,Grep,mcp__8c65c868-eb9b-445b-a9a4-5db70f99c33c__gmail_create_draft,mcp__8c65c868-eb9b-445b-a9a4-5db70f99c33c__gmail_search_messages" \
  "$TASK_DESCRIPTION"

echo ""
echo "Completed at $(date)"
