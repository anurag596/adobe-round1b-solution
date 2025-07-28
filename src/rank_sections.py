# src/rank_sections.py

# from sentence_transformers import SentenceTransformer, util
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np

# _embedder = SentenceTransformer('all-MiniLM-L6-v2')

# def rank_sections(sections, persona, job, top_k=5, tfidf_weight=0.4):
#     texts = [f"{s['heading']}. {s['content'][:200]}" for s in sections]
#     query = persona + " " + job

#     # TF-IDF scoring
#     vectorizer = TfidfVectorizer(stop_words='english')
#     mat = vectorizer.fit_transform(texts + [query])
#     tfidf_scores = (mat[-1] @ mat[:-1].T).toarray()[0]

#     # SBERT scoring
#     emb = _embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
#     q_emb = _embedder.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
#     sbert_scores = util.cos_sim(q_emb, emb)[0].cpu().numpy()

#     # Hybrid score
#     hybrid = tfidf_weight * tfidf_scores + (1 - tfidf_weight) * sbert_scores
#     idxs = np.argsort(-hybrid)[:top_k]

#     ranked = []
#     seen = set()
#     # pick top_k unique sections
#     for rank, i in enumerate(idxs, start=1):
#         sec = sections[i].copy()
#         key = (sec['doc'], sec['heading'])
#         if key in seen:
#             continue
#         seen.add(key)
#         sec['relevance_score'] = float(hybrid[i])
#         sec['importance_rank'] = rank
#         ranked.append(sec)

#     # pad up to top_k with next-best unique sections
#     for sec in sections:
#         if len(ranked) >= top_k:
#             break
#         key = (sec['doc'], sec['heading'])
#         if key in seen:
#             continue
#         seen.add(key)
#         pad = sec.copy()
#         pad['relevance_score'] = 0.0
#         pad['importance_rank'] = len(ranked) + 1
#         ranked.append(pad)

#     return ranked


from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

_embedder = SentenceTransformer('all-MiniLM-L6-v2')

def rank_sections(sections, persona, job, top_k=5, tfidf_weight=0.4):
    texts = [f"{s['heading']}. {s['content'][:200]}" for s in sections]
    query = persona + " " + job

    # TF-IDF scoring
    vectorizer = TfidfVectorizer(stop_words='english')
    mat = vectorizer.fit_transform(texts + [query])
    tfidf_scores = (mat[-1] @ mat[:-1].T).toarray()[0]

    # SBERT scoring
    emb = _embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    q_emb = _embedder.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
    sbert_scores = util.cos_sim(q_emb, emb)[0].cpu().numpy()

    # Hybrid score
    hybrid = tfidf_weight * tfidf_scores + (1 - tfidf_weight) * sbert_scores

    # Pick top_k indices
    idxs = np.argsort(-hybrid)[:top_k]

    ranked = []
    seen = set()
    # Add highest-scoring unique ones
    for rank, i in enumerate(idxs, start=1):
        sec = sections[i].copy()
        key = (sec['doc'], sec['heading'])
        if key in seen:
            continue
        seen.add(key)
        sec['relevance_score'] = float(hybrid[i])
        sec['importance_rank'] = rank
        ranked.append(sec)

    # Pad up to exactly top_k with next-best uniques
    for i in np.argsort(-hybrid):
        if len(ranked) >= top_k:
            break
        sec = sections[i].copy()
        key = (sec['doc'], sec['heading'])
        if key in seen:
            continue
        seen.add(key)
        sec['relevance_score'] = 0.0
        sec['importance_rank'] = len(ranked) + 1
        ranked.append(sec)

    return ranked
