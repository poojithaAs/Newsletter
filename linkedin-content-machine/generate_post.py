#!/usr/bin/env python3
"""
LinkedIn Content Machine for DevOps Made Simple
Generates: ready to copy post text + branded image HTML + improvement tips

Usage:
  python3 generate_post.py --newsletter path/to/newsletter.html
  python3 generate_post.py --topic "Your newsletter topic here"
  python3 generate_post.py --batch   (processes all newsletters in DevOps_Made_Simple_Newsletters/)

Rules:
  - Never use the word "real" or hyphens
  - Write in natural human language understandable by everyone
  - Posts should be 100 to 250 words
  - Always include a question at the end
  - Hashtags go at the bottom only
"""

import argparse
import os
import re
import sys
import json
import glob
from datetime import datetime
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "output")
NL_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "DevOps_Made_Simple_Newsletters")

# ─── Brand Config ────────────────────────────────────────────────────────────
BRAND = {
    "name": "Poojitha A S",
    "brand": "DevOps Made Simple",
    "tagline": "SRE | DevOps | AI Observability",
    "color1": "#0A66C2",
    "color2": "#1E3C72",
    "color3": "#2A5298",
    "bg": "#F3F2EF",
}


# ─── Image Template (1200x627 LinkedIn recommended) ──────────────────────────
def generate_image_html(title, subtitle="", badge="DevOps Made Simple", gradient="linear-gradient(135deg, #0A66C2 0%, #1E3C72 100%)", icon="⚡"):
    """Generate a branded LinkedIn image as HTML (screenshot at 1200x627)."""
    subtitle_html = f'<div class="subtitle">{subtitle}</div>' if subtitle else ''

    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1200px; height: 627px; overflow: hidden; }}
.card {{
  width: 1200px; height: 627px;
  background: {gradient};
  display: flex; flex-direction: column;
  justify-content: center; align-items: center;
  padding: 60px 80px;
  position: relative;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
}}
.badge {{
  position: absolute; top: 32px; left: 40px;
  background: rgba(255,255,255,0.15);
  color: #fff; padding: 8px 20px;
  border-radius: 20px; font-size: 16px;
  font-weight: 600; letter-spacing: 0.5px;
  backdrop-filter: blur(10px);
}}
.icon {{
  font-size: 52px; margin-bottom: 20px;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
}}
.title {{
  color: #ffffff; font-size: 42px; font-weight: 800;
  text-align: center; line-height: 1.25;
  max-width: 1000px;
  text-shadow: 0 2px 12px rgba(0,0,0,0.3);
}}
.subtitle {{
  color: rgba(255,255,255,0.85); font-size: 20px;
  text-align: center; margin-top: 16px;
  max-width: 800px; line-height: 1.4;
}}
.footer {{
  position: absolute; bottom: 28px;
  display: flex; align-items: center; gap: 16px;
  color: rgba(255,255,255,0.8); font-size: 16px;
}}
.avatar {{
  width: 40px; height: 40px; border-radius: 50%;
  background: rgba(255,255,255,0.2);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 18px; color: #fff;
  border: 2px solid rgba(255,255,255,0.4);
}}
.brand {{ font-weight: 700; color: #fff; }}
.div {{ opacity: 0.4; }}
</style></head><body>
<div class="card">
  <div class="badge">{badge}</div>
  <div class="icon">{icon}</div>
  <div class="title">{title}</div>
  {subtitle_html}
  <div class="footer">
    <div class="avatar">P</div>
    <span class="brand">{BRAND["name"]}</span>
    <span class="div">|</span>
    <span>{BRAND["brand"]}</span>
  </div>
</div>
</body></html>'''


# ─── Newsletter Parser ───────────────────────────────────────────────────────
def extract_newsletter(html_path):
    """Extract title and key content from a newsletter HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Title
    title_m = re.search(r'<title>(.*?)</title>', content)
    title = title_m.group(1) if title_m else "Untitled"
    # Clean title: remove " - DevOps Made Simple" suffix
    title = re.sub(r'\s*[\-\u2013]\s*DevOps Made Simple.*', '', title).strip()

    # Bold statements (key points)
    bold_points = re.findall(r'<strong>(.*?)</strong>', content)
    bold_points = [re.sub(r'<[^>]+>', '', b).strip() for b in bold_points]
    bold_points = [b for b in bold_points if 20 < len(b) < 300]

    # All paragraphs
    all_paras = re.findall(r'<p>(.*?)</p>', content, re.DOTALL)
    all_paras = [re.sub(r'<[^>]+>', '', p).strip() for p in all_paras]
    all_paras = [p for p in all_paras if len(p) > 40]

    # Stats (numbers/percentages)
    stats = []
    for p in all_paras:
        if re.search(r'\d+%|\$[\d,]+|\d+ billion|\d+ million', p):
            stats.append(p)

    return {
        'title': title,
        'bold_points': bold_points[:10],
        'paragraphs': all_paras[:15],
        'stats': stats[:5],
        'filename': os.path.basename(html_path),
    }


# ─── Quality Checker ─────────────────────────────────────────────────────────
def check_quality(text):
    """Score a post and return tips."""
    score = 0
    tips = []
    words = len(text.split())
    first_line = text.split('\n')[0].lower()

    # Hook (2 pts)
    strong = ['the ', 'why ', 'how ', 'what ', 'your ', 'most ', 'i ', 'we ', 'every ',
              '$', '68%', '82%', '100%', '95%', '47%', '90%', 'ai ']
    if any(first_line.startswith(w) for w in strong):
        score += 2
    else:
        score += 1
        tips.append("HOOK: Try opening with a stat or bold claim.")

    # Length (2 pts)
    if 100 <= words <= 250:
        score += 2
    elif 80 <= words <= 300:
        score += 1
        tips.append(f"LENGTH: {words} words. Aim for 100 to 250.")
    else:
        tips.append(f"LENGTH: {words} words. Way off target (100 to 250).")

    # CTA (1 pt)
    if '?' in text[-200:]:
        score += 1
    else:
        tips.append("CTA: End with a question.")

    # No external link (1 pt)
    if 'http' not in text:
        score += 1
    else:
        tips.append("LINK: Move links to first comment.")

    # Structure (2 pts)
    if any(m in text for m in ['✓', '1.', '#FIX', '#LESSON']):
        score += 2
    else:
        tips.append("STRUCTURE: Add checkmarks or numbered steps.")

    # Hashtags at end (1 pt)
    lines = text.strip().split('\n')
    if '#' in lines[-1]:
        score += 1

    # Forbidden words check
    if re.search(r'\breal\b', text, re.IGNORECASE):
        tips.append("WARNING: Contains the word 'real'. Remove it.")
    if '-' in text and not text.strip().endswith('-'):
        # Check if hyphens are in hashtags (ok) or in text (not ok)
        non_hashtag = re.sub(r'#\w+', '', text)
        if '-' in non_hashtag:
            tips.append("WARNING: Contains hyphens. Replace with spaces or rewrite.")

    grade = 'Excellent' if score >= 8 else 'Good' if score >= 6 else 'Needs Work'
    return {'score': score, 'max': 10, 'grade': grade, 'tips': tips}


# ─── Post Templates ──────────────────────────────────────────────────────────

def make_dialogue_post(title, setup_line, dialogue_pairs, fix_items, lesson):
    """Generate a #WeBrokeItTogether dialogue format post."""
    dialogue = ""
    for speaker, line in dialogue_pairs:
        dialogue += f'{speaker}: "{line}"\n'

    fixes = "\n".join([f"✓ {f}" for f in fix_items])

    return f"""{title}
#WeBrokeItTogether

#SETUP
{setup_line}

{dialogue.strip()}

#FIX
{fixes}

#LESSON
{lesson}

What would you have done differently? Drop your take below.

#DevOps #SRE #Kubernetes"""


def make_teaser_post(hook, bullet_points, closing_question):
    """Generate a newsletter teaser post."""
    bullets = "\n".join([f"✓ {b}" for b in bullet_points])

    return f"""{hook}

In this week's DevOps Made Simple, I break down:

{bullets}

{closing_question}

#DevOps #SRE #DevOpsMadeSimple"""


def make_tutorial_post(title, intro, steps, closing):
    """Generate a tutorial style post."""
    step_text = "\n\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)])

    return f"""{intro}

{step_text}

{closing}

#DevOps #SRE #Kubernetes"""


# ─── Main Processing ─────────────────────────────────────────────────────────

def process_newsletter(html_path, output_dir):
    """Generate posts and images from a newsletter."""
    data = extract_newsletter(html_path)
    title = data['title']
    safe = re.sub(r'[^a-zA-Z0-9_]', '_', title)[:50]

    os.makedirs(output_dir, exist_ok=True)

    # Use newsletter content to build posts
    key_insight = data['bold_points'][0] if data['bold_points'] else title
    stat = data['stats'][0] if data['stats'] else ""

    # Dialogue post
    dialogue_post = make_dialogue_post(
        title=title,
        setup_line=key_insight,
        dialogue_pairs=[
            ("Sara Baqla", "Everything looks fine on my end."),
            ("Poojitha A S", "That is the problem. It looks fine."),
            ("Sara Baqla", "The dashboard is green."),
            ("Poojitha A S", "The dashboard is watching the wrong thing."),
            ("Sara Baqla", "What should it be watching?"),
            ("Poojitha A S", key_insight),
        ],
        fix_items=data['bold_points'][1:5] if len(data['bold_points']) > 1 else [
            "Monitor what matters, not what is easy",
            "Alert on quality, not just uptime",
            "Review weekly and iterate"
        ],
        lesson=stat if stat else key_insight,
    )

    # Teaser post
    teaser_post = make_teaser_post(
        hook=f"{stat[:100]}." if stat else f"{key_insight}",
        bullet_points=data['bold_points'][:4] if data['bold_points'] else [
            "Why this keeps happening",
            "What the best teams do instead",
            "A step by step plan you can start tomorrow"
        ],
        closing_question="Have you seen this play out on your team? Tell me about it.",
    )

    # Tutorial post
    tutorial_post = make_tutorial_post(
        title=title,
        intro=f"{key_insight}\n\nHere is the simplest way I have found to handle it. No jargon. Just what works.",
        steps=data['bold_points'][:5] if data['bold_points'] else [
            "Identify the root cause",
            "Build a monitoring baseline",
            "Set up alerts that matter",
            "Review and iterate weekly"
        ],
        closing="Save this for later. You will need it.\n\nWhat step would you add? Let me know below.",
    )

    posts = {
        'dialogue': dialogue_post,
        'teaser': teaser_post,
        'tutorial': tutorial_post,
    }

    # Generate images
    image_configs = {
        'dialogue': {
            'badge': '#WeBrokeItTogether',
            'gradient': 'linear-gradient(135deg, #0A66C2 0%, #1E3C72 50%, #0D1B3E 100%)',
            'icon': '💬',
        },
        'teaser': {
            'badge': 'New Edition',
            'gradient': 'linear-gradient(135deg, #1E3C72 0%, #2A5298 50%, #0A66C2 100%)',
            'icon': '📰',
        },
        'tutorial': {
            'badge': 'Tutorial',
            'gradient': 'linear-gradient(135deg, #057642 0%, #1E3C72 100%)',
            'icon': '🔧',
        },
    }

    for ptype, config in image_configs.items():
        img = generate_image_html(
            title=title,
            subtitle=key_insight[:80] if len(key_insight) > 20 else "",
            badge=config['badge'],
            gradient=config['gradient'],
            icon=config['icon'],
        )
        with open(os.path.join(output_dir, f"image_{ptype}_{safe}.html"), 'w') as f:
            f.write(img)

    # Quality check + write output
    output_path = os.path.join(output_dir, f"posts_{safe}.md")
    with open(output_path, 'w') as f:
        f.write(f"# LinkedIn Posts for: {title}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Source: {data['filename']}\n\n")
        f.write("---\n\n")

        for variant, text in posts.items():
            q = check_quality(text)
            wc = len(text.split())
            f.write(f"## {variant.upper()} (Score: {q['score']}/{q['max']} {q['grade']} | {wc} words)\n\n")
            f.write(f"**Image:** `image_{variant}_{safe}.html`\n\n")
            f.write("### Ready to Copy:\n```\n")
            f.write(text)
            f.write("\n```\n\n")
            if q['tips']:
                f.write("### Tips:\n")
                for t in q['tips']:
                    f.write(f"  {t}\n")
            f.write("\n---\n\n")

        f.write("## Posting Checklist\n")
        f.write("1. Pick the variant that fits your mood\n")
        f.write("2. Open the matching image HTML in your browser\n")
        f.write("3. Screenshot at 1200x627\n")
        f.write("4. Paste post text into LinkedIn\n")
        f.write("5. Attach the image\n")
        f.write("6. Put newsletter link in FIRST COMMENT\n")
        f.write("7. Reply to comments in the first 2 hours\n")

    # Also write individual txt files
    for variant, text in posts.items():
        txt_path = os.path.join(output_dir, f"post_{variant}_{safe}.txt")
        with open(txt_path, 'w') as f:
            f.write(text)

    print(f"  Generated: {output_path}")
    print(f"  Images: image_*_{safe}.html")
    return posts


def main():
    parser = argparse.ArgumentParser(description='LinkedIn Content Machine for DevOps Made Simple')
    parser.add_argument('--newsletter', help='Path to a newsletter HTML file')
    parser.add_argument('--topic', help='Quick post from a topic string')
    parser.add_argument('--batch', action='store_true', help='Process latest 5 newsletters')
    parser.add_argument('--output', default=OUT_DIR, help='Output directory')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    if args.newsletter:
        process_newsletter(args.newsletter, args.output)

    elif args.batch:
        files = sorted(glob.glob(os.path.join(NL_DIR, '*.html')))
        latest = files[-5:] if len(files) >= 5 else files
        print(f"Processing {len(latest)} newsletters...")
        for f in latest:
            print(f"\n--- {os.path.basename(f)} ---")
            process_newsletter(f, args.output)
        print(f"\nDone! Check {args.output}/")

    elif args.topic:
        topic = args.topic
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', topic)[:40]

        # Generate image
        img = generate_image_html(topic, badge="DevOps Made Simple", icon="⚡")
        img_path = os.path.join(args.output, f"image_{safe}.html")
        with open(img_path, 'w') as f:
            f.write(img)

        # Generate a quick dialogue post
        post = make_dialogue_post(
            title=topic,
            setup_line=f"Most teams struggle with {topic.lower()}. Here is what the best ones do differently.",
            dialogue_pairs=[
                ("Sara Baqla", "We keep running into this."),
                ("Poojitha A S", "That is because the approach is wrong."),
                ("Sara Baqla", "What should we do?"),
                ("Poojitha A S", f"Start with understanding why {topic.lower()} fails in the first place."),
            ],
            fix_items=[
                "Identify the root cause before picking tools",
                "Start small. Prove it works. Then scale.",
                "Review weekly and iterate",
            ],
            lesson=f"The biggest mistake with {topic.lower()}? Treating it as a tool problem instead of a process problem.",
        )

        q = check_quality(post)
        post_path = os.path.join(args.output, f"post_{safe}.md")
        with open(post_path, 'w') as f:
            f.write(f"# LinkedIn Post: {topic}\n")
            f.write(f"Score: {q['score']}/{q['max']} ({q['grade']})\n\n")
            f.write("```\n")
            f.write(post)
            f.write("\n```\n\n")
            if q['tips']:
                f.write("## Tips:\n")
                for t in q['tips']:
                    f.write(f"  {t}\n")

        print(f"Post: {post_path}")
        print(f"Image: {img_path}")
        print(f"Score: {q['score']}/{q['max']} ({q['grade']})")

    else:
        parser.print_help()
        print("\nExamples:")
        print("  python3 generate_post.py --batch")
        print("  python3 generate_post.py --newsletter path/to/newsletter.html")
        print('  python3 generate_post.py --topic "Kubernetes Cost Optimization"')


if __name__ == '__main__':
    main()
