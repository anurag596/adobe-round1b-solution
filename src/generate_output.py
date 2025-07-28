# import json
# from datetime import datetime

# def write_output(ranked_sections, persona, job, docs, output_path):
#     out = {
#         "metadata": {
#             "input_documents": docs,
#             "persona": persona,
#             "job": job,
#             "timestamp": datetime.utcnow().isoformat() + 'Z'
#         },
#         "extracted_sections": [],
#         "subsection_analysis": []
#     }

#     for sec in ranked_sections:
#         out['extracted_sections'].append({
#             "document": sec['doc'],
#             "page": sec['page'],
#             "section_title": sec['heading'],
#             "importance_rank": sec['importance_rank']
#         })
#         # only 1 paragraph per section to keep JSON small
#         if 'content' in sec:
#             first_para = sec['content'].split('\n\n', 1)[0].strip()
#             if len(first_para) > 100:
#                 out['subsection_analysis'].append({
#                     "document": sec['doc'],
#                     "page": sec['page'],
#                     "refined_text": first_para,
#                     "importance_rank": f"{sec['importance_rank']}.1"
#                 })

#     with open(output_path, 'w', encoding='utf-8') as f:
#         json.dump(out, f, indent=2)


import json
from datetime import datetime
from summarize import summarize_text

def write_output(sections, persona, job, docs, out_path):
    out = {
        "metadata": {
            "input_documents": docs,
            "persona": persona,
            "job": job,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for sec in sections:
        out["extracted_sections"].append({
            "document": sec["doc"],
            "page_number": sec["page"],
            "section_title": sec["heading"],
            "importance_rank": sec["importance_rank"]
        })
        refined = summarize_text(sec["content"])
        out["subsection_analysis"].append({
            "document": sec["doc"],
            "page_number": sec["page"],
            "refined_text": refined,
            "importance_rank": f"{sec['importance_rank']}.1"
        })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
