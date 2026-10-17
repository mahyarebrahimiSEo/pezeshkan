import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('mag/index.html', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'newslettersData' in line:
            print(f'{idx+1}: {line.strip()[:100]}')
