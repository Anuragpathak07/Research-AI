import { useState, useEffect } from "react";
import { PageLayout } from "@/components/layout/PageLayout";
import { Button } from "@/components/ui/button";
import { ChevronDown, ChevronRight, Copy, Download, Check, Clock, TrendingUp, TrendingDown, ArrowRight, Loader2, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import { useResearch } from "@/context/ResearchContext";

interface Section {
  id: string;
  title: string;
  content: string;
}

interface SynthesisData {
  sections?: {
    methods?: { title: string; content: string };
    datasets?: { title: string; content: string };
    metrics?: { title: string; content: string };
    performance?: { title: string; content: string };
    method_transitions?: { title: string; content: string };
    dataset_shifts?: { title: string; content: string };
    metric_deprecations?: { title: string; content: string };
  };
  statistics?: {
    papers_analyzed?: number;
    year_range?: { start?: number; end?: number };
    top_methods?: Record<string, number>;
    top_datasets?: Record<string, number>;
    top_metrics?: Record<string, number>;
  };
}

export default function Synthesis() {
  const [expandedSections, setExpandedSections] = useState<string[]>(["methods", "method_transitions"]);
  const [copied, setCopied] = useState(false);
  const { papers, loading, setLoading } = useResearch();
  const [synthesisData, setSynthesisData] = useState<SynthesisData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | null>(null);

  useEffect(() => {
    if (papers.length > 0 && !synthesisData && !loading.synthesis) {
      fetchSynthesis();
    }
  }, [papers]);

  const fetchSynthesis = async () => {
    if (papers.length === 0) {
      setError("Please discover papers first on the Discover page.");
      return;
    }

    try {
      setLoading({ synthesis: true });
      setError(null);

      const papersForBackend = papers.map((p) => ({
        paper_id: p.paper_id || p.id,
        title: p.title,
        abstract: p.abstract,
        authors: p.authors,
        year: p.year,
        venue: p.venue,
        url: p.url,
      }));

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 180000); // 3 minute timeout
      
      const response = await fetch("/api/synthesis/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(papersForBackend),
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      setSynthesisData(data);
      setLoading({ synthesis: false });
      
      if (data.warning) {
        setWarning(data.warning);
      } else {
        setWarning(null);
      }
    } catch (error: any) {
      console.error("Error fetching synthesis:", error);
      if (error.name === 'AbortError') {
        setError("Synthesis request timed out. The analysis is taking longer than expected. Please try again or check if Ollama is running properly.");
      } else {
        setError("Failed to fetch synthesis. Please check if the backend is running.");
      }
      setLoading({ synthesis: false });
    }
  };

  const toggleSection = (id: string) => {
    setExpandedSections((prev) =>
      prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id]
    );
  };

  const handleCopy = async () => {
    if (!synthesisData?.sections) return;
    
    const sections = Object.values(synthesisData.sections);
    const fullText = sections
      .map((s) => `## ${s.title}\n\n${s.content}`)
      .join("\n\n");
    await navigator.clipboard.writeText(fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderContent = (content: string) => {
    return content.split("**").map((part, index) =>
      index % 2 === 1 ? (
        <strong key={index} className="font-semibold text-foreground">
          {part}
        </strong>
      ) : (
        part
      )
    );
  };

  return (
    <PageLayout>
      <div className="min-h-screen py-24 px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12 animate-fade-in">
            <h1 className="text-4xl md:text-5xl font-semibold text-foreground mb-4">
              Temporal Literature Synthesis
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              AI-generated longitudinal analysis with field evolution tracking.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-3 mb-8 animate-slide-up">
            <Button
              variant="outline"
              size="sm"
              onClick={handleCopy}
              className="gap-2"
            >
              {copied ? (
                <Check className="h-4 w-4" />
              ) : (
                <Copy className="h-4 w-4" />
              )}
              {copied ? "Copied" : "Copy All"}
            </Button>
            <Button variant="outline" size="sm" className="gap-2">
              <Download className="h-4 w-4" />
              Export PDF
            </Button>
          </div>

          {papers.length === 0 && (
            <div className="text-center py-12 p-4 rounded-lg bg-amber-50 border border-amber-200 flex items-center gap-3 justify-center">
              <AlertCircle className="h-5 w-5 text-amber-600" />
              <span className="text-amber-800">Please discover papers first on the Discover page.</span>
            </div>
          )}

          {papers.length > 0 && !synthesisData && !loading.synthesis && (
            <div className="text-center py-12">
              <Button onClick={fetchSynthesis} variant="premium" className="gap-2">
                Generate Synthesis
              </Button>
            </div>
          )}

          {loading.synthesis && (
            <div className="text-center py-12 flex items-center gap-2 justify-center">
              <Loader2 className="h-5 w-5 animate-spin" />
              <span className="text-muted-foreground">Generating synthesis content...</span>
            </div>
          )}

          {error && (
            <div className="p-4 rounded-lg bg-red-50 border border-red-200 flex items-center gap-3 justify-center mb-8">
              <AlertCircle className="h-5 w-5 text-red-600" />
              <span className="text-red-800">{error}</span>
            </div>
          )}
          {warning && (
            <div className="p-4 rounded-lg bg-amber-50 border border-amber-200 flex items-center gap-3 justify-center mb-8">
              <AlertCircle className="h-5 w-5 text-amber-600" />
              <span className="text-amber-800">{warning}</span>
            </div>
          )}

          {synthesisData?.sections && (
            <>
              {/* Synthesis Card */}
              <div className="rounded-2xl bg-card border border-border/50 shadow-premium overflow-hidden animate-slide-up mb-8">
                <div className="p-6 border-b border-border/50 bg-secondary/30">
                  <h2 className="text-xl font-medium text-foreground">
                    Structured Literature Review
                  </h2>
                  <p className="text-sm text-muted-foreground mt-1">
                    {synthesisData.statistics?.papers_analyzed || papers.length} papers analyzed
                    {synthesisData.statistics?.year_range?.start && synthesisData.statistics?.year_range?.end && 
                      ` • ${synthesisData.statistics.year_range.start}-${synthesisData.statistics.year_range.end}`
                    }
                  </p>
                </div>

                <div className="divide-y divide-border/50">
                  {synthesisData.sections.methods && (
                    <div className="animate-fade-in">
                      <button
                        onClick={() => toggleSection("methods")}
                        className="w-full px-6 py-4 flex items-center justify-between hover:bg-secondary/30 transition-colors"
                      >
                        <span className="text-base font-medium text-foreground">
                          {synthesisData.sections.methods.title}
                        </span>
                        {expandedSections.includes("methods") ? (
                          <ChevronDown className="h-5 w-5 text-muted-foreground" />
                        ) : (
                          <ChevronRight className="h-5 w-5 text-muted-foreground" />
                        )}
                      </button>
                      <div
                        className={cn(
                          "overflow-hidden transition-all duration-300",
                          expandedSections.includes("methods")
                            ? "max-h-[2000px] opacity-100"
                            : "max-h-0 opacity-0"
                        )}
                      >
                        <div className="px-6 pb-6">
                          <div className="prose prose-sm max-w-none">
                            <p className="text-muted-foreground leading-relaxed whitespace-pre-line">
                              {renderContent(synthesisData.sections.methods.content)}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {synthesisData.sections.datasets && (
                    <div className="animate-fade-in">
                      <button
                        onClick={() => toggleSection("datasets")}
                        className="w-full px-6 py-4 flex items-center justify-between hover:bg-secondary/30 transition-colors"
                      >
                        <span className="text-base font-medium text-foreground">
                          {synthesisData.sections.datasets.title}
                        </span>
                        {expandedSections.includes("datasets") ? (
                          <ChevronDown className="h-5 w-5 text-muted-foreground" />
                        ) : (
                          <ChevronRight className="h-5 w-5 text-muted-foreground" />
                        )}
                      </button>
                      <div
                        className={cn(
                          "overflow-hidden transition-all duration-300",
                          expandedSections.includes("datasets")
                            ? "max-h-[2000px] opacity-100"
                            : "max-h-0 opacity-0"
                        )}
                      >
                        <div className="px-6 pb-6">
                          <div className="prose prose-sm max-w-none">
                            <p className="text-muted-foreground leading-relaxed whitespace-pre-line">
                              {renderContent(synthesisData.sections.datasets.content)}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {synthesisData.sections.metrics && (
                    <div className="animate-fade-in">
                      <button
                        onClick={() => toggleSection("metrics")}
                        className="w-full px-6 py-4 flex items-center justify-between hover:bg-secondary/30 transition-colors"
                      >
                        <span className="text-base font-medium text-foreground">
                          {synthesisData.sections.metrics.title}
                        </span>
                        {expandedSections.includes("metrics") ? (
                          <ChevronDown className="h-5 w-5 text-muted-foreground" />
                        ) : (
                          <ChevronRight className="h-5 w-5 text-muted-foreground" />
                        )}
                      </button>
                      <div
                        className={cn(
                          "overflow-hidden transition-all duration-300",
                          expandedSections.includes("metrics")
                            ? "max-h-[2000px] opacity-100"
                            : "max-h-0 opacity-0"
                        )}
                      >
                        <div className="px-6 pb-6">
                          <div className="prose prose-sm max-w-none">
                            <p className="text-muted-foreground leading-relaxed whitespace-pre-line">
                              {renderContent(synthesisData.sections.metrics.content)}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {synthesisData.sections.performance && (
                    <div className="animate-fade-in">
                      <button
                        onClick={() => toggleSection("performance")}
                        className="w-full px-6 py-4 flex items-center justify-between hover:bg-secondary/30 transition-colors"
                      >
                        <span className="text-base font-medium text-foreground">
                          {synthesisData.sections.performance.title}
                        </span>
                        {expandedSections.includes("performance") ? (
                          <ChevronDown className="h-5 w-5 text-muted-foreground" />
                        ) : (
                          <ChevronRight className="h-5 w-5 text-muted-foreground" />
                        )}
                      </button>
                      <div
                        className={cn(
                          "overflow-hidden transition-all duration-300",
                          expandedSections.includes("performance")
                            ? "max-h-[2000px] opacity-100"
                            : "max-h-0 opacity-0"
                        )}
                      >
                        <div className="px-6 pb-6">
                          <div className="prose prose-sm max-w-none">
                            <p className="text-muted-foreground leading-relaxed whitespace-pre-line">
                              {renderContent(synthesisData.sections.performance.content)}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Evolution of the Field */}
              {synthesisData.sections.method_transitions || synthesisData.sections.dataset_shifts || synthesisData.sections.metric_deprecations ? (
                <div className="rounded-2xl bg-card border border-beige/30 shadow-premium overflow-hidden animate-slide-up-delay-1 mb-8">
                  <div className="p-6 border-b border-border/50 bg-beige-light/30">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-beige flex items-center justify-center">
                        <Clock className="w-5 h-5 text-navy" strokeWidth={1.5} />
                      </div>
                      <div>
                        <h2 className="text-xl font-medium text-foreground">
                          Evolution of the Field
                        </h2>
                        <p className="text-sm text-muted-foreground mt-0.5">
                          Temporal analysis: How the field evolved, what peaked, and what's accelerating
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="divide-y divide-border/50">
                    {synthesisData.sections.method_transitions && (
                      <div className="animate-fade-in">
                        <button
                          onClick={() => toggleSection("method_transitions")}
                          className="w-full px-6 py-4 flex items-center justify-between hover:bg-beige-light/20 transition-colors"
                        >
                          <div className="flex items-center gap-3">
                            <ArrowRight className="w-4 h-4 text-beige-dark" />
                            <span className="text-base font-medium text-foreground">
                              {synthesisData.sections.method_transitions.title}
                            </span>
                          </div>
                          {expandedSections.includes("method_transitions") ? (
                            <ChevronDown className="h-5 w-5 text-muted-foreground" />
                          ) : (
                            <ChevronRight className="h-5 w-5 text-muted-foreground" />
                          )}
                        </button>
                        <div
                          className={cn(
                            "overflow-hidden transition-all duration-300",
                            expandedSections.includes("method_transitions")
                              ? "max-h-[2000px] opacity-100"
                              : "max-h-0 opacity-0"
                          )}
                        >
                          <div className="px-6 pb-6">
                            <div className="prose prose-sm max-w-none">
                              <p className="text-muted-foreground leading-relaxed whitespace-pre-line">
                                {renderContent(synthesisData.sections.method_transitions.content)}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {synthesisData.sections.dataset_shifts && (
                      <div className="animate-fade-in">
                        <button
                          onClick={() => toggleSection("dataset_shifts")}
                          className="w-full px-6 py-4 flex items-center justify-between hover:bg-beige-light/20 transition-colors"
                        >
                          <div className="flex items-center gap-3">
                            <TrendingUp className="w-4 h-4 text-beige-dark" />
                            <span className="text-base font-medium text-foreground">
                              {synthesisData.sections.dataset_shifts.title}
                            </span>
                          </div>
                          {expandedSections.includes("dataset_shifts") ? (
                            <ChevronDown className="h-5 w-5 text-muted-foreground" />
                          ) : (
                            <ChevronRight className="h-5 w-5 text-muted-foreground" />
                          )}
                        </button>
                        <div
                          className={cn(
                            "overflow-hidden transition-all duration-300",
                            expandedSections.includes("dataset_shifts")
                              ? "max-h-[2000px] opacity-100"
                              : "max-h-0 opacity-0"
                          )}
                        >
                          <div className="px-6 pb-6">
                            <div className="prose prose-sm max-w-none">
                              <p className="text-muted-foreground leading-relaxed whitespace-pre-line">
                                {renderContent(synthesisData.sections.dataset_shifts.content)}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {synthesisData.sections.metric_deprecations && (
                      <div className="animate-fade-in">
                        <button
                          onClick={() => toggleSection("metric_deprecations")}
                          className="w-full px-6 py-4 flex items-center justify-between hover:bg-beige-light/20 transition-colors"
                        >
                          <div className="flex items-center gap-3">
                            <TrendingDown className="w-4 h-4 text-beige-dark" />
                            <span className="text-base font-medium text-foreground">
                              {synthesisData.sections.metric_deprecations.title}
                            </span>
                          </div>
                          {expandedSections.includes("metric_deprecations") ? (
                            <ChevronDown className="h-5 w-5 text-muted-foreground" />
                          ) : (
                            <ChevronRight className="h-5 w-5 text-muted-foreground" />
                          )}
                        </button>
                        <div
                          className={cn(
                            "overflow-hidden transition-all duration-300",
                            expandedSections.includes("metric_deprecations")
                              ? "max-h-[2000px] opacity-100"
                              : "max-h-0 opacity-0"
                          )}
                        >
                          <div className="px-6 pb-6">
                            <div className="prose prose-sm max-w-none">
                              <p className="text-muted-foreground leading-relaxed whitespace-pre-line">
                                {renderContent(synthesisData.sections.metric_deprecations.content)}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ) : null}
            </>
          )}

          {/* Summary Stats */}
          {synthesisData?.statistics && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 animate-slide-up-delay-2">
              <div className="p-4 rounded-xl bg-card border border-border/50 text-center">
                <div className="text-2xl font-semibold text-beige-dark">
                  {synthesisData.statistics.papers_analyzed || papers.length}
                </div>
                <div className="text-xs text-muted-foreground mt-1">
                  Papers Analyzed
                </div>
              </div>
              {synthesisData.statistics.year_range?.start && synthesisData.statistics.year_range?.end && (
                <div className="p-4 rounded-xl bg-card border border-border/50 text-center">
                  <div className="text-2xl font-semibold text-beige-dark">
                    {synthesisData.statistics.year_range.end - synthesisData.statistics.year_range.start + 1}
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">
                    Years Covered
                  </div>
                </div>
              )}
              {synthesisData.statistics.top_methods && Object.keys(synthesisData.statistics.top_methods).length > 0 && (
                <div className="p-4 rounded-xl bg-card border border-border/50 text-center">
                  <div className="text-2xl font-semibold text-beige-dark">
                    {Object.keys(synthesisData.statistics.top_methods).length}
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">
                    Method Categories
                  </div>
                </div>
              )}
              {synthesisData.statistics.top_datasets && Object.keys(synthesisData.statistics.top_datasets).length > 0 && (
                <div className="p-4 rounded-xl bg-card border border-border/50 text-center">
                  <div className="text-2xl font-semibold text-beige-dark">
                    {Object.keys(synthesisData.statistics.top_datasets).length}
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">
                    Datasets Used
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </PageLayout>
  );
}
