# api/gaps.py
from flask import Blueprint, jsonify, request
from agents.gap_agent import GapAgent
from agents.trajectory_agent import TrajectoryAgent
from agents.extraction_agent import ExtractionAgent

gaps_bp = Blueprint("gaps", __name__)
gap_agent = GapAgent()
trajectory_agent = TrajectoryAgent()
extraction_agent = ExtractionAgent()

def clusters_to_extracted_papers(clusters, use_fast_extraction=True):
    """Convert clusters format to extracted_papers format for agents"""
    extracted_papers = []
    for cluster in clusters:
        # Get papers from cluster
        papers_data = cluster.get("papersData", cluster.get("papers", []))
        if isinstance(papers_data, list) and len(papers_data) > 0:
            for paper in papers_data:
                if isinstance(paper, dict):
                    extracted_papers.append({
                        "paper_id": paper.get("paper_id") or paper.get("id", ""),
                        "title": paper.get("title", ""),
                        "abstract": paper.get("abstract", ""),
                        "year": paper.get("year", 2020),
                        "methods": [],  # Will be extracted
                        "datasets": [],
                        "metrics": []
                    })
    
    # Extract entities from papers
    # Use fast keyword-only extraction to avoid slow LLM calls
    if extracted_papers:
        if use_fast_extraction:
            # Fast keyword-based extraction only (no LLM calls)
            for p in extracted_papers:
                text = (p.get("abstract", "") + " " + p.get("title", "")).lower()
                # Quick keyword matching
                methods = [m for m in extraction_agent.METHOD_KEYWORDS if m in text]
                datasets = [d for d in extraction_agent.DATASET_KEYWORDS if d in text]
                metrics = [m for m in extraction_agent.METRIC_KEYWORDS if m in text]
                p["methods"] = list(set(methods))
                p["datasets"] = list(set(datasets))
                p["metrics"] = list(set(metrics))
        else:
            # Full LLM-based extraction (slower but more accurate)
            extracted_papers = extraction_agent.extract_entities(extracted_papers)
    
    return extracted_papers

def clusters_to_trajectories(clusters):
    """Convert clusters format to trajectories format for agents"""
    trajectories = {}
    for cluster in clusters:
        name = cluster.get("name", "Unknown")
        trajectory_status = cluster.get("trajectoryStatus", cluster.get("trajectory", "stable"))
        papers_count = cluster.get("papers", cluster.get("paper_count", 0))
        
        # Normalize trajectory status (capitalize first letter)
        if isinstance(trajectory_status, str):
            trajectory_status = trajectory_status.capitalize()
            # Map common variations
            if trajectory_status.lower() in ["rising", "increasing", "growing"]:
                trajectory_status = "Rising"
            elif trajectory_status.lower() in ["declining", "decreasing", "falling"]:
                trajectory_status = "Declining"
            elif trajectory_status.lower() in ["stable", "steady", "constant"]:
                trajectory_status = "Stable"
            elif trajectory_status.lower() in ["saturating", "saturated"]:
                trajectory_status = "Saturating"
        
        # Create trajectory entry
        trajectories[name] = {
            "trajectory": trajectory_status,
            "paper_count": papers_count if isinstance(papers_count, int) else 0,
            "years": [],
            "slope": 0.0
        }
    
    return trajectories

@gaps_bp.route("/", methods=["POST"])
def gaps():
    try:
        print(f"[GAPS] Received request with {len(request.json or [])} clusters")
        clusters = request.json or []
        if not clusters:
            return jsonify([])
        
        # Convert clusters to format expected by agents
        # Use fast extraction (keyword-only) to avoid slow LLM calls
        print("[GAPS] Extracting papers from clusters...")
        extracted_papers = clusters_to_extracted_papers(clusters, use_fast_extraction=True)
        print(f"[GAPS] Extracted {len(extracted_papers)} papers")
        
        # Build trajectories from clusters or extract from papers
        # Prefer using cluster data directly (faster) unless we have good extracted papers
        print("[GAPS] Building trajectories...")
        if extracted_papers and len(extracted_papers) > 10:
            # Only use trajectory agent if we have enough papers with extracted methods
            papers_with_methods = [p for p in extracted_papers if p.get("methods")]
            if papers_with_methods:
                print(f"[GAPS] Using trajectory agent with {len(papers_with_methods)} papers with methods")
                trajectories = trajectory_agent.build_trajectories(extracted_papers)
            else:
                print("[GAPS] Using cluster-based trajectories (no methods extracted)")
                trajectories = clusters_to_trajectories(clusters)
        else:
            print("[GAPS] Using cluster-based trajectories (few papers)")
            trajectories = clusters_to_trajectories(clusters)
        
        print(f"[GAPS] Built {len(trajectories)} trajectories")
        
        # Use agentic gap agent to detect gaps
        print("[GAPS] Detecting gaps...")
        detected_gaps = gap_agent.detect_gaps(trajectories, extracted_papers if extracted_papers else [])
        print(f"[GAPS] Detected {len(detected_gaps)} gaps")
        
        # Transform to frontend format
        formatted_gaps = []
        for i, gap in enumerate(detected_gaps):
            formatted_gaps.append({
                "id": gap.get("id", f"gap_{i+1}"),
                "gap": gap.get("title", "Unknown gap"),
                "viability": gap.get("temporalViability", "future-viable").replace("-", " ").title(),
                "reason": gap.get("why", gap.get("temporalJustification", "Analysis needed")),
                "evidence": gap.get("evidence", "Based on trajectory analysis"),
                "temporal_justification": gap.get("temporalJustification", gap.get("why", ""))
            })
        
        return jsonify(formatted_gaps[:10])  # Limit to top 10
    except Exception as e:
        print(f"Error in gaps endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
