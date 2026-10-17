import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('mag/content/pillars.json', encoding='utf-8') as f:
    data = json.load(f)

total_branches = 0
total_clusters = 0

for idx, p in enumerate(data):
    b_count = len(p.get('branches', []))
    c_count = sum(len(b.get('clusters', [])) for b in p.get('branches', []))
    total_branches += b_count
    total_clusters += c_count
    name = p['name']
    slug = p['slug']
    print(f"[Pillar {idx+1}] {name} ({slug}) -> {b_count} شاخه, {c_count} کلاستر سئو")

print(f"\nمجموع کل: {len(data)} پیلار کلان، {total_branches} شاخه تخصصی، {total_clusters} کلاستر سئو")
