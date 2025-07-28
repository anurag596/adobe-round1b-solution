# # src/summarize.py
# import re

# SENT_RE = re.compile(r'([^.?!]+[.?!])')

# def summarize_text(text, max_sents=2, char_limit=200):
#     sents = SENT_RE.findall(text)
#     summary = ' '.join(s.strip() for s in sents[:max_sents])
#     return summary[:char_limit].rstrip() + ('…' if len(summary) > char_limit else '')

import re

SENT_RE = re.compile(r'([^.?!]+[.?!])')

def summarize_text(text, max_sents=2, char_limit=200):
    sents = SENT_RE.findall(text)
    summary = ' '.join(s.strip() for s in sents[:max_sents])
    if len(summary) > char_limit:
        return summary[:char_limit].rstrip() + '…'
    return summary
