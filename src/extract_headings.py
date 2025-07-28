# import re
# from predict_headings import predict_heading

# # Heuristics to prune spurious headings
# MIN_HEADING_LEN = 5
# HEADING_VALID_RE = re.compile(r"[A-Za-z]{2,}")  # at least two letters

# def extract_headings(docs, model):
#     """
#     Detect headings and filter out non‑meaningful ones like 'X2', '0.8', etc.
#     """
#     sections = []
#     buf = {"doc": None, "page": None, "heading": None, "content": []}

#     for block in docs:
#         text = block["text"].strip()
#         is_h = (
#             predict_heading(block, model)
#             and len(text) >= MIN_HEADING_LEN
#             and HEADING_VALID_RE.search(text)
#         )
#         if is_h:
#             if buf["heading"] and len(buf["content"]) > 3:
#                 sections.append({**buf, "content": "\n".join(buf["content"])})
#             buf = {"doc": block["doc"], "page": block["page"], "heading": text, "content": []}
#         else:
#             if buf["heading"]:
#                 buf["content"].append(text)

#     if buf["heading"] and len(buf["content"]) > 3:
#         sections.append({**buf, "content": "\n".join(buf["content"])})
#     return sections
from predict_headings import load_heading_model, predict_heading
import re

MIN_HEADING_LEN = 5
HEADING_START_RE = re.compile(r"^[A-Z]")
LETTERS_RE = re.compile(r"[A-Za-z]")

def extract_headings(blocks, model):
    sections = []
    buf = {"doc": None, "page": None, "heading": None, "content": []}
    for blk in blocks:
        text = blk["text"].strip()
        is_h2 = (
            predict_heading(blk, model)
            and len(text) >= MIN_HEADING_LEN
            and HEADING_START_RE.match(text)
            and len(LETTERS_RE.findall(text)) > len(re.findall(r"\d", text))
        )
        if is_h2:
            if buf["heading"]:
                sections.append({
                    **buf,
                    "content": " ".join(buf["content"]).strip()
                })
            buf = {
                "doc": blk["doc"],
                "page": blk["page"],
                "heading": text,
                "content": []
            }
        else:
            if buf["heading"]:
                buf["content"].append(text)
    if buf["heading"]:
        sections.append({
            **buf,
            "content": " ".join(buf["content"]).strip()
        })
    return sections
