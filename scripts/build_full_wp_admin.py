# -*- coding: utf-8 -*-
"""
Builds the perfected WordPress-grade Pezeshkan Medical CMS Studio (mag/admin.html)
Features:
- Complete removal of any mention of "tiptap" in user-facing UI
- Full WordPress-style Media Library (upload from PC, select existing, Alt text, copy URL)
- Full WordPress-style Media Inserter modal for Editor & Featured Image
- Comprehensive Yoast / RankMath Style SEO Suite in Article Editor:
  - Focus Keyword
  - Google SERP Snippet Preview (Desktop & Mobile)
  - SEO Title & Meta Description with live progress bars and character limits
  - Automated Slug generator
  - Live SEO Audit Checklist with Traffic Light Score (0-100)
  - Schema.org Structured Data Generator (MedicalWebPage, Article, FAQPage)
  - Interactive FAQ Builder with automatic FAQ Schema JSON-LD injection
  - Social Sharing Open Graph Preview
- Posts Management with Status Tabs (All, Published, Drafts, Trash) + Quick Edit
- Site-Wide SEO & Google Verification Suite in Settings
- Full RTL Persian typography & clinical branding
"""

import json
import os

BASE_DIR = r"e:\antigravity\pezeshkan_design"
MAG_DIR = os.path.join(BASE_DIR, "mag")

# Load content
with open(os.path.join(MAG_DIR, "content", "pillars.json"), encoding="utf-8") as f:
    pillars_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "doctors.json"), encoding="utf-8") as f:
    doctors_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "articles.json"), encoding="utf-8") as f:
    articles_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "settings.json"), encoding="utf-8") as f:
    settings_data = json.load(f)

media_file = os.path.join(MAG_DIR, "content", "media.json")
if os.path.exists(media_file):
    with open(media_file, encoding="utf-8") as f:
        media_data = json.load(f)
else:
    media_data = []

pillars_json_str = json.dumps(pillars_data, ensure_ascii=False)
doctors_json_str = json.dumps(doctors_data, ensure_ascii=False)
articles_json_str = json.dumps(articles_data, ensure_ascii=False)
settings_json_str = json.dumps(settings_data, ensure_ascii=False)
media_json_str = json.dumps(media_data, ensure_ascii=False)

print(f"Loaded: {len(pillars_data)} pillars, {len(doctors_data)} doctors, {len(articles_data)} articles, {len(media_data)} media items.")
