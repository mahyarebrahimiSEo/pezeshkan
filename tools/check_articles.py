import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('mag/content/articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for a in articles:
    print(f"ID: {a['id']} | Category: {a.get('categoryName')} | Title: {a.get('title')}")
