# import warnings
# # Suppress all FutureWarnings (for HuggingFace torch deprecation)
# warnings.filterwarnings("ignore", category=FutureWarning)

# import argparse
# import os
# from parse_pdf import parse_pdfs
# from extract_headings import extract_headings
# from predict_headings import load_heading_model, predict_heading
# from rank_sections import rank_sections
# from generate_output import write_output

# def main(input_dir, persona_file, job_file, model_dir, output_file):
#     pdf_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
#     docs = parse_pdfs(pdf_paths)

#     heading_model = load_heading_model(model_dir)
#     sections = extract_headings(docs, heading_model)

#     persona_text = open(persona_file, 'r', encoding='utf-8').read().strip()
#     job_text = open(job_file, 'r', encoding='utf-8').read().strip()

#     ranked = rank_sections(sections, persona_text, job_text, top_k=5)
#     write_output(ranked, persona_text, job_text, pdf_paths, output_file)

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--input', required=True)
#     parser.add_argument('--persona', required=True)
#     parser.add_argument('--job', required=True)
#     parser.add_argument('--model', required=True)
#     parser.add_argument('--output', required=True)
#     args = parser.parse_args()
#     main(args.input, args.persona, args.job, args.model, args.output)


import warnings
warnings.filterwarnings("ignore", message=".*encoder_attention_mask.*", category=FutureWarning)

import argparse
import os

from parse_pdf import extract_line_objects
from extract_headings import extract_headings
from predict_headings import load_heading_model
from rank_sections import rank_sections
from generate_output import write_output

def main(input_dir, persona_file, job_file, model_dir, out_file):
    # 1. Parse PDFs
    all_blocks = []
    for fn in sorted(os.listdir(input_dir)):
        if fn.lower().endswith(".pdf"):
            path = os.path.join(input_dir, fn)
            all_blocks.extend(extract_line_objects(path))

    # 2. Load heading model and extract sections
    model = load_heading_model(model_dir)
    secs = extract_headings(all_blocks, model)

    # 3. Read persona & job
    persona = open(persona_file, encoding="utf-8").read().strip()
    job = open(job_file, encoding="utf-8").read().strip()

    # 4. Rank & summarize
    ranked = rank_sections(secs, persona, job, top_k=5)

    # 5. Generate JSON
    docs = sorted([fn for fn in os.listdir(input_dir) if fn.lower().endswith(".pdf")])
    write_output(ranked, persona, job, docs, out_file)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--persona", required=True)
    p.add_argument("--job", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    main(args.input, args.persona, args.job, args.model, args.output)
