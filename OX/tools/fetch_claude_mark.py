#!/usr/bin/env python3
"""Extract the unmodified official mark path from the public Claude wordmark SVG."""
import re
import sys
import urllib.request
from manage import ROOT
if '--stdin' in sys.argv: html=sys.stdin.read()
else:
    with urllib.request.urlopen('https://claude.com',timeout=25) as response: html=response.read().decode()
svg=next(x for x in re.findall(r'<svg\b[\s\S]*?</svg>',html) if 'ClaudeWordmark' in x)
paths=re.findall(r'<path\b[^>]*>(?:</path>)?',svg)
mark=next(x for x in paths if 'fill="#D97757"' in x)
source=ROOT/'icons/custom/sources'
(source/'claude-wordmark.svg').write_text(svg+'\n')
(source/'claude-mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 125 125">'+mark+'</svg>\n')
print('Extracted official 125x125 mark geometry without modifying its path.')
