import re

pattern = r'[^aeuio^\s]+'
text = 'The quick brown fox jumps over the lazy dog.'

matches = re.findall(pattern, text)

print(f"Pattern: {pattern}\nText: {text}\nMatches: {matches}\n")

