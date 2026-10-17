import glob
import re

files = sorted(glob.glob('portal/*.html'))
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    header_part = c.split('</header>')[0] if '</header>' in c else c
    matches = re.findall(r'<a\s+[^>]*href="([^"]*)"[^>]*class="[^"]*active[^"]*"', header_part)
    matches += re.findall(r'<a\s+[^>]*class="[^"]*active[^"]*"[^>]*href="([^"]*)"', header_part)
    print(f"{f:22} : active href -> {matches}")
