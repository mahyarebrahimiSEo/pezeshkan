# -*- coding: utf-8 -*-
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

content = open('data.html', encoding='utf-8').read()
cards = re.split(r'<div class="panel-card"', content)[1:]

print("--- FULL CARD 1 (Homepage) ---")
print(cards[0])
