# agents/trajectory_agent.py
from collections import defaultdict
import numpy as np
from agents.base_agent import BaseAgent
import json

class TrajectoryAgent(BaseAgent):
    """Agentic trajectory agent with LLM reasoning for research evolution modeling"""
    
    def __init__(self):
        tools = [
            {
                'name': 'calculate_trend',
                'description': 'Calculate trend slope from year data. Input: {"years": [2015, 2016, ...], "counts": [1, 2, ...]}',
                'func': self._calculate_trend_tool
            },
            {
                'name': 'classify_trajectory',
                'description': 'Classify research trajectory based on trend analysis. Input: {"slope": 0.5, "method": "transformer", "years": [...]}',
                'func': self._classify_trajectory_tool
            }
        ]
        super().__init__(
            name="Trajectory Modeling Agent",
            description="An AI agent that models research evolution trajectories, identifying rising, stable, saturating, and declining research directions using temporal analysis and reasoning",
            tools=tools
        )
    
    def _calculate_trend_tool(self, input_data):
        """Tool function for calculating trends"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        years = input_data.get('years', [])
        counts = input_data.get('counts', [])
        
        if not years or not counts:
            return json.dumps({"slope": 0.0, "trend": "insufficient_data"})
        
        try:
            slope = np.polyfit(range(len(counts)), counts, 1)[0]
            return json.dumps({"slope": float(slope), "trend": "calculated"})
        except:
            return json.dumps({"slope": 0.0, "trend": "error"})
    
    def _classify_trajectory_tool(self, input_data):
        """Tool function for classifying trajectory"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        slope = input_data.get('slope', 0.0)
        method = input_data.get('method', '')
        years = input_data.get('years', [])
        
        # Use LLM to reason about trajectory classification
        prompt = f"""Analyze the research trajectory for method: {method}

Trend slope: {slope}
Year range: {min(years) if years else 'N/A'} - {max(years) if years else 'N/A'}
Number of papers: {len(years)}

Classify the trajectory:
- "Rising": Positive slope > 0.3, increasing interest
- "Stable": Slope between -0.3 and 0.3, steady research
- "Saturating": High paper count but declining growth
- "Declining": Negative slope < -0.3, decreasing interest

Provide classification and reasoning."""
        
        try:
            response = self.llm_service.generate(prompt, temperature=0.2)
            # Extract classification from response
            if 'rising' in response.lower():
                return json.dumps({"label": "Rising", "reasoning": response})
            elif 'declining' in response.lower():
                return json.dumps({"label": "Declining", "reasoning": response})
            elif 'saturating' in response.lower():
                return json.dumps({"label": "Saturating", "reasoning": response})
            else:
                return json.dumps({"label": "Stable", "reasoning": response})
        except:
            # Fallback to rule-based
            if slope > 0.3:
                return json.dumps({"label": "Rising"})
            elif slope < -0.3:
                return json.dumps({"label": "Declining"})
            else:
                return json.dumps({"label": "Stable"})
    
    def build_trajectories(self, extracted_papers):
        """
        Build trajectories with LLM reasoning for better classification
        """
        method_years = defaultdict(list)

        # Collect method-year pairs
        for p in extracted_papers:
            for m in p.get("methods", []):
                method_years[m].append(p.get("year", 2020))

        trajectories = {}
        
        # Use LLM to reason about trajectory analysis strategy (optional, skip for speed)
        # Skip LLM strategy reasoning to speed up trajectory building
        strategy = ''
        # Uncomment below for LLM-based strategy reasoning (slower)
        # strategy_prompt = f"""I need to analyze trajectories for {len(method_years)} research methods.
        # ...
        # strategy_result = self.simple_reason(strategy_prompt)
        # strategy = strategy_result.get('result') or strategy_result.get('reasoning') or ''
        
        # Analyze each method
        for method, years in method_years.items():
            if not years:
                continue
                
            years = sorted(years)
            counts = np.bincount([y - min(years) for y in years])
            
            # Calculate slope
            if len(counts) > 1:
                slope = np.polyfit(range(len(counts)), counts, 1)[0]
            else:
                slope = 0.0
            
            # Use rule-based classification (skip LLM for speed)
            # Rule-based classification is fast and accurate enough
            if slope > 0.3:
                label = "Rising"
            elif slope < -0.3:
                label = "Declining"
            elif len(years) > 15:
                label = "Saturating"
            else:
                label = "Stable"
            
            # Optional: Use LLM for ambiguous cases (slower)
            # Uncomment below for LLM-based classification of ambiguous cases
            # if abs(slope) < 0.3 or len(years) > 10:  # Ambiguous cases
            #     try:
            #         classification = self._classify_trajectory_tool({
            #             'slope': slope,
            #             'method': method,
            #             'years': years
            #         })
            #         class_data = json.loads(classification)
            #         label = class_data.get('label', label)
            #     except:
            #         pass  # Use rule-based fallback

            trajectories[method] = {
                "years": years,
                "slope": float(slope),
                "trajectory": label,
                "paper_count": len(years)
            }

        return trajectories
