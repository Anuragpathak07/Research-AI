import { PageLayout } from "@/components/layout/PageLayout";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Search,
  FileText,
  Layers,
  Brain,
  Target,
  Beaker,
  Code,
  ArrowRight,
  Clock,
  TrendingUp,
  Activity,
  Eye,
} from "lucide-react";

const agentArchitecture = [
  {
    icon: Search,
    title: "Discovery Agent",
    description: "Retrieves papers over a defined time window (e.g., 2015–2025), preserving publication timestamps and venues for temporal analysis.",
    output: "Chronologically ordered paper corpus",
  },
  {
    icon: Clock,
    title: "Temporal Extraction Agent",
    description: "Extracts time-sensitive entities: methods, datasets, metrics, and experimental settings with associated temporal metadata.",
    output: "Timestamped research entities",
  },
  {
    icon: Activity,
    title: "Trajectory Modeling Agent",
    description: "The flagship agent that models research idea lifecycles: emergence, acceleration, saturation, decline, and obsolescence risk.",
    output: "Trajectory labels + momentum scores",
  },
  {
    icon: Target,
    title: "Obsolescence-Aware Gap Detection",
    description: "Detects gaps conditioned on temporal viability. Classifies gaps as Future-Viable, Time-Sensitive, or Likely Obsolete.",
    output: "Temporally-annotated research gaps",
  },
  {
    icon: Beaker,
    title: "Experiment Forecasting Agent",
    description: "Proposes experiments aligned with rising or stable trajectories. Avoids experiments tied to declining assumptions.",
    output: "Time-justified experiment proposals",
  },
  {
    icon: Code,
    title: "Code Generation Agent",
    description: "Generates experiment code with temporal relevance notes, future-proof design assumptions, and suggested extensions.",
    output: "Forward-compatible code scaffolds",
  },
];

const temporalSignals = [
  "Publication frequency per method",
  "Citation velocity (growth, stagnation, decay)",
  "Dataset reuse saturation",
  "Metric replacement trends",
  "Synthetic to real-world benchmark shift",
  "Complexity vs performance trade-offs",
];

const useCases = [
  { title: "PhD Students", description: "Choosing long-term thesis directions" },
  { title: "Researchers", description: "Avoiding dead-end problem formulations" },
  { title: "Research Labs", description: "Planning multi-year research agendas" },
  { title: "Funding Bodies", description: "Assessing proposal future relevance" },
];

export default function About() {
  return (
    <PageLayout>
      <div className="min-h-screen py-24 px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          {/* Header */}
          <div className="text-center mb-20 animate-fade-in">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-beige-light/50 text-sm font-medium text-beige-dark mb-6">
              <TrendingUp className="w-4 h-4" />
              Temporal Agentic System
            </div>
            <h1 className="text-4xl md:text-5xl font-semibold text-foreground mb-6">
              How ResearchAI Works
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              An agentic, temporal reasoning system that forecasts the future relevance 
              of scientific research directions and proposes experiments aligned with 
              long-term impact rather than short-term novelty.
            </p>
          </div>

          {/* Core Innovation */}
          <div className="mb-20 p-8 rounded-2xl bg-beige-light/30 border border-beige/30 animate-slide-up">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-semibold text-foreground mb-2">
                Core Innovation
              </h2>
              <p className="text-beige-dark font-medium">
                Temporal Research Trajectory Modeling + Obsolescence-Aware Gap Detection
              </p>
            </div>
            <div className="text-center">
              <p className="text-muted-foreground max-w-2xl mx-auto">
                Unlike existing AI research assistants that treat literature as static, 
                ResearchAI treats scientific knowledge as a <strong className="text-foreground">dynamic, evolving trajectory</strong>. 
                The system models how research ideas evolve over time, enabling future-viable 
                gap detection and experiment proposal.
              </p>
            </div>
          </div>

          {/* Key Question */}
          <div className="mb-20 text-center animate-slide-up-delay-1">
            <div className="inline-flex items-center gap-2 mb-4">
              <Eye className="w-5 h-5 text-beige-dark" />
              <span className="text-sm font-medium text-muted-foreground">Key Question Addressed</span>
            </div>
            <h2 className="text-3xl md:text-4xl font-semibold text-foreground">
              Not just "What gaps exist?"
              <br />
              <span className="text-beige-dark">but "Which gaps will still matter in the future?"</span>
            </h2>
          </div>

          {/* Agent Architecture */}
          <div className="mb-20">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-semibold text-foreground mb-4">
                Agent Architecture
              </h2>
              <p className="text-muted-foreground max-w-xl mx-auto">
                A coordinated system of specialized agents for temporal research analysis.
              </p>
            </div>

            {/* Vertical Line */}
            <div className="relative">
              <div className="absolute left-8 top-0 bottom-0 w-px bg-border hidden md:block" />

              <div className="space-y-8">
                {agentArchitecture.map((agent, index) => (
                  <div
                    key={agent.title}
                    className="relative flex gap-8 animate-slide-up"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    {/* Icon */}
                    <div className="relative z-10 shrink-0">
                      <div className="w-16 h-16 rounded-2xl bg-card border border-border/50 shadow-premium flex items-center justify-center">
                        <agent.icon className="w-7 h-7 text-beige-dark" strokeWidth={1.5} />
                      </div>
                    </div>

                    {/* Content */}
                    <div className="flex-1 pt-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-xs font-medium text-beige-dark px-2 py-1 rounded-md bg-beige-light">
                          Agent {index + 1}
                        </span>
                      </div>
                      <h3 className="text-xl font-medium text-foreground mb-2">
                        {agent.title}
                      </h3>
                      <p className="text-muted-foreground leading-relaxed mb-3">
                        {agent.description}
                      </p>
                      <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-secondary text-sm">
                        <ArrowRight className="w-3.5 h-3.5 text-beige-dark" />
                        <span className="text-muted-foreground">Output: </span>
                        <span className="text-foreground font-medium">{agent.output}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Temporal Signals */}
          <div className="mb-20 animate-slide-up-delay-2">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-semibold text-foreground mb-2">
                Temporal Signals Analyzed
              </h2>
              <p className="text-muted-foreground">
                ResearchAI reasons over longitudinal indicators
              </p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {temporalSignals.map((signal) => (
                <div
                  key={signal}
                  className="p-4 rounded-xl bg-card border border-border/50 text-center"
                >
                  <span className="text-sm text-foreground">{signal}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Use Cases */}
          <div className="mb-20">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-semibold text-foreground mb-2">
                Who Benefits
              </h2>
              <p className="text-muted-foreground">
                Strategic research decision support for
              </p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {useCases.map((useCase) => (
                <div
                  key={useCase.title}
                  className="p-6 rounded-2xl bg-card border border-border/50 shadow-premium text-center"
                >
                  <h3 className="text-base font-medium text-foreground mb-1">
                    {useCase.title}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    {useCase.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Strengths */}
          <div className="mb-20 p-8 rounded-2xl bg-secondary/30">
            <h2 className="text-2xl font-semibold text-foreground text-center mb-8">
              Approach Strengths
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                "Extremely hard to replicate",
                "Moves beyond summarization",
                "Scientifically meaningful",
                "Strong agentic justification",
              ].map((strength) => (
                <div
                  key={strength}
                  className="p-4 rounded-xl bg-card border border-border/50 text-center"
                >
                  <span className="text-sm font-medium text-foreground">{strength}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Research Contribution */}
          <div className="mb-20 text-center">
            <h2 className="text-2xl font-semibold text-foreground mb-6">
              Research Contribution
            </h2>
            <div className="space-y-3 max-w-xl mx-auto">
              {[
                "A temporal framing of research gaps",
                "Obsolescence-aware scientific reasoning",
                "An agentic architecture for future-aware discovery",
                "A shift from reactive to strategic research assistance",
              ].map((contribution, index) => (
                <div
                  key={contribution}
                  className="flex items-center gap-3 p-3 rounded-lg bg-card border border-border/50"
                >
                  <span className="w-6 h-6 rounded-full bg-beige-light flex items-center justify-center text-xs font-medium text-beige-dark">
                    {index + 1}
                  </span>
                  <span className="text-foreground">{contribution}</span>
                </div>
              ))}
            </div>
          </div>

          {/* CTA */}
          <div className="text-center animate-slide-up-delay-2">
            <h2 className="text-3xl font-semibold text-foreground mb-4">
              Ready for Future-Aware Research?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Start with any research topic and let temporal AI agents guide your strategic decisions.
            </p>
            <Button variant="premium" size="xl" asChild>
              <Link to="/discover">
                Start with a Topic
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </PageLayout>
  );
}
