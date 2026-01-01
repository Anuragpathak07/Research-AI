import { useState, useEffect } from "react";
import { PageLayout } from "@/components/layout/PageLayout";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  AreaChart,
  Area,
} from "recharts";
import { Layers, Database, FileText, TrendingUp, TrendingDown, Minus, Clock, Activity, Loader2, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import { useResearch } from "@/context/ResearchContext";
import { Button } from "@/components/ui/button";

type TrajectoryStatus = "rising" | "stable" | "saturating" | "declining";


// Color palette based on trajectory status
const getClusterColor = (status: TrajectoryStatus, index: number) => {
  switch (status) {
    case "rising":
      return ["#10b981", "#34d399", "#6ee7b7", "#a7f3d0"][index % 4]; // Green shades
    case "stable":
      return ["#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe"][index % 4]; // Blue shades
    case "saturating":
      return ["#f59e0b", "#fbbf24", "#fcd34d", "#fde68a"][index % 4]; // Amber shades
    case "declining":
      return ["#ef4444", "#f87171", "#fca5a5", "#fecaca"][index % 4]; // Red shades
    default:
      return "#9A8B76";
  }
};

const getClusterGradient = (status: TrajectoryStatus) => {
  switch (status) {
    case "rising":
      return { from: "#10b981", to: "#34d399" };
    case "stable":
      return { from: "#3b82f6", to: "#60a5fa" };
    case "saturating":
      return { from: "#f59e0b", to: "#fbbf24" };
    case "declining":
      return { from: "#ef4444", to: "#f87171" };
    default:
      return { from: "#9A8B76", to: "#B8A892" };
  }
};

const getTrajectoryIcon = (status: TrajectoryStatus) => {
  switch (status) {
    case "rising": return TrendingUp;
    case "stable": return Minus;
    case "saturating": return Activity;
    case "declining": return TrendingDown;
  }
};

const getTrajectoryColor = (status: TrajectoryStatus) => {
  switch (status) {
    case "rising": return "text-green-600 bg-green-50";
    case "stable": return "text-blue-600 bg-blue-50";
    case "saturating": return "text-amber-600 bg-amber-50";
    case "declining": return "text-red-600 bg-red-50";
  }
};

const getTrajectoryLabel = (status: TrajectoryStatus) => {
  switch (status) {
    case "rising": return "Rising";
    case "stable": return "Stable";
    case "saturating": return "Saturating";
    case "declining": return "Declining";
  }
};

export default function Clusters() {
  const { papers, clusters, setClusters, loading, setLoading } = useResearch();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (papers.length > 0 && clusters.length === 0 && !loading.clusters) {
      fetchClusters();
    }
  }, [papers]);

  const storeClustersAutomatically = async (clustersToStore: any[]) => {
    try {
      // Silently store clusters in background - no UI feedback needed
      const response = await fetch("/api/paper/store", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          papers: papers,
          clusters: clustersToStore,
          synthesis: null,
          gaps: [],
          experiments: [],
        }),
      });

      if (!response.ok) {
        console.warn("Failed to auto-store clusters:", response.status);
        return;
      }

      const data = await response.json();
      if (data.error) {
        console.warn("Error auto-storing clusters:", data.error);
        return;
      }

      console.log("Clusters auto-stored successfully");
    } catch (error) {
      console.warn("Error auto-storing clusters:", error);
      // Don't show error to user - this is background operation
    }
  };

  const fetchClusters = async () => {
    if (papers.length === 0) {
      setError("Please discover papers first on the Discover page.");
      return;
    }

    try {
      setLoading({ clusters: true });
      setError(null);

      // Transform papers to backend format
      const papersForBackend = papers.map((p) => ({
        paper_id: p.paper_id || p.id,
        title: p.title,
        abstract: p.abstract,
        authors: p.authors,
        year: p.year,
        venue: p.venue,
        url: p.url,
      }));

      const response = await fetch("/api/clusters/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(papersForBackend),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      console.log("Clusters backend response:", data);
      
      // Check if response is an error
      if (data.error) {
        throw new Error(data.error);
      }
      
      // Ensure data is an array
      if (!Array.isArray(data)) {
        console.error("Expected array but got:", typeof data, data);
        throw new Error("Invalid response format: expected array");
      }
      
      // Transform backend response to match frontend format
      const transformedClusters = data.map((cluster: any, index: number) => {
        const clusterPapers = cluster.papers || [];
        const years = clusterPapers.map((p: any) => p.year || 2020);
        const avgYear = years.length > 0 ? years.reduce((a: number, b: number) => a + b, 0) / years.length : 2020;
        
        // Determine trajectory status based on average year and paper count
        let trajectoryStatus: "rising" | "stable" | "saturating" | "declining" = "stable";
        if (avgYear > 2022) trajectoryStatus = "rising";
        else if (cluster.paper_count > 20) trajectoryStatus = "saturating";
        else if (avgYear < 2020) trajectoryStatus = "declining";

        // Extract methods and datasets from abstracts
        const abstracts = clusterPapers.map((p: any) => (p.abstract || "").toLowerCase() + " " + (p.title || "").toLowerCase()).join(" ");
        
        // Better method extraction
        const dominantMethod = 
          abstracts.includes("quantum") ? "Quantum Computing" :
          abstracts.includes("transformer") ? "Vision Transformers" :
          abstracts.includes("adversarial") ? "Adversarial Training" :
          abstracts.includes("smoothing") ? "Randomized Smoothing" :
          abstracts.includes("circuit") ? "Quantum Circuits" :
          abstracts.includes("algorithm") ? "Quantum Algorithms" :
          abstracts.includes("error correction") ? "Error Correction" :
          "Various";
        
        const datasets: string[] = [];
        if (abstracts.includes("imagenet")) datasets.push("ImageNet");
        if (abstracts.includes("cifar")) datasets.push("CIFAR");
        if (abstracts.includes("benchmark")) datasets.push("Benchmarks");
        if (abstracts.includes("simulation")) datasets.push("Simulations");
        if (datasets.length === 0) datasets.push("Various");

        // Use key papers from backend if available, otherwise extract from cluster papers
        const keyPapers = cluster.key_papers && cluster.key_papers.length > 0
          ? cluster.key_papers
          : clusterPapers
              .sort((a: any, b: any) => (b.year || 0) - (a.year || 0))
              .slice(0, 3)
              .map((p: any) => {
                const title = p.title || "Untitled";
                const year = p.year ? ` (${p.year})` : "";
                return title.length > 60 ? title.substring(0, 60) + "..." + year : title + year;
              });

        return {
          id: parseInt(cluster.cluster_id) || index + 1,
          name: cluster.name || `Cluster ${cluster.cluster_id}`,
          papers: cluster.paper_count || clusterPapers.length,
          dominantMethod,
          datasets,
          keyPapers: keyPapers,
          trajectoryStatus,
          momentumScore: Math.min(100, Math.max(0, Math.round((avgYear - 2018) * 10 + cluster.paper_count * 2))),
          lifecycleStage: trajectoryStatus === "rising" ? "Acceleration" :
                         trajectoryStatus === "saturating" ? "Maturation" :
                         trajectoryStatus === "declining" ? "Decline" : "Growth",
          papersData: clusterPapers, // Store papers for timeline generation
        };
      });

      console.log("Transformed clusters:", transformedClusters);
      console.log("Setting clusters in context, count:", transformedClusters.length);
      setClusters(transformedClusters);
      console.log("Clusters set, checking context...");
      setLoading({ clusters: false });
      
      // Auto-store clusters for paper generation
      storeClustersAutomatically(transformedClusters);
      
      // Verify clusters were set
      setTimeout(() => {
        console.log("After setClusters - clusters count:", clusters.length);
      }, 100);
    } catch (error) {
      console.error("Error fetching clusters:", error);
      setError("Failed to fetch clusters. Please check if the backend is running.");
      setLoading({ clusters: false });
    }
  };

  // Generate meaningful chart data from actual clusters
  const distributionData = clusters.map((c, idx) => ({
    theme: c.name.length > 25 ? c.name.substring(0, 25) + '...' : c.name,
    count: c.papers,
    color: getClusterColor(c.trajectoryStatus, idx),
    status: c.trajectoryStatus,
  }));

  // Generate timeline data from actual paper years
  const timelineData = clusters.reduce((acc: any[], cluster: any) => {
    // Get actual years from papers stored in cluster
    const clusterPapers = cluster.papersData || [];
    
    // Use actual paper years if we have them
    if (clusterPapers.length > 0) {
      clusterPapers.forEach((p: any) => {
        const year = p.year;
        if (year) {
          const yearStr = year.toString();
          const existing = acc.find((d) => d.year === yearStr);
          if (existing) {
            existing.papers += 1;
            existing[cluster.trajectoryStatus] = (existing[cluster.trajectoryStatus] || 0) + 1;
          } else {
            acc.push({ 
              year: yearStr, 
              papers: 1,
              [cluster.trajectoryStatus]: 1
            });
          }
        }
      });
    } else {
      // Fallback: estimate based on momentum
      const baseYear = cluster.momentumScore > 70 ? 2022 : cluster.momentumScore > 40 ? 2020 : 2018;
      const yearStr = baseYear.toString();
      const existing = acc.find((d) => d.year === yearStr);
      if (existing) {
        existing.papers += cluster.papers;
        existing[cluster.trajectoryStatus] = (existing[cluster.trajectoryStatus] || 0) + cluster.papers;
      } else {
        acc.push({ 
          year: yearStr, 
          papers: cluster.papers,
          [cluster.trajectoryStatus]: cluster.papers
        });
      }
    }
    return acc;
  }, []).sort((a, b) => a.year.localeCompare(b.year));

  // Trajectory evolution showing momentum over time by status
  const trajectoryEvolution = clusters.length > 0 ? clusters.map((c, idx) => ({
    name: c.name.substring(0, 15) + (c.name.length > 15 ? '...' : ''),
    momentum: c.momentumScore,
    status: c.trajectoryStatus,
    color: getClusterColor(c.trajectoryStatus, idx),
  })) : [];

  // Calculate meaningful insights
  const totalPapers = clusters.reduce((sum, c) => sum + c.papers, 0);
  const risingClusters = clusters.filter(c => c.trajectoryStatus === "rising");
  const decliningClusters = clusters.filter(c => c.trajectoryStatus === "declining");
  const avgMomentum = clusters.length > 0 
    ? Math.round(clusters.reduce((sum, c) => sum + c.momentumScore, 0) / clusters.length)
    : 0;

  return (
    <PageLayout>
      <div className="min-h-screen py-24 px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="text-center mb-16 animate-fade-in">
            <h1 className="text-4xl md:text-5xl font-semibold text-foreground mb-4">
              Temporal Trajectory Analysis
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Research evolution, trajectory modeling, and momentum analysis across publication cycles.
            </p>
            {papers.length === 0 && (
              <div className="mt-6 p-4 rounded-lg bg-amber-50 border border-amber-200 flex items-center gap-3 justify-center">
                <AlertCircle className="h-5 w-5 text-amber-600" />
                <span className="text-amber-800">Please discover papers first on the Discover page.</span>
              </div>
            )}
            {papers.length > 0 && clusters.length === 0 && !loading.clusters && (
              <Button onClick={fetchClusters} className="mt-6" variant="premium">
                Generate Clusters
              </Button>
            )}
            {loading.clusters && (
              <div className="mt-6 flex items-center gap-2 justify-center">
                <Loader2 className="h-5 w-5 animate-spin" />
                <span className="text-muted-foreground">Generating clusters...</span>
              </div>
            )}
            {error && (
              <div className="mt-6 p-4 rounded-lg bg-red-50 border border-red-200 flex items-center gap-3 justify-center">
                <AlertCircle className="h-5 w-5 text-red-600" />
                <span className="text-red-800">{error}</span>
              </div>
            )}
          </div>

          {clusters.length === 0 && !loading.clusters && papers.length > 0 && (
            <div className="text-center py-12">
              <p className="text-muted-foreground">Click "Generate Clusters" to analyze your discovered papers.</p>
            </div>
          )}

          {clusters.length > 0 && (
            <>
          {/* Key Insights */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="p-6 rounded-xl bg-gradient-to-br from-green-50 to-green-100 border border-green-200">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5 text-green-600" />
                <span className="text-sm font-medium text-green-800">Rising Clusters</span>
              </div>
              <div className="text-3xl font-bold text-green-900">{risingClusters.length}</div>
              <div className="text-xs text-green-700 mt-1">
                {risingClusters.reduce((sum, c) => sum + c.papers, 0)} papers
              </div>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-red-50 to-red-100 border border-red-200">
              <div className="flex items-center gap-2 mb-2">
                <TrendingDown className="w-5 h-5 text-red-600" />
                <span className="text-sm font-medium text-red-800">Declining Clusters</span>
              </div>
              <div className="text-3xl font-bold text-red-900">{decliningClusters.length}</div>
              <div className="text-xs text-red-700 mt-1">
                {decliningClusters.reduce((sum, c) => sum + c.papers, 0)} papers
              </div>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200">
              <div className="flex items-center gap-2 mb-2">
                <Activity className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-medium text-blue-800">Avg Momentum</span>
              </div>
              <div className="text-3xl font-bold text-blue-900">{avgMomentum}</div>
              <div className="text-xs text-blue-700 mt-1">Across all clusters</div>
            </div>
            <div className="p-6 rounded-xl bg-gradient-to-br from-amber-50 to-amber-100 border border-amber-200">
              <div className="flex items-center gap-2 mb-2">
                <FileText className="w-5 h-5 text-amber-600" />
                <span className="text-sm font-medium text-amber-800">Total Papers</span>
              </div>
              <div className="text-3xl font-bold text-amber-900">{totalPapers}</div>
              <div className="text-xs text-amber-700 mt-1">Across {clusters.length} clusters</div>
            </div>
          </div>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
            {/* Trajectory Evolution Chart */}
            <div className="p-8 rounded-2xl bg-card border border-border/50 shadow-premium lg:col-span-2 animate-slide-up">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
                  <Clock className="w-5 h-5 text-white" strokeWidth={1.5} />
                </div>
                <div>
                  <h2 className="text-xl font-medium text-foreground">
                    Cluster Momentum Analysis
                  </h2>
                  <p className="text-sm text-muted-foreground">
                    Momentum scores by research direction - higher scores indicate more recent and active research
                  </p>
                </div>
              </div>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={trajectoryEvolution}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis 
                      dataKey="name" 
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 11 }}
                      angle={-45}
                      textAnchor="end"
                      height={80}
                    />
                    <YAxis 
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
                      label={{ value: 'Momentum Score', angle: -90, position: 'insideLeft', fill: 'hsl(var(--muted-foreground))' }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'hsl(var(--card))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '12px',
                      }}
                      formatter={(value: any, name: string, props: any) => [
                        `${value} (${props.payload.status})`,
                        'Momentum Score'
                      ]}
                    />
                    <Bar dataKey="momentum" radius={[8, 8, 0, 0]}>
                      {trajectoryEvolution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="flex items-center justify-center gap-6 mt-4 text-sm flex-wrap">
                {clusters.map((cluster, idx) => {
                  const color = getClusterColor(cluster.trajectoryStatus, idx);
                  return (
                    <div key={idx} className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
                      <span className="text-muted-foreground">{cluster.name.length > 20 ? cluster.name.substring(0, 20) + '...' : cluster.name}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Paper Distribution by Theme */}
            <div className="p-8 rounded-2xl bg-card border border-border/50 shadow-premium animate-slide-up">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center">
                  <Layers className="w-5 h-5 text-white" strokeWidth={1.5} />
                </div>
                <div>
                  <h2 className="text-xl font-medium text-foreground">
                    Paper Distribution by Cluster
                  </h2>
                  <p className="text-sm text-muted-foreground">
                    Number of papers per research cluster
                  </p>
                </div>
              </div>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={distributionData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis type="number" tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }} />
                    <YAxis 
                      dataKey="theme" 
                      type="category" 
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 11 }}
                      width={140}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'hsl(var(--card))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '12px',
                        boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)',
                      }}
                      formatter={(value: any, name: string, props: any) => [
                        `${value} papers (${props.payload.status})`,
                        'Paper Count'
                      ]}
                    />
                    <Bar dataKey="count" radius={[0, 8, 8, 0]}>
                      {distributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Theme Proportion */}
            <div className="p-8 rounded-2xl bg-card border border-border/50 shadow-premium animate-slide-up-delay-1">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-600 flex items-center justify-center">
                  <Database className="w-5 h-5 text-white" strokeWidth={1.5} />
                </div>
                <div>
                  <h2 className="text-xl font-medium text-foreground">
                    Cluster Proportions
                  </h2>
                  <p className="text-sm text-muted-foreground">
                    Relative distribution of papers across clusters
                  </p>
                </div>
              </div>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={distributionData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={3}
                      dataKey="count"
                      label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
                    >
                      {distributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'hsl(var(--card))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '12px',
                      }}
                      formatter={(value: any, name: string, props: any) => [
                        `${value} papers (${props.payload.status})`,
                        props.payload.theme
                      ]}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 flex flex-wrap gap-3 justify-center text-xs">
                {distributionData.map((entry, idx) => (
                  <div key={idx} className="flex items-center gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: entry.color }} />
                    <span className="text-muted-foreground">{entry.theme}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Publication Timeline */}
            {timelineData.length > 0 && (
              <div className="p-8 rounded-2xl bg-card border border-border/50 shadow-premium lg:col-span-2 animate-slide-up-delay-2">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-white" strokeWidth={1.5} />
                  </div>
                  <div>
                    <h2 className="text-xl font-medium text-foreground">
                      Research Activity Timeline
                    </h2>
                    <p className="text-sm text-muted-foreground">
                      Estimated publication distribution across time periods
                    </p>
                  </div>
                </div>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={timelineData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                      <XAxis 
                        dataKey="year" 
                        tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
                      />
                      <YAxis 
                        tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
                        label={{ value: 'Papers', angle: -90, position: 'insideLeft', fill: 'hsl(var(--muted-foreground))' }}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: 'hsl(var(--card))',
                          border: '1px solid hsl(var(--border))',
                          borderRadius: '12px',
                        }}
                      />
                      <Area 
                        type="monotone" 
                        dataKey="papers" 
                        stroke="#3b82f6" 
                        fill="#60a5fa" 
                        name="Total Papers"
                        strokeWidth={2}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}
          </div>

          {/* Cluster Cards */}
          <div className="mb-8">
            <h2 className="text-2xl font-medium text-foreground mb-2">
              Topic Clusters with Trajectory Status
            </h2>
            <p className="text-muted-foreground">
              Each cluster includes lifecycle stage and momentum scoring
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {clusters.map((cluster, index) => {
              const TrajectoryIcon = getTrajectoryIcon(cluster.trajectoryStatus);
              return (
                <div
                  key={`cluster-${index}-${cluster.id}`}
                  className="p-6 rounded-2xl bg-card border-2 shadow-premium hover:shadow-premium-lg transition-all duration-300 animate-slide-up"
                  style={{ 
                    animationDelay: `${index * 0.1}s`,
                    borderColor: getClusterColor(cluster.trajectoryStatus, index) + '40',
                    background: `linear-gradient(to bottom right, ${getClusterColor(cluster.trajectoryStatus, index)}08, transparent)`
                  }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-lg font-medium text-foreground">
                      {cluster.name}
                    </h3>
                    <span 
                      className="px-3 py-1 rounded-full text-sm font-medium text-white"
                      style={{ backgroundColor: getClusterColor(cluster.trajectoryStatus, index) }}
                    >
                      {cluster.papers} {cluster.papers === 1 ? 'paper' : 'papers'}
                    </span>
                  </div>

                  {/* Trajectory Status Badge */}
                  <div className="flex items-center gap-3 mb-4">
                    <div className={cn(
                      "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium",
                      getTrajectoryColor(cluster.trajectoryStatus)
                    )}>
                      <TrajectoryIcon className="w-3.5 h-3.5" />
                      {getTrajectoryLabel(cluster.trajectoryStatus)}
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-muted-foreground">Momentum:</span>
                      <div className="flex items-center gap-1">
                        <div className="w-16 h-1.5 bg-secondary rounded-full overflow-hidden">
                          <div 
                            className="h-full rounded-full transition-all duration-500"
                            style={{ 
                              width: `${cluster.momentumScore}%`,
                              backgroundColor: getClusterColor(cluster.trajectoryStatus, index)
                            }}
                          />
                        </div>
                        <span 
                          className="text-xs font-medium"
                          style={{ color: getClusterColor(cluster.trajectoryStatus, index) }}
                        >
                          {cluster.momentumScore}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Lifecycle Stage */}
                  <div className="mb-4 p-2 rounded-lg bg-secondary/50">
                    <div className="flex items-center gap-2 text-xs">
                      <Clock className="w-3.5 h-3.5 text-muted-foreground" />
                      <span className="text-muted-foreground">Lifecycle Stage:</span>
                      <span className="font-medium text-foreground">{cluster.lifecycleStage}</span>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center gap-2 text-sm">
                      <FileText className="w-4 h-4 text-muted-foreground" />
                      <span className="text-muted-foreground">Dominant Method:</span>
                      <span className="text-foreground font-medium">{cluster.dominantMethod}</span>
                    </div>

                    <div className="flex items-start gap-2 text-sm">
                      <Database className="w-4 h-4 text-muted-foreground mt-0.5" />
                      <span className="text-muted-foreground">Datasets:</span>
                      <div className="flex flex-wrap gap-1">
                        {cluster.datasets.map((dataset) => (
                          <span
                            key={dataset}
                            className="px-2 py-0.5 rounded-md bg-secondary text-xs text-muted-foreground"
                          >
                            {dataset}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="pt-3 border-t border-border/50">
                      <span className="text-xs text-muted-foreground mb-2 block">Key Papers:</span>
                      <div className="space-y-1.5">
                        {cluster.keyPapers.map((paper: string, idx: number) => (
                          <div key={idx} className="text-sm text-foreground leading-relaxed">
                            {idx + 1}. {paper}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
            </>
          )}
        </div>
      </div>
    </PageLayout>
  );
}
