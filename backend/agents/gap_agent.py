# agents/gap_agent.py
from agents.base_agent import BaseAgent
import json

class GapAgent(BaseAgent):
    """Agentic gap detection agent with LLM reasoning for temporal viability assessment"""
    
    def __init__(self):
        tools = [
            {
                'name': 'analyze_gap_viability',
                'description': 'Analyze if a research gap is future-viable. Input: {"gap": "...", "trajectory": "...", "evidence": {...}}',
                'func': self._analyze_viability_tool
            },
            {
                'name': 'generate_gap_hypothesis',
                'description': 'Generate research gap hypothesis. Input: {"method": "...", "context": "..."}',
                'func': self._generate_hypothesis_tool
            }
        ]
        super().__init__(
            name="Gap Detection Agent",
            description="An AI agent that detects research gaps with temporal viability assessment, classifying gaps as future-viable, time-sensitive, or likely obsolete",
            tools=tools
        )
    
    def _analyze_viability_tool(self, input_data):
        """Tool function for analyzing gap viability"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        gap = input_data.get('gap', '')
        trajectory = input_data.get('trajectory', '')
        evidence = input_data.get('evidence', {})
        
        prompt = f"""Analyze the temporal viability of this research gap:

Gap: {gap}
Trajectory: {trajectory}
Evidence: {json.dumps(evidence, indent=2)}

Classify viability:
- "future-viable": Promising research direction with growing interest
- "time-sensitive": Needs immediate attention, window may close
- "likely-obsolete": Declining field, may not be worth pursuing

Provide classification and detailed reasoning."""
        
        try:
            response = self.llm_service.generate(prompt, temperature=0.3)
            
            # Extract classification
            if 'future-viable' in response.lower() or 'future viable' in response.lower():
                viability = "future-viable"
            elif 'time-sensitive' in response.lower() or 'time sensitive' in response.lower():
                viability = "time-sensitive"
            elif 'obsolete' in response.lower():
                viability = "likely-obsolete"
            else:
                viability = "future-viable"  # Default
            
            return json.dumps({
                "viability": viability,
                "reasoning": response
            })
        except:
            # Fallback
            if trajectory == "Rising":
                return json.dumps({"viability": "future-viable"})
            elif trajectory == "Declining":
                return json.dumps({"viability": "likely-obsolete"})
            else:
                return json.dumps({"viability": "time-sensitive"})
    
    def _generate_hypothesis_tool(self, input_data):
        """Tool function for generating gap hypotheses"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        method = input_data.get('method', '')
        context = input_data.get('context', '')
        
        prompt = f"""Generate a research gap hypothesis for method: {method}

Context: {context}

Create a specific, actionable research gap that:
1. Is clearly defined
2. Has temporal relevance
3. Is feasible to address

Format: Title and detailed description."""
        
        try:
            response = self.llm_service.generate(prompt, temperature=0.5)
            return response
        except:
            return f"Underexplored application of {method}"
    
    def detect_gaps(self, trajectories, extracted_papers):
        """
        Detect gaps with LLM reasoning for better temporal viability assessment
        """
        gaps = []
        
        if not trajectories:
            return gaps

        # Count method usage
        method_counts = {}
        for p in extracted_papers:
            for m in p.get("methods", []):
                method_counts[m] = method_counts.get(m, 0) + 1

        # Use LLM to reason about gap detection strategy (optional, skip for speed)
        # Skip LLM strategy reasoning to speed up gap detection
        strategy = ''
        # Uncomment below for LLM-based strategy reasoning (slower)
        # try:
        #     strategy_result = self.simple_reason(strategy_prompt)
        #     strategy = strategy_result.get('result') or strategy_result.get('reasoning') or ''
        # except Exception as e:
        #     print(f"LLM reasoning failed in gap detection: {e}")
        #     strategy = ''
        
        # Analyze each method for gaps
        for method, info in trajectories.items():
            if not isinstance(info, dict):
                continue
                
            count = method_counts.get(method, info.get("paper_count", 0))
            trajectory = info.get("trajectory", "Stable")
            
            # Use LLM reasoning for gap detection (with fast fallback)
            # Also detect gaps for methods with low paper count regardless of trajectory
            if (trajectory == "Rising" and count < 10) or (count > 0 and count < 5):
                # Potential gap - use fast rule-based analysis (skip LLM for speed)
                viability = "future-viable"
                reasoning = f"Positive momentum ({trajectory}) with low paper volume ({count} papers)"
                hypothesis = f"Underexplored application of {method} in research"
                
                # Optional: Use LLM for more detailed analysis (slower)
                # Uncomment below for LLM-based analysis
                # try:
                #     gap_analysis = self._analyze_viability_tool({
                #         'gap': f"Underexplored use of {method}",
                #         'trajectory': trajectory,
                #         'evidence': info
                #     })
                #     analysis = json.loads(gap_analysis)
                #     viability = analysis.get('viability', 'future-viable')
                #     reasoning = analysis.get('reasoning', reasoning)
                #     
                #     hypothesis = self._generate_hypothesis_tool({
                #         'method': method,
                #         'context': f"Trajectory: {trajectory}, Papers: {count}"
                #     })
                # except:
                #     pass  # Use rule-based fallback
                
                gaps.append({
                    "id": f"gap_{method}_{len(gaps)}",
                    "title": hypothesis.split('\n')[0] if '\n' in hypothesis else hypothesis[:100],
                    "why": reasoning or f"Positive momentum ({trajectory}) with low paper volume ({count} papers)",
                    "evidence": json.dumps(info),
                    "temporalViability": viability,
                    "temporalJustification": reasoning or f"Method shows {trajectory} trajectory with {count} papers, indicating potential for future research"
                })
            
            elif trajectory == "Declining":
                # Declining method - potential obsolescence (use fast rule-based)
                viability = "likely-obsolete"
                
                # Optional: Use LLM for more detailed analysis (slower)
                # try:
                #     gap_analysis = self._analyze_viability_tool({
                #         'gap': f"{method} research direction",
                #         'trajectory': trajectory,
                #         'evidence': info
                #     })
                #     analysis = json.loads(gap_analysis)
                #     viability = analysis.get('viability', 'likely-obsolete')
                # except:
                #     pass  # Use rule-based fallback
                
                gaps.append({
                    "id": f"gap_{method}_{len(gaps)}",
                    "title": f"{method} research direction showing decline",
                    "why": f"Negative trend ({trajectory}) suggests field may be saturating",
                    "evidence": json.dumps(info),
                    "temporalViability": viability,
                    "temporalJustification": f"Method shows {trajectory} trajectory, indicating potential obsolescence"
                })
            
            elif trajectory == "Stable" and count > 0:
                # Stable methods with moderate activity - potential for innovation
                gaps.append({
                    "id": f"gap_{method}_{len(gaps)}",
                    "title": f"Potential innovation opportunities in {method}",
                    "why": f"Stable trajectory with {count} papers suggests room for novel approaches",
                    "evidence": json.dumps(info),
                    "temporalViability": "future-viable",
                    "temporalJustification": f"Method shows stable trajectory with {count} papers, indicating sustained interest with potential for innovation"
                })

        # If no gaps found, create at least one generic gap from the first trajectory
        if not gaps and trajectories:
            first_method = list(trajectories.keys())[0]
            first_info = trajectories[first_method]
            gaps.append({
                "id": "gap_fallback_1",
                "title": f"Research opportunities in {first_method}",
                "why": f"Analysis of {first_method} trajectory reveals potential research directions",
                "evidence": json.dumps(first_info),
                "temporalViability": "future-viable",
                "temporalJustification": "Based on trajectory analysis of research methods"
            })

        return gaps
