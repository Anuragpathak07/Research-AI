# agents/experiment_agent.py
from agents.base_agent import BaseAgent
import json
import re

class ExperimentAgent(BaseAgent):
    """Agentic experiment proposal agent with LLM reasoning for future-aligned experiment design"""
    
    def __init__(self):
        tools = [
            {
                'name': 'design_experiment',
                'description': 'Design an experiment for a research gap. Input: {"gap": "...", "context": "..."}',
                'func': self._design_experiment_tool
            },
            {
                'name': 'select_datasets',
                'description': 'Select appropriate datasets for an experiment. Input: {"objective": "...", "field": "..."}',
                'func': self._select_datasets_tool
            },
            {
                'name': 'generate_code_structure',
                'description': 'Generate code structure for an experiment. Input: {"experiment": {...}}',
                'func': self._generate_code_structure_tool
            }
        ]
        super().__init__(
            name="Experiment Proposal Agent",
            description="An AI agent that proposes future-aligned experiments based on research gaps, selecting appropriate datasets, models, and metrics with temporal relevance",
            tools=tools
        )
    
    def _design_experiment_tool(self, input_data):
        """Tool function for designing experiments"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        gap = input_data.get('gap', {})
        context = input_data.get('context', '')
        
        prompt = f"""Design a research experiment to address this gap:

Gap: {json.dumps(gap, indent=2)}
Context: {context}

Design an experiment that:
1. Has a clear objective aligned with the gap
2. Uses appropriate datasets and models
3. Includes relevant evaluation metrics
4. Is future-proof and temporally relevant

Return as JSON with: objective, datasets (array), models (array), metrics (array), expected_outcome"""
        
        try:
            response = self.llm_service.generate(prompt, temperature=0.4)
            # Try to extract JSON
            json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
            if json_match:
                return json_match.group(0)
            return response
        except Exception as e:
            return json.dumps({
                "objective": gap.get('title', 'Unknown'),
                "datasets": ["CIFAR-10", "ImageNet"],
                "models": ["ResNet", "Vision Transformer"],
                "metrics": ["Accuracy", "Robustness"],
                "expected_outcome": "Validate research hypothesis"
            })
    
    def _select_datasets_tool(self, input_data):
        """Tool function for selecting datasets"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        objective = input_data.get('objective', '')
        field = input_data.get('field', '')
        
        prompt = f"""Select appropriate datasets for this experiment:

Objective: {objective}
Field: {field}

Consider:
- Dataset relevance to the objective
- Dataset popularity and availability
- Dataset size and complexity
- Temporal relevance (recent vs. established datasets)

Return as JSON array of dataset names."""
        
        try:
            response = self.llm_service.generate(prompt, temperature=0.3)
            json_match = re.search(r'\[[^\]]+\]', response)
            if json_match:
                return json_match.group(0)
            return '["CIFAR-10", "ImageNet"]'
        except:
            return '["CIFAR-10", "ImageNet"]'
    
    def _generate_code_structure_tool(self, input_data):
        """Tool function for generating code structure"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        experiment = input_data.get('experiment', {})
        
        prompt = f"""Generate a code structure for this experiment:

{json.dumps(experiment, indent=2)}

Create a file structure with:
- train.py: Model training loop
- evaluate.py: Evaluation metrics
- config.yaml: Hyperparameters
- README.md: Experiment description

Return as JSON with file names as keys and descriptions as values."""
        
        try:
            response = self.llm_service.generate(prompt, temperature=0.3)
            json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
            if json_match:
                return json_match.group(0)
            return json.dumps({
                "train.py": "model training loop",
                "evaluate.py": "evaluation metrics",
                "config.yaml": "hyperparameters"
            })
        except:
            return json.dumps({
                "train.py": "model training loop",
                "evaluate.py": "evaluation metrics",
                "config.yaml": "hyperparameters"
            })
    
    def propose_experiments(self, gaps):
        """
        Propose experiments with LLM reasoning for better design
        """
        experiments = []
        
        # Filter for future-viable gaps
        viable_gaps = [g for g in gaps if g.get("temporalViability") == "future-viable"]
        
        if not viable_gaps:
            return experiments
        
        # Use LLM to reason about experiment strategy
        strategy_prompt = f"""I need to propose experiments for {len(viable_gaps)} research gaps.

Each experiment should:
1. Address a specific gap
2. Use appropriate datasets and models
3. Include relevant metrics
4. Be future-proof and temporally relevant

What approach should I take for experiment design?"""
        
        strategy_result = self.simple_reason(strategy_prompt)
        strategy = strategy_result.get('result') or strategy_result.get('reasoning') or ''
        
        # Design experiments for each gap
        for gap in viable_gaps:
            try:
                # Design experiment using LLM
                experiment_design = self._design_experiment_tool({
                    'gap': gap,
                    'context': f"Viability: {gap.get('temporalViability')}, Evidence: {gap.get('evidence', '')}"
                })
                
                # Parse experiment design
                try:
                    design = json.loads(experiment_design)
                except:
                    # Fallback
                    design = {
                        "objective": gap.get("title", "Unknown"),
                        "datasets": ["CIFAR-10", "ImageNet"],
                        "models": ["ResNet", "Vision Transformer"],
                        "metrics": ["Accuracy", "Robustness"],
                        "expected_outcome": "Validate research hypothesis"
                    }
                
                # Generate code structure
                code_structure = self._generate_code_structure_tool({
                    'experiment': design
                })
                
                try:
                    code_struct = json.loads(code_structure)
                except:
                    code_struct = {
                        "train.py": "model training loop",
                        "evaluate.py": "evaluation metrics",
                        "config.yaml": "hyperparameters"
                    }
                
                experiments.append({
                    "id": f"exp_{len(experiments)}",
                    "objective": design.get("objective", gap.get("title", "Unknown")),
                    "dataset": ", ".join(design.get("datasets", [])),
                    "models": design.get("models", ["ResNet", "Vision Transformer"]),
                    "metrics": design.get("metrics", ["Accuracy", "Robustness"]),
                    "outcome": design.get("expected_outcome", "Validate scalability and generalization"),
                    "recommended": True,
                    "temporalRelevance": f"Addresses {gap.get('temporalViability')} gap: {gap.get('title', '')}",
                    "futureProofDesign": "Designed with temporal relevance and future-proof assumptions",
                    "code_structure": code_struct
                })
            except Exception as e:
                # Fallback experiment
                experiments.append({
                    "id": f"exp_{len(experiments)}",
                    "objective": gap.get("title", "Unknown"),
                    "dataset": "CIFAR-10, ImageNet",
                    "models": ["ResNet", "Vision Transformer"],
                    "metrics": ["Accuracy", "Robustness"],
                    "outcome": "Validate scalability and generalization",
                    "recommended": True,
                    "temporalRelevance": f"Addresses {gap.get('temporalViability')} gap",
                    "futureProofDesign": "Standard experiment design",
                    "code_structure": {
                        "train.py": "model training loop",
                        "evaluate.py": "evaluation metrics",
                        "config.yaml": "hyperparameters"
                    }
                })

        return experiments
