# agents/experiment_agent.py
class ExperimentAgent:
    def propose_experiments(self, gaps):
        experiments = []

        for g in gaps:
            if g["viability"] != "Future-Viable":
                continue

            experiments.append({
                "objective": g["gap_title"],
                "datasets": ["CIFAR-10", "ImageNet"],
                "models": ["ResNet", "Vision Transformer"],
                "metrics": ["Accuracy", "Robustness"],
                "expected_outcome": "Validate scalability and generalization",
                "code_structure": {
                    "train.py": "model training loop",
                    "evaluate.py": "evaluation metrics",
                    "config.yaml": "hyperparameters"
                }
            })

        return experiments
