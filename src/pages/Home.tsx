import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { PageLayout } from "@/components/layout/PageLayout";
import { 
  Search, 
  Brain, 
  Layers, 
  Target, 
  Beaker, 
  ArrowRight,
  ChevronRight,
  Clock,
  TrendingUp,
  Eye
} from "lucide-react";

const workflowSteps = [
  { icon: Search, label: "Discover", description: "Temporal paper retrieval" },
  { icon: Clock, label: "Trajectory", description: "Model research evolution" },
  { icon: Layers, label: "Synthesize", description: "Longitudinal analysis" },
  { icon: Target, label: "Detect Gaps", description: "Obsolescence-aware" },
  { icon: Beaker, label: "Propose", description: "Future-aligned experiments" },
];

const comparisons = [
  { traditional: "Static literature review", researchai: "Temporal knowledge modeling" },
  { traditional: "Gap = absence", researchai: "Gap = absence + future relevance" },
  { traditional: "One-shot summaries", researchai: "Longitudinal trend reasoning" },
  { traditional: "Reactive assistance", researchai: "Proactive scientific foresight" },
];

export default function Home() {
  return (
    <PageLayout>
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center justify-center px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          {/* Badge */}
          <div className="animate-fade-in mb-8">
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-secondary text-sm font-medium text-muted-foreground">
              <span className="w-2 h-2 rounded-full bg-beige animate-pulse" />
              Temporal Agentic Research System
            </span>
          </div>

          {/* Main Headline */}
          <h1 className="animate-slide-up text-5xl md:text-7xl font-semibold tracking-tight text-foreground leading-[1.1] mb-6">
            Research,
            <br />
            <span className="text-beige-dark">Future-Aware.</span>
          </h1>

          {/* Subheadline */}
          <p className="animate-slide-up-delay-1 text-xl md:text-2xl text-muted-foreground font-light max-w-2xl mx-auto mb-8 leading-relaxed">
            An agentic AI system that forecasts the future relevance of scientific research 
            and proposes experiments aligned with long-term impact.
          </p>

          {/* Core Innovation Badge */}
          <div className="animate-slide-up-delay-1 mb-12">
            <div className="inline-flex items-center gap-3 px-5 py-3 rounded-xl bg-beige-light/50 border border-beige/30">
              <TrendingUp className="w-5 h-5 text-beige-dark" />
              <span className="text-sm font-medium text-foreground">
                Temporal Research Trajectory Modeling + Obsolescence-Aware Gap Detection
              </span>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="animate-slide-up-delay-2 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button variant="hero" size="lg" asChild>
              <Link to="/discover">
                Start with a Topic
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button variant="hero-outline" size="lg" asChild>
              <Link to="/about">
                See How It Works
                <ChevronRight className="ml-1 h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>

        {/* Subtle gradient overlay */}
        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-beige-light/20 via-transparent to-transparent" />
      </section>

      {/* Key Question Section */}
      <section className="py-20 px-6 lg:px-8 border-t border-border/50">
        <div className="max-w-4xl mx-auto text-center">
          <div className="animate-fade-in">
            <p className="text-lg text-muted-foreground mb-4">The key question we address:</p>
            <h2 className="text-3xl md:text-4xl font-semibold text-foreground mb-6">
              Not just "What gaps exist?"
              <br />
              <span className="text-beige-dark">but "Which gaps will still matter in the future?"</span>
            </h2>
          </div>
        </div>
      </section>

      {/* Workflow Section */}
      <section className="py-24 px-6 lg:px-8 bg-secondary/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-semibold text-foreground mb-4 animate-fade-in">
              From Topic to Future-Aligned Research
            </h2>
            <p className="text-lg text-muted-foreground max-w-xl mx-auto">
              Time-aware agentic reasoning through the entire research lifecycle.
            </p>
          </div>

          {/* Workflow Steps */}
          <div className="relative">
            {/* Connection Line */}
            <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-px bg-border -translate-y-1/2 z-0" />
            
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-8 relative z-10">
              {workflowSteps.map((step, index) => (
                <div 
                  key={step.label}
                  className="flex flex-col items-center text-center animate-slide-up"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="w-16 h-16 rounded-2xl bg-card shadow-premium flex items-center justify-center mb-4 border border-border/50">
                    <step.icon className="w-7 h-7 text-beige-dark" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-base font-medium text-foreground mb-1">
                    {step.label}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    {step.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Comparison Section */}
      <section className="py-24 px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-semibold text-foreground mb-4">
              Beyond Traditional Systems
            </h2>
            <p className="text-lg text-muted-foreground">
              ResearchAI treats scientific knowledge as a dynamic, evolving trajectory.
            </p>
          </div>

          <div className="rounded-2xl bg-card border border-border/50 shadow-premium overflow-hidden">
            <div className="grid grid-cols-2 divide-x divide-border/50">
              <div className="p-4 bg-secondary/50 text-center">
                <span className="text-sm font-medium text-muted-foreground">Traditional Systems</span>
              </div>
              <div className="p-4 bg-beige-light/30 text-center">
                <span className="text-sm font-medium text-beige-dark">ResearchAI</span>
              </div>
            </div>
            {comparisons.map((item, index) => (
              <div 
                key={index} 
                className="grid grid-cols-2 divide-x divide-border/50 border-t border-border/50"
              >
                <div className="p-4 text-center text-sm text-muted-foreground">
                  {item.traditional}
                </div>
                <div className="p-4 text-center text-sm text-foreground font-medium">
                  {item.researchai}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Value Proposition */}
      <section className="py-24 px-6 lg:px-8 bg-secondary/30">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-semibold text-foreground mb-6">
            Strategic Research Decisions
          </h2>
          <p className="text-lg text-muted-foreground mb-12 max-w-2xl mx-auto">
            ResearchAI assists researchers in making future-aware strategic decisions.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { icon: Eye, title: "Forecast Relevance", description: "Predict which research directions will matter" },
              { icon: Target, title: "Prevent Obsolescence", description: "Avoid soon-to-be outdated approaches" },
              { icon: TrendingUp, title: "Long-term Impact", description: "Highlight underexplored high-impact areas" },
            ].map((feature, index) => (
              <div 
                key={feature.title}
                className="p-8 rounded-2xl bg-card shadow-premium border border-border/50"
              >
                <div className="w-12 h-12 rounded-xl bg-beige-light flex items-center justify-center mx-auto mb-4">
                  <feature.icon className="w-6 h-6 text-beige-dark" strokeWidth={1.5} />
                </div>
                <h3 className="text-lg font-medium text-foreground mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-muted-foreground">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <section className="py-24 px-6 lg:px-8">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-semibold text-foreground mb-6">
            Ready for Future-Aware Research?
          </h2>
          <p className="text-lg text-muted-foreground mb-8">
            Enter your research topic and let temporal AI agents guide your strategic decisions.
          </p>
          <Button variant="premium" size="xl" asChild>
            <Link to="/discover">
              Enter Research Topic
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>
      </section>
    </PageLayout>
  );
}
