# agents/extraction_agent.py
import re
from collections import defaultdict
from agents.base_agent import BaseAgent
import json

class ExtractionAgent(BaseAgent):
    """Agentic extraction agent with LLM reasoning for entity extraction"""
    
    METHOD_KEYWORDS = ["transformer", "cnn", "rnn", "gan", "diffusion", "svm", "quantum", "circuit", "algorithm"]
    DATASET_KEYWORDS = ["imagenet", "cifar", "mnist", "coco", "cityscapes", "benchmark", "simulation"]
    METRIC_KEYWORDS = ["accuracy", "f1", "precision", "recall", "mAP", "robustness", "fidelity", "error rate"]
    
    def __init__(self):
        tools = [
            {
                'name': 'extract_keywords',
                'description': 'Extract keywords from text using pattern matching. Input: {"text": "...", "type": "methods|datasets|metrics"}',
                'func': self._extract_keywords_tool
            },
            {
                'name': 'analyze_paper_content',
                'description': 'Analyze paper abstract and title for research entities. Input: {"title": "...", "abstract": "..."}',
                'func': self._analyze_paper_tool
            }
        ]
        super().__init__(
            name="Extraction Agent",
            description="An AI agent that intelligently extracts research entities (methods, datasets, metrics) from papers using both pattern matching and semantic understanding",
            tools=tools
        )
    
    def _extract_keywords_tool(self, input_data):
        """Tool function for keyword extraction"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        text = input_data.get('text', '').lower()
        entity_type = input_data.get('type', 'methods')
        
        if entity_type == 'methods':
            keywords = self.METHOD_KEYWORDS
        elif entity_type == 'datasets':
            keywords = self.DATASET_KEYWORDS
        else:
            keywords = self.METRIC_KEYWORDS
        
        found = [kw for kw in keywords if kw in text]
        return json.dumps(found)
    
    def _analyze_paper_tool(self, input_data):
        """Tool function for analyzing paper content"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        title = input_data.get('title', '')
        abstract = input_data.get('abstract', '')
        
        # Use LLM to extract entities
        prompt = f"""Extract research entities from this paper:

Title: {title}
Abstract: {abstract[:500]}

Extract:
1. Methods/Techniques used
2. Datasets/Benchmarks mentioned
3. Evaluation Metrics used

Return as JSON: {{"methods": [...], "datasets": [...], "metrics": [...]}}"""
        
        try:
            response = self.llm_service.generate(prompt, temperature=0.2)
            # Try to extract JSON from response
            json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
            if json_match:
                return json_match.group(0)
            return response
        except:
            return json.dumps({"methods": [], "datasets": [], "metrics": []})
    
    def extract_entities(self, papers):
        """
        Extract entities with LLM reasoning for better accuracy
        """
        extracted = []
        
        # Use LLM to reason about extraction strategy
        strategy_prompt = f"""I need to extract research entities from {len(papers)} papers.

I should extract:
- Methods/Techniques (e.g., transformers, CNNs, quantum circuits)
- Datasets/Benchmarks (e.g., ImageNet, CIFAR, simulations)
- Evaluation Metrics (e.g., accuracy, F1, robustness)

Should I:
1. Use keyword matching for speed
2. Use LLM analysis for accuracy
3. Use a hybrid approach (keywords + LLM validation)

Provide reasoning."""
        
        strategy_result = self.simple_reason(strategy_prompt)
        strategy = strategy_result.get('result') or strategy_result.get('reasoning') or ''
        
        # Process papers
        for i, p in enumerate(papers):
            text = (p.get("abstract", "") + " " + p.get("title", "")).lower()
            
            # Keyword-based extraction (fast)
            methods = [m for m in self.METHOD_KEYWORDS if m in text]
            datasets = [d for d in self.DATASET_KEYWORDS if d in text]
            metrics = [m for m in self.METRIC_KEYWORDS if m in text]
            
            # Use LLM for papers where keyword extraction might miss important entities
            # (sample every 5th paper or if no keywords found)
            if i % 5 == 0 or (not methods and not datasets and not metrics):
                try:
                    llm_result = self._analyze_paper_tool({
                        'title': p.get('title', ''),
                        'abstract': p.get('abstract', '')
                    })
                    
                    # Try to parse LLM result
                    try:
                        llm_entities = json.loads(llm_result)
                        methods.extend(llm_entities.get('methods', []))
                        datasets.extend(llm_entities.get('datasets', []))
                        metrics.extend(llm_entities.get('metrics', []))
                    except:
                        pass
                except:
                    pass
            
            extracted.append({
                **p,
                "methods": list(set(methods)),
                "datasets": list(set(datasets)),
                "metrics": list(set(metrics))
            })
        
        return extracted
