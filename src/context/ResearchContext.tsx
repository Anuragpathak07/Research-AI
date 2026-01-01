import { createContext, useContext, useState, ReactNode, useEffect } from "react";

interface Paper {
  id: string;
  title: string;
  year: number;
  venue: string;
  abstract: string;
  authors: string[];
  url?: string;
  paper_id?: string;
}

interface Cluster {
  id: number;
  name: string;
  papers: number;
  dominantMethod: string;
  datasets: string[];
  keyPapers: string[];
  trajectoryStatus: "rising" | "stable" | "saturating" | "declining";
  momentumScore: number;
  lifecycleStage: string;
}

interface Gap {
  id: string;
  title: string;
  why: string;
  evidence: string;
  temporalViability: "future-viable" | "time-sensitive" | "likely-obsolete";
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


interface ResearchContextType {
  papers: Paper[];
  setPapers: (papers: Paper[]) => void;
  clusters: Cluster[];
  setClusters: (clusters: Cluster[]) => void;
  gaps: Gap[];
  setGaps: (gaps: Gap[]) => void;
  experiments: Experiment[];
  setExperiments: (experiments: Experiment[]) => void;
  loading: {
    papers: boolean;
    clusters: boolean;
    synthesis: boolean;
    gaps: boolean;
    experiments: boolean;
  };
  setLoading: (loading: Partial<ResearchContextType["loading"]>) => void;
}

const ResearchContext = createContext<ResearchContextType | undefined>(undefined);

export function ResearchProvider({ children }: { children: ReactNode }) {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoadingState] = useState({
    papers: false,
    clusters: false,
    synthesis: false,
    gaps: false,
    experiments: false,
  });

  const setLoading = (updates: Partial<ResearchContextType["loading"]>) => {
    setLoadingState((prev) => ({ ...prev, ...updates }));
  };

  // Debug logging
  useEffect(() => {
    console.log("Papers updated in context:", papers.length);
  }, [papers]);

  useEffect(() => {
    console.log("Clusters updated in context:", clusters.length);
  }, [clusters]);

  useEffect(() => {
    console.log("Gaps updated in context:", gaps.length);
  }, [gaps]);

  useEffect(() => {
    console.log("Experiments updated in context:", experiments.length);
  }, [experiments]);

  return (
    <ResearchContext.Provider
      value={{
        papers,
        setPapers,
        clusters,
        setClusters,
        gaps,
        setGaps,
        experiments,
        setExperiments,
        loading,
        setLoading,
      }}
    >
      {children}
    </ResearchContext.Provider>
  );
}

export function useResearch() {
  const context = useContext(ResearchContext);
  if (context === undefined) {
    throw new Error("useResearch must be used within a ResearchProvider");
  }
  return context;
}

