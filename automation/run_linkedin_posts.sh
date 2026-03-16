#!/bin/bash
# LinkedIn Post Generator - Runs every Sunday at 9 AM (after newsletters)
# Generates newsletter teaser posts AND standalone WeBrokeItTogether posts

echo "=========================================="
echo "LinkedIn Post Generator - $(date)"
echo "=========================================="

export PATH="/usr/local/bin:$PATH"

TASK_DESCRIPTION=$(cat << 'TASKEOF'
You are running the automated LinkedIn post generator for Poojitha A S. There are TWO separate content streams. Generate BOTH.

PART 1: NEWSLETTER TEASER POSTS

STEP 1: Check /sessions/quirky-brave-hopper/mnt/Newsletter/upcoming_newsletters/ for the latest generated newsletters.
STEP 2: For each new newsletter, create a teaser post (140 to 180 words):
- Open with the most surprising stat or bold claim from the newsletter (NOT "New edition is live")
- List 3 to 5 things the newsletter covers using checkmark bullets
- End with a question
- Add #DevOps #SRE #DevOpsMadeSimple hashtags at the bottom only
STEP 3: Generate a branded image for each (1200x627 HTML file with navy/blue gradient, "New Edition" badge, newsletter title, "DevOps Made Simple | Poojitha A S")

PART 2: STANDALONE #WEBROKEITTOGETHER POSTS

STEP 1: Pick 2 to 3 original incident stories. These must NOT be about newsletter topics. Think: deployment disasters, DNS typos, certificate expiries, memory leaks, config drift, load balancer issues, database failovers, etc.
STEP 2: For each, write a dialogue post (180 to 240 words):
- Hook (surprising stat or bold statement)
- Tag #WeBrokeItTogether
- #SETUP section explaining the situation
- Natural dialogue between Sara Baqla and Poojitha A S (sounds like two people talking, not a script)
- #FIX section with checkmark bullets of what they did
- #LESSON section with takeaway
- End with a question
- #DevOps #SRE hashtags at the bottom only
STEP 3: Generate branded images (1200x627 HTML, blue gradient, "#WeBrokeItTogether" badge)

OUTPUT:
Save all posts and images to /sessions/quirky-brave-hopper/mnt/Newsletter/linkedin-content-machine/ready_posts/
- Newsletter posts: post_newsletter_XX.txt and image_newsletter_XX.html
- WBT posts: post_wbt_XX.txt and image_wbt_XX.html
- Master guide: ALL_READY_POSTS.md

Check the existing files in ready_posts/ first and increment the numbering from the highest existing number.

CRITICAL RULES:
- NEVER use the word "real" anywhere
- NEVER use hyphens (use "to" instead)
- Newsletter teasers do NOT use dialogue format
- WeBrokeItTogether posts are NOT about newsletter topics
- Dialogue should sound natural, not scripted
- Newsletter links go in FIRST COMMENT, never in post body
- Every post ends with a question
- Hashtags only at the bottom

QUALITY CHECK:
After generating all posts, verify:
- No forbidden words ("real", hyphens)
- Word counts in range (newsletter 140 to 180, WBT 180 to 240)
- Every post has a question CTA
- Every post has hashtags only at bottom

SUCCESS: All posts and images generated, validated clean, saved to ready_posts/.
TASKEOF
)

claude --print \
  --dangerously-skip-permissions \
  --allowedTools "WebSearch,Read,Write,Bash,Glob,Grep,Edit" \
  "$TASK_DESCRIPTION"

echo ""
echo "Completed at $(date)"
