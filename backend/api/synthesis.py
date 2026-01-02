# api/synthesis.py
from flask import Blueprint, jsonify, request
from collections import Counter, defaultdict
from services.llm_service import LLMService
from services.data_cache import DataCache
import json

synthesis_bp = Blueprint("synthesis", __name__)
llm_service = LLMService()
data_cache = DataCache()

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
    
    # Create detailed summary for LLM with actual paper content
    top_methods_str = ', '.join([f"{m} ({c} papers)" for m, c in methods.most_common(5)])
    top_datasets_str = ', '.join([f"{d} ({c} papers)" for d, c in datasets.most_common(5)])
    top_metrics_str = ', '.join([f"{m} ({c} papers)" for m, c in metrics.most_common(5)])
    
    # Include more paper details for better context
    paper_details = []
    for i, p in enumerate(papers[:15], 1):  # Include more papers
        title = p.get('title', 'Unknown')
        abstract = p.get('abstract', '')[:200]  # First 200 chars of abstract
        year = p.get('year', '?')
        paper_details.append(f"{i}. {title} ({year})\n   {abstract}...")
    
    papers_text = '\n\n'.join(paper_details)
    
    summary = f"""Research Literature Analysis:
- Total Papers: {len(papers)}
- Year Range: {year_range[0] if year_range[0] else '?'} to {year_range[1] if year_range[1] else '?'}
- Dominant Methods: {top_methods_str if top_methods_str else 'Various approaches'}
- Common Datasets: {top_datasets_str if top_datasets_str else 'Various benchmarks'}
- Evaluation Metrics: {top_metrics_str if top_metrics_str else 'Various metrics'}

Key Papers:
{papers_text}"""
    
    # Generate only key sections with LLM (reduce from 7 to 2-3 for speed)
    sections = {}
    
    def safe_generate(prompt, title, default_content, timeout_override=None):
        """Safely generate content with fallback and optional timeout"""
        try:
            print(f"Generating {title} with LLM...")
            # Use higher temperature for more creative/detailed content
            content = llm_service.generate(prompt, temperature=0.6)
            if content and len(content.strip()) > 100:  # Require at least 100 chars
                # Clean up the content
                content = content.strip()
                # Ensure it has proper formatting
                if not content.startswith("**"):
                    # Add bold formatting if missing
                    lines = content.split('\n')
                    if lines[0] and not lines[0].startswith('**'):
                        lines[0] = f"**{lines[0]}**"
                    content = '\n'.join(lines)
                
                print(f"Successfully generated {title} ({len(content)} chars)")
                return {
                    "title": title,
                    "content": content
                }
            else:
                print(f"LLM returned short/empty content for {title} (length: {len(content) if content else 0}), using fallback")
                return {
                    "title": title,
                    "content": default_content
                }
        except Exception as e:
            print(f"Error generating {title} with LLM: {e}")
            import traceback
            traceback.print_exc()
            # Return fallback but mark it
            return {
                "title": title,
                "content": default_content
            }
    
    # Methods & Approaches - Generate with LLM (key section)
    methods_prompt = f"""You are a research synthesis expert. Analyze the following research papers and write a comprehensive synthesis of the methods and approaches used.

{summary}

Write a detailed 3-4 paragraph analysis covering:
1. The dominant methodological approaches and why they are important
2. Key techniques and innovations mentioned in the papers
3. How methods have evolved over the time period
4. Connections between different approaches

Use **bold** for important terms and method names. Be specific and reference the actual research themes from the papers. Write in academic style."""
    
    sections["methods"] = safe_generate(
        methods_prompt,
        "Methods & Approaches",
        f"**Analysis of {len(papers)} papers ({year_range[0] if year_range[0] else '?'}-{year_range[1] if year_range[1] else '?'}):**\n\n"
        f"The dominant methodological approaches include: {', '.join([f'**{m}** ({c} papers)' for m, c in methods.most_common(5)])}. "
        f"These methods represent the primary research directions in this field. "
        f"The distribution shows {methods.most_common(1)[0][0] if methods else 'various methods'} as the most common approach with {methods.most_common(1)[0][1] if methods else 0} papers."
    )
    
    # Datasets & Benchmarks - Generate with LLM
    datasets_prompt = f"""Analyze the datasets and benchmarks used in these research papers:

{summary}

Write 2-3 paragraphs on:
1. The most commonly used datasets and benchmarks
2. Why certain datasets are preferred
3. How dataset choices reflect research priorities
4. Trends in dataset usage over time

Use **bold** for dataset names. Be specific about the evaluation approaches."""
    
    sections["datasets"] = safe_generate(
        datasets_prompt,
        "Datasets & Benchmarks",
        f"**Analysis of {len(papers)} papers:**\n\n"
        f"The most commonly used datasets and benchmarks include: {', '.join([f'**{d}** ({c} papers)' for d, c in datasets.most_common(5)]) if datasets else 'Various benchmarks'}. "
        f"{'The field shows a focus on ' + datasets.most_common(1)[0][0] + ' with ' + str(datasets.most_common(1)[0][1]) + ' papers' if datasets else 'Various evaluation approaches are used'}."
    )
    
    # Evaluation Metrics - Generate with LLM
    metrics_prompt = f"""Analyze the evaluation metrics used in these research papers:

{summary}

Write 2-3 paragraphs on:
1. The primary evaluation metrics and their significance
2. Why certain metrics are preferred in this field
3. How metric choices reflect research goals
4. Trends in metric usage and what they indicate about the field

Use **bold** for metric names. Explain the importance of these metrics."""
    
    sections["metrics"] = safe_generate(
        metrics_prompt,
        "Evaluation Metrics",
        f"**Common evaluation metrics:**\n\n"
        f"The primary metrics used across these papers include: {', '.join([f'**{m}** ({c} papers)' for m, c in metrics.most_common(5)]) if metrics else 'Various metrics'}. "
        f"{metrics.most_common(1)[0][0] + ' appears in ' + str(metrics.most_common(1)[0][1]) + ' papers' if metrics else 'Various evaluation approaches'}."
    )
    
    # Performance Trends - Generate with LLM
    performance_prompt = f"""Analyze performance trends and research progress in these papers:

{summary}

Write 2-3 paragraphs on:
1. Overall performance trends and improvements over time
2. Key breakthroughs or significant advances
3. How research priorities have shifted
4. What the performance trends indicate about the field's maturity

Use **bold** for important concepts. Be analytical about the research trajectory."""
    
    sections["performance"] = safe_generate(
        performance_prompt,
        "Performance Trends",
        f"**Performance analysis ({year_range[0] if year_range[0] else '?'}-{year_range[1] if year_range[1] else '?'}):**\n\n"
        f"Analysis of {len(papers)} papers reveals performance trends across the field. "
        f"The research spans {year_range[1] - year_range[0] + 1 if year_range[0] and year_range[1] else 'multiple'} years, "
        f"showing evolution in performance standards and evaluation approaches."
    )
    
    # Method Transitions (Evolution) - Generate with LLM (key section)
    transitions_prompt = f"""Analyze the evolution and paradigm shifts in this research field:

{summary}

Write a detailed 3-4 paragraph analysis covering:
1. Major paradigm shifts and methodological transitions
2. Which methods are rising, which are declining, and why
3. The trajectory implications for future research
4. Key turning points or innovations that changed the field

Use **bold** for important concepts. Be insightful about the field's evolution."""
    
    sections["method_transitions"] = safe_generate(
        transitions_prompt,
        "Method Transitions",
        f"**Field Evolution Analysis:**\n\n"
        f"Based on {len(papers)} papers from {year_range[0] if year_range[0] else '?'} to {year_range[1] if year_range[1] else '?'}, "
        f"the field has evolved with key methods including: {', '.join([m for m, _ in methods.most_common(3)]) if methods else 'various approaches'}. "
        f"Research directions show different trajectories, with some methods gaining prominence while others stabilize or decline."
    )
    
    # Dataset Shifts (Evolution) - Generate with LLM
    dataset_shifts_prompt = f"""Analyze how dataset and benchmark usage has evolved:

{summary}

Write 2-3 paragraphs on:
1. How dataset choices have shifted over time
2. What drives changes in benchmark preferences
3. Emerging datasets and what they indicate
4. The implications of dataset evolution for the field

Use **bold** for dataset names. Explain the significance of these shifts."""
    
    sections["dataset_shifts"] = safe_generate(
        dataset_shifts_prompt,
        "Dataset Shifts",
        f"**Benchmark Evolution ({year_range[0] if year_range[0] else '?'}-{year_range[1] if year_range[1] else '?'}):**\n\n"
        f"Dataset usage has evolved over time. Top datasets include: {', '.join([d for d, _ in datasets.most_common(3)]) if datasets else 'Various benchmarks'}. "
        f"The field shows {datasets.most_common(1)[0][0] + ' as the dominant benchmark' if datasets else 'diverse evaluation approaches'}."
    )
    
    # Metric Deprecations (Evolution) - Generate with LLM
    metric_evolution_prompt = f"""Analyze how evaluation metrics have evolved:

{summary}

Write 2-3 paragraphs on:
1. How evaluation metrics have changed over time
2. Which metrics have gained or lost prominence and why
3. What metric evolution reveals about research priorities
4. Emerging evaluation approaches

Use **bold** for metric names. Explain the significance of these changes."""
    
    sections["metric_deprecations"] = safe_generate(
        metric_evolution_prompt,
        "Metric Evolution",
        f"**Metric Evolution:**\n\n"
        f"Evaluation metrics have evolved, with common metrics including: {', '.join([m for m, _ in metrics.most_common(3)]) if metrics else 'Various metrics'}. "
        f"The field shows {metrics.most_common(1)[0][0] + ' as a primary metric' if metrics else 'diverse evaluation approaches'}."
    )
    
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
        data = request.json
        if isinstance(data, list):
            # Backward compatibility: if data is a list, treat as papers
            papers = data
            force_regenerate = False
        else:
            # New format: data is a dict with papers and optional force_regenerate
            papers = data.get("papers", [])
            force_regenerate = data.get("force_regenerate", False)
        
        if not papers:
            return jsonify({"error": "No papers provided"}), 400
        
        # Check cache first (unless force_regenerate is True)
        if not force_regenerate:
            cached_data = data_cache.get_synthesis(papers)
            if cached_data and cached_data.get("synthesis"):
                print("Returning cached synthesis")
                return jsonify(cached_data["synthesis"])
        
        # Generate fresh synthesis
        print("Generating fresh synthesis content...")
        result = generate_synthesis_content(papers)
        
        # Check if LLM was actually used (not just fallback content)
        llm_used = False
        for section_key, section_data in result.get("sections", {}).items():
            content = section_data.get("content", "")
            # Check if content looks like LLM-generated (longer, more detailed)
            if len(content) > 200 and ("**" in content or "\n\n" in content):
                llm_used = True
                break
        
        if not llm_used:
            result["warning"] = "LLM generation failed or returned insufficient content. Using basic analysis. Please ensure Ollama is running and the model is available for full synthesis."
            print("Warning: Synthesis generated without LLM - using fallback content")
        
        # Auto-store in cache
        data_cache.save_synthesis(papers, result)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
