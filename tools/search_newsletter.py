import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
search_terms = ['خبرنامه و ویژه‌نامه‌های سلامت', 'تریاژ دردهای حاد قفسه سینه', 'مشاهده نسخه کامل خبرنامه', 'دستورالعمل بالینی تشخیص سریع']

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith(('.html', '.js', '.json', '.py')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for term in search_terms:
                        if term in content:
                            print(f'Found "{term}" in {filepath}')
            except Exception:
                pass
