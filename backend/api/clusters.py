# api/clusters.py
from flask import Blueprint, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from collections import Counter
import re

clusters_bp = Blueprint("clusters", __name__)

def extract_keywords(text, top_n=5):
    """Extract top keywords from text"""
    if not text:
        return []
    
    # Simple keyword extraction - find important terms
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    # Filter common stop words
    stop_words = {'this', 'that', 'these', 'those', 'with', 'from', 'have', 'been', 'were', 
                  'their', 'there', 'which', 'would', 'could', 'should', 'about', 'using',
                  'based', 'paper', 'study', 'research', 'method', 'approach', 'results',
                  'propose', 'present', 'show', 'demonstrate', 'analysis', 'evaluation'}
    words = [w for w in words if w not in stop_words and len(w) > 3]
    
    word_counts = Counter(words)
    return [word for word, _ in word_counts.most_common(top_n)]

def generate_cluster_name(papers_in_cluster):
    """Generate a meaningful cluster name from papers"""
    if not papers_in_cluster:
        return "Unknown Cluster"
    
    # Combine all abstracts and titles
    all_text = " ".join([
        (p.get("title", "") + " " + p.get("abstract", "")).lower() 
        for p in papers_in_cluster[:10]  # Use first 10 papers
    ])
    
    # Extract keywords
    keywords = extract_keywords(all_text, top_n=3)
    
    if keywords:
        # Create name from top keywords
        name = " ".join([kw.capitalize() for kw in keywords[:2]])
        if len(name) < 10:
            name = " ".join([kw.capitalize() for kw in keywords[:3]])
        return name[:50]  # Limit length
    
    # Fallback: use common terms from titles
    title_words = []
    for p in papers_in_cluster[:5]:
        title = p.get("title", "")
        if title:
            words = re.findall(r'\b[A-Z][a-z]+\b', title)
            title_words.extend(words[:3])
    
    if title_words:
        common_words = Counter(title_words).most_common(2)
        if common_words:
            return " ".join([word for word, _ in common_words])
    
    return f"Research Cluster {len(papers_in_cluster)}"

def get_key_papers(papers_in_cluster, max_papers=3):
    """Get key papers from cluster - prioritize by year and title quality"""
    if not papers_in_cluster:
        return []
    
    # Sort by year (most recent first), then by title length (more descriptive)
    sorted_papers = sorted(
        papers_in_cluster,
        key=lambda p: (p.get("year", 0), len(p.get("title", ""))),
        reverse=True
    )
    
    key_papers = []
    for p in sorted_papers[:max_papers]:
        title = p.get("title", "Untitled")
        year = p.get("year", "")
        authors = p.get("authors", [])
        
        # Format: "Title (Year)" or "Title (First Author, Year)"
        if authors and isinstance(authors, list) and len(authors) > 0:
            first_author = authors[0].split()[-1] if authors[0] else ""
            paper_str = f"{title} ({first_author} et al., {year})" if year else title
        else:
            paper_str = f"{title} ({year})" if year else title
        
        key_papers.append(paper_str)
    
    return key_papers

def cluster_papers(papers, k=None):
    if not papers:
        return []
    
    # Auto-determine number of clusters (between 3 and 8, based on paper count)
    if k is None:
        k = min(max(3, len(papers) // 5), 8)
    
    texts = [p.get("abstract", "") or p.get("title", "") for p in papers]
    if not any(texts):
        return []
    
    vectorizer = TfidfVectorizer(stop_words="english", max_features=2000, min_df=1)
    try:
        X = vectorizer.fit_transform(texts)
    except ValueError:
        # Fallback if vectorization fails
        return []
    
    if X.shape[0] < k:
        k = max(2, X.shape[0] // 2)
    
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X)

    clusters = {}
    for label, paper in zip(labels, papers):
        clusters.setdefault(label, []).append(paper)

    results = []
    for cid, plist in clusters.items():
        if not plist:
            continue
            
        years = [p.get("year", 2020) for p in plist if p.get("year")]
        avg_year = np.mean(years) if years else 2020
        
        # Determine trajectory based on average year
        if avg_year > 2022:
            trend = "Rising"
        elif avg_year < 2020:
            trend = "Declining"
        elif len(plist) > 15:
            trend = "Saturating"
        else:
            trend = "Stable"
        
        # Generate meaningful name
        cluster_name = generate_cluster_name(plist)
        
        # Get key papers
        key_papers = get_key_papers(plist, max_papers=3)
        
        # Get year distribution for timeline
        year_distribution = Counter([p.get("year", 2020) for p in plist if p.get("year")])
        
        results.append({
            "cluster_id": str(cid),
            "name": cluster_name,
            "paper_count": len(plist),
            "trajectory": trend,
            "papers": plist,
            "key_papers": key_papers,
            "avg_year": float(avg_year),
            "year_distribution": dict(year_distribution)
        })
    
    # Sort by paper count (descending)
    results.sort(key=lambda x: x["paper_count"], reverse=True)
    
    return results

@clusters_bp.route("/", methods=["POST"])
def clusters():
    try:
        papers = request.json or []
        if not papers:
            return jsonify([])
        
        results = cluster_papers(papers)
        return jsonify(results)
    except Exception as e:
        print(f"Error in clustering: {e}")
        return jsonify({"error": str(e)}), 500
