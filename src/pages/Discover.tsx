import { useState, useEffect } from "react";
import { PageLayout } from "@/components/layout/PageLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Loader2, ExternalLink, Calendar, BookOpen } from "lucide-react";
import { cn } from "@/lib/utils";
import { useResearch } from "@/context/ResearchContext";

interface Paper {
  id: string;
  title: string;
  year: number;
  venue: string;
  abstract: string;
  authors: string[];
  url?: string;
}

const mockPapers: Paper[] = [
  {
    id: "1",
    title: "Robust Image Classification via Adversarial Training with Data Augmentation",
    year: 2023,
    venue: "NeurIPS",
    abstract: "We propose a novel framework that combines adversarial training with advanced data augmentation techniques to improve model robustness against various perturbations...",
    authors: ["Smith, J.", "Chen, L.", "Wang, M."],
  },
  {
    id: "2",
    title: "Understanding the Trade-offs Between Accuracy and Robustness in Deep Learning",
    year: 2023,
    venue: "ICML",
    abstract: "This paper investigates the fundamental trade-offs between standard accuracy and adversarial robustness, providing theoretical insights and practical guidelines...",
    authors: ["Johnson, A.", "Kumar, P."],
  },
  {
    id: "3",
    title: "Self-Supervised Learning for Robust Visual Representations",
    year: 2022,
    venue: "CVPR",
    abstract: "We introduce a self-supervised learning approach that naturally produces robust representations without requiring adversarial examples during training...",
    authors: ["Zhang, Y.", "Brown, K.", "Lee, S."],
  },
  {
    id: "4",
    title: "Certified Defenses Against Adversarial Patches",
    year: 2023,
    venue: "ICLR",
    abstract: "We present the first certified defense mechanism against adversarial patches with provable guarantees on the maximum perturbation size...",
    authors: ["Miller, R.", "Davis, E."],
  },
  {
    id: "5",
    title: "Robustness Evaluation of Vision Transformers Across Domains",
    year: 2024,
    venue: "AAAI",
    abstract: "A comprehensive study evaluating the robustness of Vision Transformers compared to CNNs across multiple domains and perturbation types...",
    authors: ["Wilson, T.", "Garcia, M.", "Patel, N."],
  },
];

type ProgressStep = "idle" | "searching" | "ranking" | "fetching" | "complete";

const progressSteps: { key: ProgressStep; label: string }[] = [
  { key: "searching", label: "Searching papers" },
  { key: "ranking", label: "Ranking relevance" },
  { key: "fetching", label: "Fetching metadata" },
];

export default function Discover() {
  const [topic, setTopic] = useState("");
  const [progress, setProgress] = useState<ProgressStep>("idle");
  const { papers, setPapers, setLoading } = useResearch();

  // Debug: Log papers changes
  useEffect(() => {
    console.log("Discover page - papers in context:", papers.length);
  }, [papers]);

  const handleDiscover = async () => {
    if (!topic.trim()) return;

    try {
      setProgress("searching");
      setLoading({ papers: true });
      
      const response = await fetch("/api/discover/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: topic,
          start_year: 2015,
          end_year: new Date().getFullYear(),
          max_results: 50,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      setProgress("ranking");
      await new Promise((r) => setTimeout(r, 500));
      
      setProgress("fetching");
      const data = await response.json();
      
      console.log("Backend response:", data);
      
      // Check if response is an error
      if (data.error) {
        throw new Error(data.error);
      }
      
      // Ensure data is an array
      if (!Array.isArray(data)) {
        console.error("Expected array but got:", typeof data, data);
        throw new Error("Invalid response format: expected array");
      }
      
      // Transform API response to match frontend format
      const transformedPapers: Paper[] = data.map((paper: any, index: number) => ({
        id: paper.paper_id || `paper-${index}`,
        title: paper.title || "Untitled",
        year: paper.year || new Date().getFullYear(),
        venue: paper.venue || "Unknown",
        abstract: paper.abstract || "",
        authors: paper.authors || [],
        url: paper.url,
      }));
      
      console.log("Transformed papers:", transformedPapers);
      setPapers(transformedPapers);
      setProgress("complete");
      setLoading({ papers: false });
    } catch (error) {
      console.error("Error discovering papers:", error);
      alert("Failed to discover papers. Please check if the backend is running on port 5005.");
      setProgress("idle");
    }
  };

  const getCurrentStepIndex = () => {
    return progressSteps.findIndex((s) => s.key === progress);
  };

  return (
    <PageLayout>
      <div className="min-h-screen py-24 px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12 animate-fade-in">
            <h1 className="text-4xl md:text-5xl font-semibold text-foreground mb-4">
              Discover Papers
            </h1>
            <p className="text-lg text-muted-foreground max-w-xl mx-auto">
              Enter your research topic and we'll find the most relevant academic papers.
            </p>
          </div>

          {/* Search Input */}
          <div className="animate-slide-up mb-12">
            <div className="relative max-w-2xl mx-auto">
              <div className="flex gap-3">
                <div className="relative flex-1">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                  <Input
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="Enter your research topic (e.g., Robust Image Classification)"
                    className="pl-12 h-14 text-base rounded-xl border-border bg-card shadow-premium focus:ring-2 focus:ring-beige focus:border-beige"
                    onKeyDown={(e) => e.key === "Enter" && handleDiscover()}
                  />
                </div>
                <Button
                  variant="premium"
                  size="lg"
                  onClick={handleDiscover}
                  disabled={!topic.trim() || (progress !== "idle" && progress !== "complete")}
                  className="h-14 px-8"
                >
                  {progress !== "idle" && progress !== "complete" ? (
                    <Loader2 className="h-5 w-5 animate-spin" />
                  ) : (
                    "Discover Papers"
                  )}
                </Button>
              </div>
            </div>
          </div>

          {/* Progress Indicator */}
          {progress !== "idle" && progress !== "complete" && (
            <div className="max-w-md mx-auto mb-12 animate-fade-in">
              <div className="flex items-center justify-between">
                {progressSteps.map((step, index) => (
                  <div key={step.key} className="flex items-center">
                    <div className="flex flex-col items-center">
                      <div
                        className={cn(
                          "w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium transition-all duration-300",
                          index <= getCurrentStepIndex()
                            ? "bg-beige text-navy"
                            : "bg-secondary text-muted-foreground"
                        )}
                      >
                        {index < getCurrentStepIndex() ? (
                          "✓"
                        ) : index === getCurrentStepIndex() ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          index + 1
                        )}
                      </div>
                      <span className="mt-2 text-xs text-muted-foreground text-center">
                        {step.label}
                      </span>
                    </div>
                    {index < progressSteps.length - 1 && (
                      <div
                        className={cn(
                          "w-16 h-px mx-2 transition-all duration-300",
                          index < getCurrentStepIndex()
                            ? "bg-beige"
                            : "bg-border"
                        )}
                      />
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Papers List */}
          {papers.length > 0 && (
            <div className="space-y-4 animate-slide-up">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-medium text-foreground">
                  Discovered Papers
                </h2>
                <span className="text-sm text-muted-foreground">
                  {papers.length} papers found
                </span>
              </div>

              {papers.map((paper, index) => (
                <div
                  key={paper.id}
                  className="p-6 rounded-2xl bg-card border border-border/50 shadow-premium hover:shadow-premium-lg transition-all duration-300 animate-slide-up"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-foreground mb-2 leading-snug">
                        {paper.title}
                      </h3>
                      <div className="flex items-center gap-4 mb-3 text-sm text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          {paper.year}
                        </span>
                        <span className="flex items-center gap-1">
                          <BookOpen className="h-4 w-4" />
                          {paper.venue}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground leading-relaxed line-clamp-2">
                        {paper.abstract}
                      </p>
                      <div className="mt-3 text-sm text-muted-foreground">
                        {paper.authors.join(", ")}
                      </div>
                    </div>
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="shrink-0"
                      onClick={() => paper.url && window.open(paper.url, '_blank')}
                    >
                      <ExternalLink className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </PageLayout>
  );
}
