import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s#+.-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def match_resume_to_jd(resume_text: str, jd_text: str, top_missing: int = 12) -> dict:
    r = normalize(resume_text)
    j = normalize(jd_text)

    vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_features=2500)
    X = vec.fit_transform([r, j])
    score = float(cosine_similarity(X[0], X[1])[0][0])
    match_pct = round(score * 100, 1)

    # "Missing keywords" heuristic: terms with high TF-IDF in JD but low in resume
    feature_names = vec.get_feature_names_out()
    r_vec = X[0].toarray()[0]
    j_vec = X[1].toarray()[0]
    gap = j_vec - r_vec

    missing_idx = gap.argsort()[::-1]
    missing = [feature_names[i] for i in missing_idx if gap[i] > 0][:top_missing]

    return {"match_percent": match_pct, "missing_keywords": missing}
