# pipelines/temporal_pipeline.py
from agents.trajectory_agent import TrajectoryAgent
from agents.gap_agent import GapAgent

class TemporalPipeline:
    def __init__(self):
        self.trajectory_agent = TrajectoryAgent()
        self.gap_agent = GapAgent()

    def run(self, extracted_papers):
        trajectories = self.trajectory_agent.build_trajectories(extracted_papers)
        gaps = self.gap_agent.detect_gaps(trajectories, extracted_papers)

        return {
            "trajectories": trajectories,
            "gaps": gaps
        }
