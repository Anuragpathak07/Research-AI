# agents/extraction_agent.py
import re
from collections import defaultdict

class ExtractionAgent:
    METHOD_KEYWORDS = ["transformer", "cnn", "rnn", "gan", "diffusion", "svm"]
    DATASET_KEYWORDS = ["imagenet", "cifar", "mnist", "coco", "cityscapes"]
    METRIC_KEYWORDS = ["accuracy", "f1", "precision", "recall", "mAP", "robustness"]

    def extract_entities(self, papers):
        extracted = []

        for p in papers:
            text = p["abstract"].lower()

            methods = [m for m in self.METHOD_KEYWORDS if m in text]
            datasets = [d for d in self.DATASET_KEYWORDS if d in text]
            metrics = [m for m in self.METRIC_KEYWORDS if m in text]

            extracted.append({
                **p,
                "methods": list(set(methods)),
                "datasets": list(set(datasets)),
                "metrics": list(set(metrics))
            })

        return extracted
