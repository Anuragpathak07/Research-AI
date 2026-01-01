# api/paper_generation.py
from flask import Blueprint, jsonify, request
from services.knowledge_base import KnowledgeBase
from services.llm_service import LLMService
import json

paper_generation_bp = Blueprint("paper_generation", __name__)
llm_service = LLMService()
knowledge_base = KnowledgeBase()

def format_context_for_llm(context, content_map):
    """Format context into a structured prompt with full content"""
    formatted = []
    
    if context and context.get("papers"):
        formatted.append("## Relevant Papers:")
        for paper_meta in context["papers"][:5]:  # Top 5 papers
            paper_id = paper_meta.get("id")
            if not paper_id:
                continue
            paper_content = content_map.get(("paper", str(paper_id)), {}) or {}
            title = paper_content.get("title") or paper_meta.get("title", "Unknown")
            abstract = paper_content.get("abstract", "") or ""
            year = paper_content.get("year", "") or ""
            formatted.append(f"\n### {title}" + (f" ({year})" if year else ""))
            if abstract:
                formatted.append(f"Abstract: {abstract[:300]}...")
    
    if context and context.get("synthesis"):
        formatted.append("\n\n## Synthesis Insights:")
        for synth_meta in context["synthesis"][:3]:  # Top 3 synthesis sections
            synth_id = synth_meta.get("id")
            if not synth_id:
                continue
            synth_content = content_map.get(("synthesis", str(synth_id)), {}) or {}
            title = synth_content.get("title") or synth_meta.get("title", "Unknown")
            content = synth_content.get("content", "") or ""
            formatted.append(f"\n### {title}")
            if content:
                formatted.append(content[:500] + "..." if len(content) > 500 else content)
    
    if context and context.get("gaps"):
        formatted.append("\n\n## Research Gaps:")
        for gap_meta in context["gaps"][:3]:  # Top 3 gaps
            gap_id = gap_meta.get("id")
            if not gap_id:
                continue
            gap_content = content_map.get(("gap", str(gap_id)), {}) or {}
            title = gap_content.get("title") or gap_meta.get("title", "Unknown")
            why = gap_content.get("why", "") or ""
            formatted.append(f"\n### {title}")
            if why:
                formatted.append(f"Why: {why[:200]}...")
    
    if context and context.get("experiments"):
        formatted.append("\n\n## Proposed Experiments:")
        for exp_meta in context["experiments"][:2]:  # Top 2 experiments
            exp_id = exp_meta.get("id")
            if not exp_id:
                continue
            exp_content = content_map.get(("experiment", str(exp_id)), {}) or {}
            objective = exp_content.get("objective") or exp_meta.get("title", "Unknown")
            dataset = exp_content.get("dataset", "") or ""
            formatted.append(f"\n### {objective}")
            if dataset:
                formatted.append(f"Dataset: {dataset}")
    
    return "\n".join(formatted) if formatted else "No relevant context found."

@paper_generation_bp.route("/generate", methods=["POST"])
def generate_paper():
    try:
        data = request.json
        topic = data.get("topic", "")
        papers = data.get("papers", [])
        clusters = data.get("clusters", [])
        synthesis = data.get("synthesis", {})
        gaps = data.get("gaps", [])
        experiments = data.get("experiments", [])
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        if not papers:
            return jsonify({"error": "No papers available. Please discover papers first."}), 400
        
        # Transform clusters from frontend format to backend format if needed
        transformed_clusters = []
        if clusters:
            for cluster in clusters:
                # Check if already in backend format
                if "cluster_id" in cluster:
                    transformed_clusters.append(cluster)
                else:
                    # Transform from frontend format
                    transformed_cluster = {
                        "cluster_id": str(cluster.get("id", cluster.get("cluster_id", ""))),
                        "name": cluster.get("name", ""),
                        "paper_count": cluster.get("papers", cluster.get("paper_count", 0)),
                        "key_papers": cluster.get("keyPapers", cluster.get("key_papers", [])),
                        "trajectory": cluster.get("trajectoryStatus", cluster.get("trajectory", "stable")),
                        "papers": cluster.get("papersData", cluster.get("papers", []))
                    }
                    transformed_clusters.append(transformed_cluster)
        
        # Build knowledge base
        try:
            kb_size = knowledge_base.build_knowledge_base(
                papers=papers,
                clusters=transformed_clusters,
                synthesis=synthesis,
                gaps=gaps,
                experiments=experiments
            )
            
            if not kb_size or kb_size == 0:
                return jsonify({
                    "error": "Failed to build knowledge base",
                    "details": "No content available to build knowledge base. Please ensure you have papers, clusters, or synthesis data."
                }), 500
        except Exception as e:
            print(f"Error building knowledge base: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                "error": f"Failed to build knowledge base: {str(e)}"
            }), 500
        
        # Get relevant context
        try:
            context = knowledge_base.get_context_for_paper_generation(topic, max_chunks=15)
            
            # Get full content for retrieved items
            content_map = knowledge_base.get_full_content(
                papers=papers,
                clusters=transformed_clusters,
                synthesis=synthesis,
                gaps=gaps,
                experiments=experiments
            )
            
            context_text = format_context_for_llm(context, content_map)
            
            if not context_text or len(context_text.strip()) < 50:
                return jsonify({
                    "error": "Insufficient context for paper generation",
                    "details": "The knowledge base does not contain enough relevant content for the given topic. Please ensure you have generated clusters and synthesis data."
                }), 400
        except Exception as e:
            print(f"Error getting context: {e}")
            return jsonify({
                "error": f"Failed to retrieve context: {str(e)}"
            }), 500
        
        # Generate paper using RAG
        prompt = f"""You are a research paper writer. Generate a comprehensive research paper on the topic: "{topic}"

Use the following knowledge base as context:

{context_text}

Generate a research paper with the following structure:
1. Abstract (150-200 words)
2. Introduction (2-3 paragraphs)
3. Related Work (2-3 paragraphs based on the papers provided)
4. Methodology (2-3 paragraphs)
5. Results and Discussion (2-3 paragraphs)
6. Conclusion (1-2 paragraphs)
7. References (list key papers from the context)

Write in academic style, cite relevant work from the context, and ensure the paper is coherent and well-structured. Use **bold** for section headers and key terms."""

        try:
            paper_content = llm_service.generate(prompt, temperature=0.7)
        except Exception as e:
            return jsonify({
                "error": f"Failed to generate paper: {str(e)}",
                "suggestion": "Please ensure Ollama is running and the model is available."
            }), 500
        
        return jsonify({
            "topic": topic,
            "paper": paper_content,
            "context_used": {
                "papers": len(context.get("papers", [])),
                "synthesis": len(context.get("synthesis", [])),
                "gaps": len(context.get("gaps", [])),
                "experiments": len(context.get("experiments", []))
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@paper_generation_bp.route("/store", methods=["POST"])
def store_data():
    """Store clusters, synthesis, gaps, and experiments"""
    try:
        data = request.json
        
        # Transform clusters from frontend format to backend format
        clusters = data.get("clusters", [])
        transformed_clusters = []
        for cluster in clusters:
            # Frontend format: id, papers, keyPapers, etc.
            # Backend format: cluster_id, paper_count, key_papers, etc.
            transformed_cluster = {
                "cluster_id": str(cluster.get("id", cluster.get("cluster_id", ""))),
                "name": cluster.get("name", ""),
                "paper_count": cluster.get("papers", cluster.get("paper_count", 0)),
                "key_papers": cluster.get("keyPapers", cluster.get("key_papers", [])),
                "trajectory": cluster.get("trajectoryStatus", cluster.get("trajectory", "stable")),
                "papers": cluster.get("papersData", cluster.get("papers", []))
            }
            transformed_clusters.append(transformed_cluster)
        
        # Store in a simple in-memory cache (can be replaced with DB later)
        synthesis_data = data.get("synthesis")
        if synthesis_data is None:
            synthesis_data = {}
        
        stored_data = {
            "clusters": transformed_clusters,
            "synthesis": synthesis_data,
            "gaps": data.get("gaps", []),
            "experiments": data.get("experiments", []),
            "papers": data.get("papers", [])
        }
        
        # In a real implementation, you'd save to database
        # For now, we'll use the knowledge base to store it
        try:
            kb_size = knowledge_base.build_knowledge_base(
                papers=stored_data["papers"],
                clusters=stored_data["clusters"],
                synthesis=stored_data["synthesis"],
                gaps=stored_data["gaps"],
                experiments=stored_data["experiments"]
            )
            
            if not kb_size or kb_size == 0:
                # This is okay - might not have enough data yet
                print("Warning: Knowledge base built with 0 items")
        except Exception as kb_error:
            print(f"Error building knowledge base: {kb_error}")
            # Don't fail the request if KB build fails - data is still stored
            import traceback
            traceback.print_exc()
        
        return jsonify({
            "status": "success",
            "message": "Data stored successfully",
            "stored": {
                "papers": len(stored_data["papers"]),
                "clusters": len(stored_data["clusters"]),
                "synthesis_sections": len(stored_data["synthesis"].get("sections", {})) if stored_data["synthesis"] else 0,
                "gaps": len(stored_data["gaps"]),
                "experiments": len(stored_data["experiments"])
            }
        })
        
    except Exception as e:
        print(f"Error in store_data: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

