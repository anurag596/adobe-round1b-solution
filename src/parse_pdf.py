# import fitz
# import numpy as np
# import re
# from PIL import Image
# import pytesseract  # keep installed, used only when needed

# OCR_LANGS = "eng+hin+jpn+chi_sim"
# NUM_PREFIX_RE = re.compile(r"^(\d+\.)+\s*")

# def extract_line_objects(pdf_path, ocr_fallback=True):
#     doc = fitz.open(pdf_path)
#     all_lines = []
#     for page_num in range(len(doc)):
#         page = doc[page_num]
#         # check if page has any selectable text
#         full_text = page.get_text("text").strip()
#         do_ocr = ocr_fallback and not full_text
#         blocks = page.get_text("dict")["blocks"]
#         for b in blocks:
#             if b["type"] != 0:
#                 continue
#             for line in b["lines"]:
#                 spans = line["spans"]
#                 text = "".join(span["text"] for span in spans).strip()
#                 sizes = [span["size"] for span in spans]

#                 # if no selectable text in spans and page has none, run OCR
#                 if not text and do_ocr:
#                     x0 = min(s["bbox"][0] for s in spans)
#                     y0 = min(s["bbox"][1] for s in spans)
#                     x1 = max(s["bbox"][2] for s in spans)
#                     y1 = max(s["bbox"][3] for s in spans)
#                     clip = page.get_pixmap(clip=fitz.Rect(x0, y0, x1, y1))
#                     img = Image.frombytes("RGB", [clip.width, clip.height], clip.samples)
#                     text = pytesseract.image_to_string(img, lang=OCR_LANGS).strip()
#                     sizes = [12.0]

#                 if not text:
#                     continue

#                 # compute darkness
#                 colors = [span.get("color", (0,0,0)) for span in spans]
#                 if isinstance(colors[0], tuple):
#                     brightness = np.mean([np.mean(c) for c in colors])
#                 else:
#                     rgb = [((c>>16)&255, (c>>8)&255, c&255) for c in colors]
#                     brightness = np.mean([np.mean(c)/255 for c in rgb])
#                 darkness = round(1 - brightness, 3)

#                 x0 = min(s["bbox"][0] for s in spans)
#                 avg_size = float(np.mean(sizes))
#                 bold = any("Bold" in s["font"] for s in spans)
#                 num_prefix = bool(NUM_PREFIX_RE.match(text))

#                 all_lines.append({
#                     "doc": pdf_path,
#                     "page": page_num + 1,
#                     "text": text,
#                     "x0": x0,
#                     "y0": min(s["bbox"][1] for s in spans),
#                     "y1": max(s["bbox"][3] for s in spans),
#                     "avg_size": avg_size,
#                     "is_bold": int(bold),
#                     "num_prefix": int(num_prefix),
#                     "darkness": darkness
#                 })

#     # assign columns per page
#     out = []
#     for pg in set(l["page"] for l in all_lines):
#         page_lines = [l for l in all_lines if l["page"] == pg]
#         xs = [l["x0"] for l in page_lines]
#         if max(xs) - min(xs) > 100:
#             mid = np.median(xs)
#             for l in page_lines:
#                 l["col"] = 0 if l["x0"] <= mid else 1
#         else:
#             for l in page_lines:
#                 l["col"] = 0
#         out.extend(page_lines)

#     return out


import fitz
import numpy as np
import re
from PIL import Image
import pytesseract  # keep installed, used only when needed

OCR_LANGS = "eng+hin+jpn+chi_sim"
NUM_PREFIX_RE = re.compile(r"^(\d+\.)+\s*")

def extract_line_objects(pdf_path, ocr_fallback=True):
    doc = fitz.open(pdf_path)
    all_lines = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        # check if page has any selectable text
        full_text = page.get_text("text").strip()
        do_ocr = ocr_fallback and not full_text
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b["type"] != 0:
                continue
            for line in b["lines"]:
                spans = line["spans"]
                text = "".join(span["text"] for span in spans).strip()
                sizes = [span["size"] for span in spans]

                # if no selectable text in spans and page has none, run OCR
                if not text and do_ocr:
                    x0 = min(s["bbox"][0] for s in spans)
                    y0 = min(s["bbox"][1] for s in spans)
                    x1 = max(s["bbox"][2] for s in spans)
                    y1 = max(s["bbox"][3] for s in spans)
                    clip = page.get_pixmap(clip=fitz.Rect(x0, y0, x1, y1))
                    img = Image.frombytes("RGB", [clip.width, clip.height], clip.samples)
                    text = pytesseract.image_to_string(img, lang=OCR_LANGS).strip()
                    sizes = [12.0]

                if not text:
                    continue

                # compute darkness
                colors = [span.get("color", (0,0,0)) for span in spans]
                if isinstance(colors[0], tuple):
                    brightness = np.mean([np.mean(c) for c in colors])
                else:
                    rgb = [((c>>16)&255, (c>>8)&255, c&255) for c in colors]
                    brightness = np.mean([np.mean(c)/255 for c in rgb])
                darkness = round(1 - brightness, 3)

                x0 = min(s["bbox"][0] for s in spans)
                avg_size = float(np.mean(sizes))
                bold = any("Bold" in s["font"] for s in spans)
                num_prefix = bool(NUM_PREFIX_RE.match(text))

                all_lines.append({
                    "doc": pdf_path,
                    "page": page_num + 1,
                    "text": text,
                    "x0": x0,
                    "y0": min(s["bbox"][1] for s in spans),
                    "y1": max(s["bbox"][3] for s in spans),
                    "avg_size": avg_size,
                    "is_bold": int(bold),
                    "num_prefix": int(num_prefix),
                    "darkness": darkness
                })

    # assign columns per page
    out = []
    for pg in set(l["page"] for l in all_lines):
        page_lines = [l for l in all_lines if l["page"] == pg]
        xs = [l["x0"] for l in page_lines]
        if max(xs) - min(xs) > 100:
            mid = np.median(xs)
            for l in page_lines:
                l["col"] = 0 if l["x0"] <= mid else 1
        else:
            for l in page_lines:
                l["col"] = 0
        out.extend(page_lines)

    return out
