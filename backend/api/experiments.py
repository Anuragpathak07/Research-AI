# api/experiments.py
from flask import Blueprint, jsonify, request

experiments_bp = Blueprint("experiments", __name__)

@experiments_bp.route("/", methods=["POST"])
def experiments():
    gaps = request.json or []
    experiments = []

    for g in gaps:
        experiments.append({
            "objective": g.get("gap", "Unknown gap"),
            "datasets": ["ImageNet", "CIFAR-10"],
            "models": ["ResNet", "ViT"],
            "metrics": ["Accuracy", "Robustness"],
            "code_stub": "train.py / evaluate.py"
        })

    return jsonify(experiments)
