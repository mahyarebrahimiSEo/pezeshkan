import sys, glob, re
sys.stdout.reconfigure(encoding='utf-8')

for p in glob.glob('new data for design and hero section/vital-frame-assets/**/*.svg', recursive=True):
    if 'dark' in p.lower():
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        print("FILE:", p)
        # Find any text or dial group
        texts = re.findall(r'<text[^>]*>.*?</text>', c)
        print("  texts:", texts)
        # Check if 30 or ۳۰ or polygon
        if '۳۰' in c:
            print("  Contains Persian 30 (۳۰)")
        if 'scale(1.25 .88)' in c:
            print("  Contains 7-segment 30 polygon")
        # Search for any '30' or '3' or '0' in text
        matches = re.findall(r'<text[^>]*>[^<]*30[^<]*</text>', c)
        print("  English 30 texts:", matches)
        # Search for font-family
        fonts = set(re.findall(r'font-family="([^"]+)"', c))
        print("  fonts:", fonts)
        print("-" * 50)
