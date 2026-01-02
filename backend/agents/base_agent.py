# agents/base_agent.py
"""
Base agent class implementing ReAct (Reasoning + Acting) pattern
for agentic AI capabilities
"""
from services.llm_service import LLMService
import json
import re

class BaseAgent:
    """Base class for all agents with ReAct reasoning capabilities"""
    
    def __init__(self, name, description, tools=None):
        self.name = name
        self.description = description
        self.llm_service = LLMService()
        self.tools = tools or []
        self.reasoning_history = []
    
    def _format_tools_prompt(self):
        """Format available tools for the LLM"""
        if not self.tools:
            return "No tools available."
        
        tools_desc = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in self.tools
        ])
        return f"Available tools:\n{tools_desc}"
    
    def _parse_reasoning(self, response):
        """Parse ReAct-style reasoning from LLM response"""
        # Look for Thought/Action/Action Input/Observation pattern
        thought_match = re.search(r'Thought:\s*(.+?)(?=Action:|$)', response, re.DOTALL)
        action_match = re.search(r'Action:\s*(\w+)', response)
        action_input_match = re.search(r'Action Input:\s*(.+?)(?=Observation:|$)', response, re.DOTALL)
        observation_match = re.search(r'Observation:\s*(.+?)(?=Thought:|Final Answer:|$)', response, re.DOTALL)
        final_answer_match = re.search(r'Final Answer:\s*(.+?)$', response, re.DOTALL)
        
        return {
            'thought': thought_match.group(1).strip() if thought_match else None,
            'action': action_match.group(1) if action_match else None,
            'action_input': action_input_match.group(1).strip() if action_input_match else None,
            'observation': observation_match.group(1).strip() if observation_match else None,
            'final_answer': final_answer_match.group(1).strip() if final_answer_match else None,
            'raw': response
        }
    
    def _execute_tool(self, tool_name, tool_input):
        """Execute a tool by name"""
        for tool in self.tools:
            if tool['name'] == tool_name:
                try:
                    # Parse tool input if it's JSON
                    if isinstance(tool_input, str):
                        try:
                            tool_input = json.loads(tool_input)
                        except:
                            pass
                    
                    result = tool['func'](tool_input)
                    return str(result)
                except Exception as e:
                    return f"Error executing tool {tool_name}: {str(e)}"
        
        return f"Tool {tool_name} not found"
    
    def reason_and_act(self, task, context=None, max_iterations=5):
        """
        ReAct pattern: Reason about the task, take actions, observe results
        
        Args:
            task: The task description
            context: Additional context for the task
            max_iterations: Maximum reasoning iterations
        
        Returns:
            Final result from the agent
        """
        self.reasoning_history = []
        
        # Build initial prompt
        system_prompt = f"""You are {self.name}, {self.description}

You use the ReAct (Reasoning + Acting) pattern:
1. **Thought**: Think about what you need to do
2. **Action**: Choose a tool to use (or "Final Answer" if done)
3. **Action Input**: Provide input for the action
4. **Observation**: Observe the result
5. Repeat until you have a final answer

{self._format_tools_prompt()}

Format your response as:
Thought: [your reasoning]
Action: [tool name or "Final Answer"]
Action Input: [input for the action]
Observation: [result from the action]

Continue this pattern until you reach a Final Answer."""

        user_prompt = f"Task: {task}"
        if context:
            user_prompt += f"\n\nContext: {json.dumps(context, indent=2)}"
        
        full_prompt = f"{system_prompt}\n\n{user_prompt}\n\nBegin reasoning:"
        
        # ReAct loop
        for iteration in range(max_iterations):
            try:
                # Get LLM response
                response = self.llm_service.generate(full_prompt, temperature=0.3)
                
                # Parse reasoning
                reasoning = self._parse_reasoning(response)
                self.reasoning_history.append(reasoning)
                
                # Check for final answer
                if reasoning['final_answer']:
                    return {
                        'result': reasoning['final_answer'],
                        'reasoning_history': self.reasoning_history
                    }
                
                # Execute action if present
                if reasoning['action']:
                    if reasoning['action'].lower() == 'final answer':
                        return {
                            'result': reasoning['action_input'] or reasoning['thought'],
                            'reasoning_history': self.reasoning_history
                        }
                    
                    # Execute tool
                    observation = self._execute_tool(reasoning['action'], reasoning['action_input'])
                    
                    # Update prompt with observation
                    full_prompt += f"\n\n{response}\nObservation: {observation}\n\nContinue reasoning:"
                else:
                    # No action, try to extract final answer from thought
                    if reasoning['thought']:
                        # Check if thought contains a conclusion
                        if 'conclusion' in reasoning['thought'].lower() or 'answer' in reasoning['thought'].lower():
                            return {
                                'result': reasoning['thought'],
                                'reasoning_history': self.reasoning_history
                            }
                    
                    # Continue reasoning
                    full_prompt += f"\n\n{response}\n\nContinue with next Thought and Action:"
            
            except Exception as e:
                # Fallback: return what we have
                return {
                    'result': f"Error during reasoning: {str(e)}",
                    'reasoning_history': self.reasoning_history,
                    'error': str(e)
                }
        
        # Max iterations reached
        last_reasoning = self.reasoning_history[-1] if self.reasoning_history else {}
        return {
            'result': last_reasoning.get('thought') or last_reasoning.get('final_answer', 'Max iterations reached'),
            'reasoning_history': self.reasoning_history,
            'warning': 'Max iterations reached'
        }
    
    def simple_reason(self, prompt, context=None):
        """
        Simplified reasoning without ReAct loop - just LLM reasoning
        Use this for simpler tasks that don't need tool use
        """
        full_prompt = f"""You are {self.name}, {self.description}

Task: {prompt}"""
        
        if context:
            full_prompt += f"\n\nContext:\n{json.dumps(context, indent=2)}"
        
        full_prompt += "\n\nProvide your analysis and reasoning:"
        
        try:
            response = self.llm_service.generate(full_prompt, temperature=0.4)
            return {
                'result': response,
                'reasoning': response
            }
        except Exception as e:
            # Return error but don't fail - allow fallback behavior
            print(f"LLM reasoning failed for {self.name}: {e}")
            return {
                'result': None,
                'reasoning': None,
                'error': str(e),
                'fallback': True
            }

