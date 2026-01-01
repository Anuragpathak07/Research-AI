# api/code.py
from flask import Blueprint, jsonify, request
from services.llm_service import LLMService

code_bp = Blueprint("code", __name__)
llm_service = LLMService()

def generate_code_structure(experiments):
    """Generate code structure for experiments"""
    if not experiments:
        return None
    
    # Create basic structure
    structure = {
        "name": "research-experiments",
        "type": "folder",
        "children": [
            {
                "name": "README.md",
                "type": "file",
                "content": f"""# Research Experiments

This project contains code for {len(experiments)} proposed research experiments.

## Experiments
{chr(10).join([f"{i+1}. {exp.get('objective', exp.get('gap', 'Unknown'))}" for i, exp in enumerate(experiments[:5])])}

## Setup
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage
See individual experiment notebooks for details.
"""
            },
            {
                "name": "requirements.txt",
                "type": "file",
                "content": """torch>=2.0.0
torchvision>=0.15.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
jupyter>=1.0.0
tqdm>=4.65.0"""
            },
            {
                "name": "experiments",
                "type": "folder",
                "children": []
            }
        ]
    }
    
    # Add experiment files
    for i, exp in enumerate(experiments[:5]):  # Limit to 5 experiments
        exp_name = f"experiment_{i+1}"
        objective = exp.get("objective", exp.get("gap", f"Experiment {i+1}"))
        datasets = exp.get("datasets", exp.get("dataset", "TBD"))
        models = exp.get("models", ["TBD"])
        
        structure["children"][2]["children"].append({
            "name": f"{exp_name}.ipynb",
            "type": "file",
            "content": f"""{{
 "cells": [
  {{
   "cell_type": "markdown",
   "metadata": {{}},
   "source": [
    "# {objective}\\n",
    "\\n",
    "## Objective\\n",
    "{objective}\\n",
    "\\n",
    "## Datasets\\n",
    "{datasets if isinstance(datasets, str) else ', '.join(datasets)}\\n",
    "\\n",
    "## Models\\n",
    "{', '.join(models) if isinstance(models, list) else models}"
   ]
  }},
  {{
   "cell_type": "code",
   "execution_count": null,
   "metadata": {{}},
   "source": [
    "import torch\\n",
    "import torchvision\\n",
    "import numpy as np\\n",
    "\\n",
    "# TODO: Implement experiment based on objective\\n",
    "# {objective}"
   ]
  }}
 ]
}}"""
        })
    
    return structure

@code_bp.route("/", methods=["POST"])
def code():
    try:
        experiments = request.json or []
        if not experiments:
            return jsonify({"error": "No experiments provided"}), 400
        
        structure = generate_code_structure(experiments)
        if not structure:
            return jsonify({"error": "Failed to generate code structure"}), 500
        
        return jsonify(structure)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

