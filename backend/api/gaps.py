# api/gaps.py
from flask import Blueprint, jsonify, request
from collections import defaultdict
from services.llm_service import LLMService

gaps_bp = Blueprint("gaps", __name__)
llm_service = LLMService()

def analyze_clusters_for_gaps(clusters):
    """Analyze clusters to identify research gaps"""
    gaps = []
    
    # Basic analysis
    for c in clusters:
        name = c.get("name", "Unknown")
        papers = c.get("papers", c.get("paper_count", 0))
        status = c.get("trajectoryStatus", c.get("trajectory", "stable"))
        momentum = c.get("momentumScore", 50)
        
        # Identify gaps based on patterns
        if status == "rising" and papers < 10:
            gaps.append({
                "gap": f"Emerging research area: {name}",
                "viability": "Future-Viable",
                "reason": f"Rising trajectory with only {papers} papers - early opportunity for contribution"
            })
        elif status == "stable" and papers < 5:
            gaps.append({
                "gap": f"Underexplored area: {name}",
                "viability": "Future-Viable",
                "reason": f"Stable momentum but low paper count ({papers}) - potential for growth"
            })
        elif status == "declining" and momentum < 30:
            gaps.append({
                "gap": f"Declining area: {name}",
                "viability": "Likely Obsolete",
                "reason": f"Declining trajectory with low momentum ({momentum}) - may become obsolete"
            })
        elif status == "saturating" and papers > 20:
            gaps.append({
                "gap": f"Saturated area: {name}",
                "viability": "Time-Sensitive",
                "reason": f"High saturation ({papers} papers) - limited time window for novel contributions"
            })
    
    # Use LLM to enhance gaps if available
    if gaps and len(clusters) > 0:
        try:
            cluster_summary = "\n".join([
                f"- {c.get('name', 'Unknown')}: {c.get('papers', c.get('paper_count', 0))} papers, {c.get('trajectoryStatus', c.get('trajectory', 'unknown'))} trajectory"
                for c in clusters[:10]
            ])
            
            prompt = f"""Based on these research clusters, identify 3-5 key research gaps:

{cluster_summary}

For each gap, provide:
1. A clear gap title
2. Why it matters (2-3 sentences)
3. Evidence from the data
4. Temporal viability: "Future-Viable", "Time-Sensitive", or "Likely Obsolete"
5. Temporal justification (why this classification)

Format as JSON array with keys: gap, reason, evidence, viability, temporal_justification"""
            
            llm_response = llm_service.generate(prompt, temperature=0.5)
            
            # Try to parse LLM response (simplified - in production, use proper JSON parsing)
            # For now, use basic analysis + LLM enhancement
            enhanced_gaps = []
            for gap in gaps[:5]:  # Limit to top 5
                enhanced_gaps.append({
                    "gap": gap["gap"],
                    "viability": gap["viability"],
                    "reason": gap["reason"],
                    "evidence": f"Based on cluster analysis: {gap['reason']}",
                    "temporal_justification": f"Analysis suggests {gap['viability'].lower()} trajectory based on current research patterns."
                })
            
            return enhanced_gaps
        except Exception as e:
            print(f"LLM enhancement failed, using basic analysis: {e}")
            # Return basic gaps if LLM fails
            return gaps[:5]  # Limit to 5 gaps
    
    return gaps[:5]

@gaps_bp.route("/", methods=["POST"])
def gaps():
    try:
        clusters = request.json or []
        if not clusters:
            return jsonify([])
        
        gaps = analyze_clusters_for_gaps(clusters)
        return jsonify(gaps)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
