# models/experiment.py
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Experiment:
    objective: str
    datasets: List[str]
    models: List[str]
    metrics: List[str]
    expected_outcome: str
    code_structure: Dict[str, str] = field(default_factory=dict)
