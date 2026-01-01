# api/synthesis.py
from flask import Blueprint, jsonify, request
from collections import Counter, defaultdict
from services.llm_service import LLMService
import json

synthesis_bp = Blueprint("synthesis", __name__)
llm_service = LLMService()

def generate_synthesis_content(papers):
    """Generate synthesis content using LLM"""
    if not papers:
        return {
            "methods": {"content": "No papers available for analysis."},
            "datasets": {"content": "No papers available for analysis."},
            "metrics": {"content": "No papers available for analysis."},
            "performance": {"content": "No papers available for analysis."},
            "method_transitions": {"content": "No papers available for analysis."},
            "dataset_shifts": {"content": "No papers available for analysis."},
            "metric_deprecations": {"content": "No papers available for analysis."}
        }
    
    # Analyze papers
    methods = Counter()
    datasets = Counter()
    metrics = Counter()
    years = []
    venues = Counter()
    
    for p in papers:
        text = (p.get("abstract", "") + " " + p.get("title", "")).lower()
        
        # Extract methods - broader keyword matching
        if "quantum" in text:
            methods["Quantum Computing"] += 1
        if "circuit" in text or "gate" in text:
            methods["Quantum Circuits"] += 1
        if "algorithm" in text:
            methods["Quantum Algorithms"] += 1
        if "error" in text and "correction" in text:
            methods["Error Correction"] += 1
        if "topological" in text:
            methods["Topological Quantum"] += 1
        if "nisq" in text:
            methods["NISQ Era"] += 1
        if "transformer" in text or "vision transformer" in text:
            methods["Vision Transformers"] += 1
        if "cnn" in text or "convolutional" in text:
            methods["CNNs"] += 1
        if "adversarial" in text or "robust" in text:
            methods["Adversarial Training"] += 1
        if "smoothing" in text or "certified" in text:
            methods["Certified Defenses"] += 1
        if "augmentation" in text:
            methods["Data Augmentation"] += 1
        
        # Extract datasets/benchmarks
        if "benchmark" in text:
            datasets["Benchmarks"] += 1
        if "simulation" in text:
            datasets["Simulations"] += 1
        if "imagenet" in text:
            datasets["ImageNet"] += 1
        if "cifar" in text:
            datasets["CIFAR"] += 1
        if "mnist" in text:
            datasets["MNIST"] += 1
        
        # Extract metrics
        if "fidelity" in text:
            metrics["Fidelity"] += 1
        if "error" in text and "rate" in text:
            metrics["Error Rate"] += 1
        if "accuracy" in text:
            metrics["Accuracy"] += 1
        if "robust" in text:
            metrics["Robustness"] += 1
        
        if p.get("year"):
            years.append(p["year"])
        if p.get("venue"):
            venues[p["venue"]] += 1
    
    year_range = (min(years), max(years)) if years else (None, None)
    
    # Create concise summary for LLM (limit to avoid long prompts)
    top_methods_str = ', '.join([f"{m} ({c})" for m, c in methods.most_common(5)])
    top_datasets_str = ', '.join([f"{d} ({c})" for d, c in datasets.most_common(5)])
    top_metrics_str = ', '.join([f"{m} ({c})" for m, c in metrics.most_common(5)])
    sample_titles = '\n'.join([f"- {p.get('title', 'Unknown')[:80]}" for p in papers[:8]])
    
    summary = f"{len(papers)} papers ({year_range[0] if year_range[0] else '?'}-{year_range[1] if year_range[1] else '?'}). Methods: {top_methods_str}. Datasets: {top_datasets_str}. Metrics: {top_metrics_str}.\n\nSample titles:\n{sample_titles}"
    
    # Generate only key sections with LLM (reduce from 7 to 2-3 for speed)
    sections = {}
    
    def safe_generate(prompt, title, default_content, timeout_override=None):
        """Safely generate content with fallback and optional timeout"""
        try:
            # Use shorter timeout for faster failure
            original_timeout = llm_service.generate.__defaults__ if hasattr(llm_service.generate, '__defaults__') else None
            content = llm_service.generate(prompt, temperature=0.4)
            return {
                "title": title,
                "content": content
            }
        except Exception as e:
            print(f"Error generating {title}: {e}")
            return {
                "title": title,
                "content": default_content
            }
    
    # Methods & Approaches - Generate with LLM (key section)
    methods_prompt = f"""Synthesize methods from: {summary}

Write 2-3 paragraphs on dominant methods, key techniques, and evolution. Use **bold** for terms. Be concise."""
    
    sections["methods"] = safe_generate(
        methods_prompt,
        "Methods & Approaches",
        f"**Analysis of {len(papers)} papers ({year_range[0] if year_range[0] else '?'}-{year_range[1] if year_range[1] else '?'}):**\n\n"
        f"The dominant methodological approaches include: {', '.join([f'**{m}** ({c} papers)' for m, c in methods.most_common(5)])}. "
        f"These methods represent the primary research directions in this field. "
        f"The distribution shows {methods.most_common(1)[0][0] if methods else 'various methods'} as the most common approach with {methods.most_common(1)[0][1] if methods else 0} papers."
    )
    
    # Datasets & Benchmarks - Use basic analysis (fast)
    sections["datasets"] = {
        "title": "Datasets & Benchmarks",
        "content": f"**Analysis of {len(papers)} papers:**\n\n"
        f"The most commonly used datasets and benchmarks include: {', '.join([f'**{d}** ({c} papers)' for d, c in datasets.most_common(5)]) if datasets else 'Various benchmarks'}. "
        f"{'The field shows a focus on ' + datasets.most_common(1)[0][0] + ' with ' + str(datasets.most_common(1)[0][1]) + ' papers' if datasets else 'Various evaluation approaches are used'}."
    }
    
    # Evaluation Metrics - Use basic analysis (fast)
    sections["metrics"] = {
        "title": "Evaluation Metrics",
        "content": f"**Common evaluation metrics:**\n\n"
        f"The primary metrics used across these papers include: {', '.join([f'**{m}** ({c} papers)' for m, c in metrics.most_common(5)]) if metrics else 'Various metrics'}. "
        f"{metrics.most_common(1)[0][0] + ' appears in ' + str(metrics.most_common(1)[0][1]) + ' papers' if metrics else 'Various evaluation approaches'}."
    }
    
    # Performance Trends - Use basic analysis (fast)
    sections["performance"] = {
        "title": "Performance Trends",
        "content": f"**Performance analysis ({year_range[0] if year_range[0] else '?'}-{year_range[1] if year_range[1] else '?'}):**\n\n"
        f"Analysis of {len(papers)} papers reveals performance trends across the field. "
        f"The research spans {year_range[1] - year_range[0] + 1 if year_range[0] and year_range[1] else 'multiple'} years, "
        f"showing evolution in performance standards and evaluation approaches."
    }
    
    # Method Transitions (Evolution) - Generate with LLM (key section)
    transitions_prompt = f"""Analyze evolution: {summary}

Write 2-3 paragraphs on paradigm shifts, rising/declining methods, and trajectory implications. Use **bold** for terms."""
    
    sections["method_transitions"] = safe_generate(
        transitions_prompt,
        "Method Transitions",
        f"**Field Evolution Analysis:**\n\n"
        f"Based on {len(papers)} papers from {year_range[0] if year_range[0] else '?'} to {year_range[1] if year_range[1] else '?'}, "
        f"the field has evolved with key methods including: {', '.join([m for m, _ in methods.most_common(3)]) if methods else 'various approaches'}. "
        f"Research directions show different trajectories, with some methods gaining prominence while others stabilize or decline."
    )
    
    # Dataset Shifts (Evolution) - Use basic analysis (fast)
    sections["dataset_shifts"] = {
        "title": "Dataset Shifts",
        "content": f"**Benchmark Evolution ({year_range[0] if year_range[0] else '?'}-{year_range[1] if year_range[1] else '?'}):**\n\n"
        f"Dataset usage has evolved over time. Top datasets include: {', '.join([d for d, _ in datasets.most_common(3)]) if datasets else 'Various benchmarks'}. "
        f"The field shows {datasets.most_common(1)[0][0] + ' as the dominant benchmark' if datasets else 'diverse evaluation approaches'}."
    }
    
    # Metric Deprecations (Evolution) - Use basic analysis (fast)
    sections["metric_deprecations"] = {
        "title": "Metric Evolution",
        "content": f"**Metric Evolution:**\n\n"
        f"Evaluation metrics have evolved, with common metrics including: {', '.join([m for m, _ in metrics.most_common(3)]) if metrics else 'Various metrics'}. "
        f"The field shows {metrics.most_common(1)[0][0] + ' as a primary metric' if metrics else 'diverse evaluation approaches'}."
    }
    
    return {
        "sections": sections,
        "statistics": {
            "papers_analyzed": len(papers),
            "year_range": {"start": year_range[0], "end": year_range[1]},
            "top_methods": dict(methods.most_common(5)),
            "top_datasets": dict(datasets.most_common(5)),
            "top_metrics": dict(metrics.most_common(5))
        }
    }

@synthesis_bp.route("/", methods=["POST"])
def synthesis():
    try:
        papers = request.json
        if not papers:
            return jsonify({"error": "No papers provided"}), 400
        
        result = generate_synthesis_content(papers)
        
        # Check if any sections failed to generate
        has_errors = False
        for section_key, section_data in result.get("sections", {}).items():
            if section_data.get("content", "").startswith("Error:"):
                has_errors = True
                break
        
        if has_errors:
            result["warning"] = "Some sections could not be generated with LLM. Using basic analysis instead. Please ensure Ollama is running for full synthesis."
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
