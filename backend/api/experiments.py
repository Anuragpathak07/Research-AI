# api/experiments.py
from flask import Blueprint, jsonify, request
from agents.experiment_agent import ExperimentAgent

experiments_bp = Blueprint("experiments", __name__)
experiment_agent = ExperimentAgent()

@experiments_bp.route("/", methods=["POST"])
def experiments():
    try:
        gaps_data = request.json or []
        if not gaps_data:
            return jsonify([])
        
        # Transform gaps to format expected by agent
        gaps = []
        for g in gaps_data:
            gaps.append({
                "id": g.get("id", ""),
                "title": g.get("gap", g.get("title", "Unknown")),
                "temporalViability": g.get("viability", "future-viable").lower().replace(" ", "-"),
                "why": g.get("reason", g.get("why", "")),
                "evidence": g.get("evidence", "")
            })
        
        # Use agentic experiment agent to propose experiments
        proposed_experiments = experiment_agent.propose_experiments(gaps)
        
        # Transform to frontend format
        formatted_experiments = []
        for exp in proposed_experiments:
            formatted_experiments.append({
                "objective": exp.get("objective", "Unknown objective"),
                "datasets": exp.get("dataset", exp.get("datasets", [])),
                "models": exp.get("models", []),
                "metrics": exp.get("metrics", []),
                "code_stub": "train.py / evaluate.py",
                "expected_outcome": exp.get("outcome", "To be determined"),
                "temporal_relevance": exp.get("temporalRelevance", ""),
                "future_proof_design": exp.get("futureProofDesign", "")
            })
        
        return jsonify(formatted_experiments)
    except Exception as e:
        print(f"Error in experiments endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
