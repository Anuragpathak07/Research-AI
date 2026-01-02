import { useState, useEffect } from "react";
import { PageLayout } from "@/components/layout/PageLayout";
import { AlertCircle, Lightbulb, Target, Database, BarChart3, CheckCircle, Clock, TrendingUp, AlertTriangle, XCircle, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useResearch } from "@/context/ResearchContext";
import { Button } from "@/components/ui/button";

type TemporalViability = "future-viable" | "time-sensitive" | "likely-obsolete";

interface Gap {
  id: string;
  title: string;
  why: string;
  evidence: string;
  temporalViability: TemporalViability;
  temporalJustification: string;
}

interface Experiment {
  id: string;
  objective: string;
  dataset: string;
  models: string[];
  metrics: string[];
  outcome: string;
  recommended?: boolean;
  temporalRelevance: string;
  futureProofDesign: string;
}

const defaultResearchGaps: Gap[] = [
  {
    id: "1",
    title: "Limited evaluation on real-world noisy datasets",
    why: "Current benchmarks use synthetic corruptions that may not reflect actual deployment conditions. Models optimized for these benchmarks may fail in production.",
    evidence: "Only 3 of 91 papers evaluate on real-world noise datasets; ImageNet-C dominates with 78% usage.",
    temporalViability: "future-viable",
    temporalJustification: "Real-world deployment emphasis is accelerating across ML. Industry adoption driving demand for deployment-ready evaluation. Expected relevance: 5+ years.",
  },
  {
    id: "2",
    title: "Lack of cross-dataset generalization analysis",
    why: "Robustness methods are typically evaluated on the same distribution they were trained on, leaving generalization to new domains unexplored.",
    evidence: "Cross-dataset evaluation appears in <10% of papers; most report single-dataset metrics.",
    temporalViability: "future-viable",
    temporalJustification: "Foundation model era demands cross-domain generalization. Trajectory aligned with scaling paradigm. Expected relevance: 5+ years.",
  },
  {
    id: "3",
    title: "Underexplored efficiency-robustness trade-off",
    why: "Adversarial training increases computational cost 3-10x, making robust models impractical for edge deployment.",
    evidence: "Only 5 papers explicitly measure computational overhead; efficiency metrics absent from 95% of evaluations.",
    temporalViability: "time-sensitive",
    temporalJustification: "High current relevance but hardware advances may reduce urgency. Window: 2-3 years before efficient robust training becomes commoditized.",
  },
  {
    id: "4",
    title: "Missing long-tail robustness evaluation",
    why: "Real-world data follows long-tail distributions, but robustness is primarily evaluated on balanced datasets.",
    evidence: "Zero papers evaluate robustness under class imbalance; ImageNet-LT unused for robustness studies.",
    temporalViability: "future-viable",
    temporalJustification: "Long-tail recognition is rising research direction. Intersection with robustness unexplored. First-mover advantage available.",
  },
  {
    id: "5",
    title: "Single-architecture adversarial training optimization",
    why: "Most adversarial training techniques optimized for ResNets; transfer to modern architectures unexplored.",
    evidence: "85% of adversarial training papers use ResNet variants; ViT-specific training underexplored.",
    temporalViability: "likely-obsolete",
    temporalJustification: "Architecture-based robustness emerging as alternative paradigm. Training-based methods showing saturation. Risk of obsolescence within 2 years.",
  },
];

const defaultProposedExperiments: Experiment[] = [
  {
    id: "1",
    objective: "Evaluate state-of-the-art robust models on real-world noise datasets",
    dataset: "NICO++, DomainNet, OpenImages-N",
    models: ["PGD-AT ResNet-50", "Smooth ViT-B", "Standard ViT-L"],
    metrics: ["Clean Accuracy", "Real-world Noise Accuracy", "Domain Gap"],
    outcome: "Quantify the gap between synthetic and real-world robustness to guide future benchmark design.",
    recommended: true,
    temporalRelevance: "Aligned with rising deployment-oriented evaluation trend. Architecture-based models included for future relevance.",
    futureProofDesign: "Includes ViT models positioned for long-term dominance. Benchmark selection emphasizes real-world signals over synthetic proxies.",
  },
  {
    id: "2",
    objective: "Cross-dataset robustness transfer study",
    dataset: "Train: ImageNet → Eval: CIFAR-100, Caltech-256, SUN397",
    models: ["Adversarial Training variants", "Data Augmentation baselines"],
    metrics: ["Transfer Robust Accuracy", "Relative Robustness Retention"],
    outcome: "Identify which robustness mechanisms generalize beyond training distribution.",
    temporalRelevance: "Foundation model paradigm makes cross-dataset evaluation increasingly critical. Growing publication venue interest.",
    futureProofDesign: "Methodology applicable to future model scales. Transfer evaluation framework reusable across architectures.",
  },
  {
    id: "3",
    objective: "Efficient adversarial training with knowledge distillation",
    dataset: "CIFAR-100, ImageNet-100",
    models: ["Teacher: PGD-AT WRN-70-16", "Student: MobileNetV3"],
    metrics: ["Robust Accuracy", "FLOPs", "Inference Latency", "Pareto Efficiency"],
    outcome: "Develop practical robust models for resource-constrained deployment.",
    recommended: true,
    temporalRelevance: "Time-sensitive opportunity: 2-3 year window before efficient training becomes standard. High impact potential.",
    futureProofDesign: "Student models selected for edge deployment relevance. Pareto efficiency metrics future-standard.",
  },
  {
    id: "4",
    objective: "Long-tail adversarial robustness benchmark",
    dataset: "ImageNet-LT with adversarial perturbations",
    models: ["Class-balanced AT", "Focal Loss + AT", "LDAM-DRW + AT"],
    metrics: ["Head/Medium/Tail Robust Accuracy", "Worst-class Robustness"],
    outcome: "Establish first benchmark for robustness under class imbalance.",
    temporalRelevance: "First-mover advantage: unexplored intersection of two rising research areas. High citation potential.",
    futureProofDesign: "Benchmark designed for extension to other long-tail datasets. Evaluation framework applicable to future methods.",
  },
];

const getViabilityIcon = (viability: TemporalViability) => {
  switch (viability) {
    case "future-viable": return TrendingUp;
    case "time-sensitive": return Clock;
    case "likely-obsolete": return XCircle;
  }
};

const getViabilityColor = (viability: TemporalViability) => {
  switch (viability) {
    case "future-viable": return "text-green-600 bg-green-50 border-green-200";
    case "time-sensitive": return "text-amber-600 bg-amber-50 border-amber-200";
    case "likely-obsolete": return "text-red-600 bg-red-50 border-red-200";
  }
};

const getViabilityLabel = (viability: TemporalViability) => {
  switch (viability) {
    case "future-viable": return "Future-Viable";
    case "time-sensitive": return "Time-Sensitive";
    case "likely-obsolete": return "Likely Obsolete";
  }
};

export default function Gaps() {
  const { clusters, gaps, setGaps, experiments, setExperiments, loading, setLoading } = useResearch();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (clusters.length > 0 && gaps.length === 0 && !loading.gaps) {
      fetchGaps();
    }
  }, [clusters]);

  // Don't auto-fetch experiments - user should click button

  const fetchGaps = async () => {
    if (clusters.length === 0) {
      setError("Please generate clusters first on the Clusters page.");
      return;
    }

    try {
      setLoading({ gaps: true });
      setError(null);

      const response = await fetch("/api/gaps/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(clusters),
      });

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.error || errorMessage;
        } catch {
          // If response is not JSON, use default message
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      
      // Transform backend response to match frontend format
      const transformedGaps = data.map((gap: any, index: number) => ({
        id: String(index + 1),
        title: gap.gap || "Unknown gap",
        why: gap.reason || "Analysis needed",
        evidence: `Identified from cluster analysis`,
        temporalViability: gap.viability?.toLowerCase().includes("future") ? "future-viable" :
                          gap.viability?.toLowerCase().includes("time") ? "time-sensitive" : "likely-obsolete",
        temporalJustification: gap.reason || "Based on trajectory analysis",
      }));

      setGaps(transformedGaps);
      setLoading({ gaps: false });
    } catch (error) {
      console.error("Error fetching gaps:", error);
      setError("Failed to fetch gaps. Please check if the backend is running.");
      setLoading({ gaps: false });
    }
  };

  const fetchExperiments = async () => {
    if (gaps.length === 0) {
      return;
    }

    try {
      setLoading({ experiments: true });

      const gapsForBackend = gaps.map((g) => ({
        gap: g.title,
        viability: g.temporalViability,
        reason: g.why,
      }));

      const response = await fetch("/api/experiments/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(gapsForBackend),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Transform backend response to match frontend format
      const transformedExperiments = data.map((exp: any, index: number) => ({
        id: String(index + 1),
        objective: exp.objective || "Unknown objective",
        dataset: Array.isArray(exp.datasets) ? exp.datasets.join(", ") : exp.datasets || "TBD",
        models: Array.isArray(exp.models) ? exp.models : [exp.models || "TBD"],
        metrics: Array.isArray(exp.metrics) ? exp.metrics : [exp.metrics || "TBD"],
        outcome: "To be determined based on experiment results",
        recommended: index < 2, // First 2 are recommended
        temporalRelevance: "Aligned with identified research gaps",
        futureProofDesign: "Designed to address temporal viability concerns",
      }));

      setExperiments(transformedExperiments);
      setLoading({ experiments: false });
    } catch (error) {
      console.error("Error fetching experiments:", error);
      setLoading({ experiments: false });
    }
  };

  return (
    <PageLayout>
      <div className="min-h-screen py-24 px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          {/* Header */}
          <div className="text-center mb-16 animate-fade-in">
            <h1 className="text-4xl md:text-5xl font-semibold text-foreground mb-4">
              Obsolescence-Aware Gap Detection
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Gaps classified by temporal viability with future-aligned experiment proposals.
            </p>
            {clusters.length === 0 && (
              <div className="mt-6 p-4 rounded-lg bg-amber-50 border border-amber-200 flex items-center gap-3 justify-center">
                <AlertCircle className="h-5 w-5 text-amber-600" />
                <span className="text-amber-800">Please generate clusters first on the Clusters page.</span>
              </div>
            )}
            {clusters.length > 0 && gaps.length === 0 && !loading.gaps && (
              <Button onClick={fetchGaps} className="mt-6" variant="premium">
                Detect Gaps
              </Button>
            )}
            {loading.gaps && (
              <div className="mt-6 flex items-center gap-2 justify-center">
                <Loader2 className="h-5 w-5 animate-spin" />
                <span className="text-muted-foreground">Detecting gaps...</span>
              </div>
            )}
            {error && (
              <div className="mt-6 p-4 rounded-lg bg-red-50 border border-red-200 flex items-center gap-3 justify-center">
                <AlertCircle className="h-5 w-5 text-red-600" />
                <span className="text-red-800">{error}</span>
              </div>
            )}
          </div>

          {/* Legend */}
          <div className="flex flex-wrap items-center justify-center gap-4 mb-12 p-4 rounded-xl bg-secondary/30">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500" />
              <span className="text-sm text-muted-foreground">Future-Viable: Will remain relevant 5+ years</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-amber-500" />
              <span className="text-sm text-muted-foreground">Time-Sensitive: 2-3 year window</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500" />
              <span className="text-sm text-muted-foreground">Likely Obsolete: Declining trajectory</span>
            </div>
          </div>

          {/* Research Gaps Section */}
          <section className="mb-20">
            <div className="flex items-center gap-3 mb-8">
              <div className="w-10 h-10 rounded-xl bg-beige-light flex items-center justify-center">
                <AlertCircle className="w-5 h-5 text-beige-dark" strokeWidth={1.5} />
              </div>
              <div>
                <h2 className="text-2xl font-medium text-foreground">
                  Identified Research Gaps
                </h2>
                <p className="text-sm text-muted-foreground">
                  Each gap annotated with temporal viability assessment
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-6">
              {gaps.length === 0 && !loading.gaps && (
                <div className="text-center py-12 p-6 rounded-xl bg-secondary/30 border border-border/50">
                  <AlertCircle className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground mb-4">No gaps detected yet. Click "Detect Gaps" to analyze your clusters.</p>
                </div>
              )}
              {gaps.map((gap, index) => {
                const ViabilityIcon = getViabilityIcon(gap.temporalViability);
                return (
                  <div
                    key={gap.id}
                    className="p-6 rounded-2xl bg-card border border-border/50 shadow-premium hover:shadow-premium-lg transition-all duration-300 animate-slide-up"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <div className="flex items-start justify-between gap-4 mb-4">
                      <h3 className="text-base font-medium text-foreground leading-snug flex-1">
                        {gap.title}
                      </h3>
                      <div className={cn(
                        "shrink-0 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border",
                        getViabilityColor(gap.temporalViability)
                      )}>
                        <ViabilityIcon className="w-3.5 h-3.5" />
                        {getViabilityLabel(gap.temporalViability)}
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                      <div>
                        <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground mb-1">
                          <Lightbulb className="w-4 h-4" />
                          Why it matters
                        </div>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          {gap.why}
                        </p>
                      </div>

                      <div>
                        <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground mb-1">
                          <BarChart3 className="w-4 h-4" />
                          Evidence
                        </div>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          {gap.evidence}
                        </p>
                      </div>
                    </div>

                    {/* Temporal Justification */}
                    <div className={cn(
                      "p-3 rounded-lg border",
                      gap.temporalViability === "future-viable" && "bg-green-50/50 border-green-200",
                      gap.temporalViability === "time-sensitive" && "bg-amber-50/50 border-amber-200",
                      gap.temporalViability === "likely-obsolete" && "bg-red-50/50 border-red-200"
                    )}>
                      <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground mb-1">
                        <Clock className="w-3.5 h-3.5" />
                        Temporal Justification
                      </div>
                      <p className="text-sm text-foreground">
                        {gap.temporalJustification}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>

          {/* Proposed Experiments Section */}
          {gaps.length > 0 && (
            <section>
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-beige-light flex items-center justify-center">
                    <Target className="w-5 h-5 text-beige-dark" strokeWidth={1.5} />
                  </div>
                  <div>
                    <h2 className="text-2xl font-medium text-foreground">
                      Future-Aligned Experiments
                    </h2>
                    <p className="text-sm text-muted-foreground">
                      Proposals aligned with rising or stable trajectories only
                    </p>
                  </div>
                </div>
                {experiments.length === 0 && !loading.experiments && (
                  <Button onClick={fetchExperiments} variant="premium" className="gap-2">
                    <Target className="h-4 w-4" />
                    Generate Experiments
                  </Button>
                )}
                {loading.experiments && (
                  <div className="flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span className="text-sm text-muted-foreground">Generating experiments...</span>
                  </div>
                )}
              </div>

              {experiments.length === 0 && !loading.experiments && (
                <div className="text-center py-12 p-6 rounded-xl bg-secondary/30 border border-border/50">
                  <Target className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground mb-4">No experiments generated yet. Click "Generate Experiments" to create experiment proposals.</p>
                </div>
              )}

              <div className="space-y-6">
                {experiments.map((exp, index) => (
                <div
                  key={exp.id}
                  className={cn(
                    "p-6 rounded-2xl border shadow-premium transition-all duration-300 animate-slide-up",
                    exp.recommended
                      ? "bg-beige-light/30 border-beige"
                      : "bg-card border-border/50"
                  )}
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  {exp.recommended && (
                    <div className="flex items-center gap-2 mb-4">
                      <span className="px-3 py-1 rounded-full bg-beige text-xs font-medium text-navy">
                        Recommended Experiment
                      </span>
                    </div>
                  )}

                  <h3 className="text-lg font-medium text-foreground mb-6">
                    {exp.objective}
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                      <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground mb-2">
                        <Database className="w-4 h-4" />
                        Dataset
                      </div>
                      <p className="text-sm text-foreground">{exp.dataset}</p>
                    </div>

                    <div>
                      <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground mb-2">
                        <BarChart3 className="w-4 h-4" />
                        Metrics
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {exp.metrics.map((metric) => (
                          <span
                            key={metric}
                            className="px-2 py-1 rounded-md bg-secondary text-xs text-muted-foreground"
                          >
                            {metric}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="md:col-span-2">
                      <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground mb-2">
                        Models
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {exp.models.map((model) => (
                          <span
                            key={model}
                            className="px-3 py-1 rounded-lg bg-secondary text-sm text-foreground"
                          >
                            {model}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Temporal Relevance Notes */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 rounded-xl bg-secondary/30 mb-4">
                    <div>
                      <div className="flex items-center gap-2 text-xs font-medium text-beige-dark mb-1">
                        <TrendingUp className="w-3.5 h-3.5" />
                        Temporal Relevance
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {exp.temporalRelevance}
                      </p>
                    </div>
                    <div>
                      <div className="flex items-center gap-2 text-xs font-medium text-beige-dark mb-1">
                        <Clock className="w-3.5 h-3.5" />
                        Future-Proof Design
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {exp.futureProofDesign}
                      </p>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-border/50">
                    <div className="flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 text-beige-dark mt-0.5 shrink-0" />
                      <div>
                        <span className="text-sm font-medium text-muted-foreground">
                          Expected Outcome:
                        </span>
                        <p className="text-sm text-foreground mt-1">
                          {exp.outcome}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
                ))}
              </div>
            </section>
          )}
        </div>
      </div>
    </PageLayout>
  );
}
