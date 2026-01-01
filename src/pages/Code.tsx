import { useState } from "react";
import { PageLayout } from "@/components/layout/PageLayout";
import { Button } from "@/components/ui/button";
import {
  FolderOpen,
  FileCode,
  FileText,
  Download,
  Copy,
  Check,
  ChevronRight,
  ChevronDown,
  Clock,
  TrendingUp,
  Lightbulb,
  AlertCircle,
  Loader2,
  Target,
  CheckCircle,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useResearch } from "@/context/ResearchContext";

interface FileNode {
  name: string;
  type: "file" | "folder";
  children?: FileNode[];
  content?: string;
}

const defaultProjectStructure: FileNode = {
  name: "robust-classification-experiment",
  type: "folder",
  children: [
    {
      name: "experiment.ipynb",
      type: "file",
      content: `{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Robust Image Classification Experiment\\n",
    "# Temporal Relevance: Aligned with rising deployment-oriented evaluation\\n",
    "\\n",
    "This notebook implements the proposed experiment for evaluating\\n",
    "robust models on real-world noise datasets.\\n",
    "\\n",
    "## Future-Proof Design Notes:\\n",
    "- Includes ViT models positioned for long-term dominance\\n",
    "- Benchmark selection emphasizes real-world signals\\n",
    "- Methodology extensible to future model scales"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "import torch\\n",
    "import torchvision\\n",
    "from robustbench import load_model\\n",
    "from datasets import load_nico_plus_plus\\n",
    "\\n",
    "# Load pre-trained robust models\\n",
    "# Selected for temporal relevance: includes rising architecture-based approaches\\n",
    "model_pgd = load_model('Carmon2019Unlabeled', dataset='cifar10')\\n",
    "model_vit = load_model('Singh2023Revisiting_ViT-S', dataset='imagenet')\\n",
    "\\n",
    "# Note: ViT included as architecture-based robustness shows acceleration trajectory"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Evaluation loop with future-extensible design\\n",
    "def evaluate_robustness(model, dataloader, attack=None):\\n",
    "    '''\\n",
    "    Temporal Design: Framework supports both current PGD and future attack methods.\\n",
    "    Extensible to AutoAttack and emerging evaluation standards.\\n",
    "    '''\\n",
    "    model.eval()\\n",
    "    correct = 0\\n",
    "    total = 0\\n",
    "    \\n",
    "    for images, labels in dataloader:\\n",
    "        if attack:\\n",
    "            images = attack(model, images, labels)\\n",
    "        outputs = model(images)\\n",
    "        _, predicted = outputs.max(1)\\n",
    "        correct += predicted.eq(labels).sum().item()\\n",
    "        total += labels.size(0)\\n",
    "    \\n",
    "    return 100. * correct / total"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Suggested Extensions (Aligned with Emerging Trends)\\n",
    "\\n",
    "1. **Multi-modal robustness**: Extend to vision-language models (rising trajectory)\\n",
    "2. **Efficiency metrics**: Add FLOPs/latency tracking (time-sensitive window)\\n",
    "3. **Cross-dataset evaluation**: Implement transfer robustness assessment"
   ]
  }
 ]
}`,
    },
    {
      name: "requirements.txt",
      type: "file",
      content: `# Core dependencies (stable, long-term support)
torch>=2.0.0
torchvision>=0.15.0
robustbench>=1.1
autoattack>=0.1

# Data processing
numpy>=1.24.0
pandas>=2.0.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0

# Utilities
tqdm>=4.65.0
wandb>=0.15.0

# Future-extensible: Vision Transformer support
timm>=0.9.0
transformers>=4.30.0`,
    },
    {
      name: "README.md",
      type: "file",
      content: `# Robust Image Classification Experiment

## Temporal Relevance Notes
This experiment is designed with future viability in mind:
- **Rising trajectories**: Architecture-based robustness (ViT) included
- **Stable baselines**: Adversarial training variants for comparison
- **Deployment focus**: Real-world noise datasets emphasized

## Overview
This repository contains code to evaluate state-of-the-art robust 
image classification models on real-world noise datasets.

## Future-Proof Design
- Modular architecture supports emerging model types
- Evaluation framework extensible to new benchmarks
- Metrics aligned with evolving publication standards

## Setup
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage
\`\`\`bash
jupyter notebook experiment.ipynb
\`\`\`

## Models Evaluated
- PGD-AT ResNet-50 (Madry et al., 2018) - Baseline, saturating
- Smooth ViT-B (Cohen et al., 2019) - Stable trajectory  
- Standard ViT-L baseline - Rising trajectory

## Datasets
- NICO++ (real-world context shifts) - Rising usage
- DomainNet (domain generalization) - Stable usage
- OpenImages-N (natural noise) - Emerging benchmark

## Metrics
- Clean Accuracy (standard)
- Real-world Noise Accuracy (rising importance)
- Domain Gap Score (future-relevant)
- Pareto Efficiency (emerging standard)

## Suggested Extensions
Based on temporal trajectory analysis:
1. Add multi-modal robustness evaluation (rising)
2. Include efficiency-robustness trade-off analysis (time-sensitive)
3. Extend to long-tail class distributions (underexplored)

## Citation
If you use this code, please cite:
\`\`\`bibtex
@misc{researchai2024,
  title={Real-world Robustness Evaluation},
  author={ResearchAI},
  year={2024}
}
\`\`\``,
    },
    {
      name: "src",
      type: "folder",
      children: [
        { name: "models.py", type: "file", content: "# Model loading utilities\n# Includes ViT models for future-proof evaluation" },
        { name: "datasets.py", type: "file", content: "# Dataset loading\n# Supports real-world noise datasets (rising trajectory)" },
        { name: "attacks.py", type: "file", content: "# Attack implementations\n# AutoAttack standard, extensible to emerging methods" },
        { name: "evaluate.py", type: "file", content: "# Evaluation scripts\n# Pareto efficiency metrics included" },
      ],
    },
    {
      name: "configs",
      type: "folder",
      children: [
        { name: "default.yaml", type: "file", content: "# Default config with temporal design notes" },
        { name: "imagenet.yaml", type: "file", content: "# ImageNet config for scale evaluation" },
        { name: "future_extensions.yaml", type: "file", content: "# Placeholder configs for emerging benchmarks" },
      ],
    },
  ],
};

export default function Code() {
  const { experiments } = useResearch();
  const [selectedFile, setSelectedFile] = useState<FileNode | null>(null);
  const [expandedFolders, setExpandedFolders] = useState<string[]>([]);
  const [copied, setCopied] = useState(false);
  const [codeGenerated, setCodeGenerated] = useState(false);
  const [generatedStructure, setGeneratedStructure] = useState<FileNode | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const toggleFolder = (name: string) => {
    setExpandedFolders((prev) =>
      prev.includes(name) ? prev.filter((f) => f !== name) : [...prev, name]
    );
  };

  const handleCopy = async () => {
    if (selectedFile?.content) {
      await navigator.clipboard.writeText(selectedFile.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const generateCode = async () => {
    if (experiments.length === 0) {
      setError("Please generate experiments first on the Gaps page.");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await fetch("/api/code/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(experiments),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setGeneratedStructure(data);
      setCodeGenerated(true);
      setExpandedFolders([data.name]);
      setSelectedFile(data.children?.[0] || null);
      setLoading(false);
    } catch (error) {
      console.error("Error generating code:", error);
      setError("Failed to generate code. Please check if the backend is running.");
      setLoading(false);
    }
  };

  const countFiles = (node: FileNode): number => {
    if (node.type === "file") return 1;
    if (!node.children) return 0;
    return node.children.reduce((sum, child) => sum + countFiles(child), 0);
  };

  const renderFileTree = (node: FileNode, depth = 0) => {
    const isExpanded = expandedFolders.includes(node.name);
    const isSelected = selectedFile?.name === node.name;

    return (
      <div key={node.name}>
        <button
          onClick={() => {
            if (node.type === "folder") {
              toggleFolder(node.name);
            } else {
              setSelectedFile(node);
            }
          }}
          className={cn(
            "w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors",
            isSelected
              ? "bg-beige-light text-foreground"
              : "text-muted-foreground hover:bg-secondary hover:text-foreground"
          )}
          style={{ paddingLeft: `${depth * 16 + 12}px` }}
        >
          {node.type === "folder" ? (
            <>
              {isExpanded ? (
                <ChevronDown className="w-4 h-4 shrink-0" />
              ) : (
                <ChevronRight className="w-4 h-4 shrink-0" />
              )}
              <FolderOpen className="w-4 h-4 shrink-0 text-beige-dark" />
            </>
          ) : (
            <>
              <span className="w-4" />
              {node.name.endsWith(".ipynb") ? (
                <FileCode className="w-4 h-4 shrink-0 text-beige-dark" />
              ) : (
                <FileText className="w-4 h-4 shrink-0 text-muted-foreground" />
              )}
            </>
          )}
          <span className="truncate">{node.name}</span>
        </button>
        {node.type === "folder" && isExpanded && node.children && (
          <div>
            {node.children.map((child) => renderFileTree(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <PageLayout>
      <div className="min-h-screen py-24 px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12 animate-fade-in">
            <h1 className="text-4xl md:text-5xl font-semibold text-foreground mb-4">
              Future-Proof Code Generation
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Experiment code with temporal relevance notes and extensibility design.
            </p>
          </div>

          {experiments.length === 0 && (
            <div className="mb-8 p-6 rounded-xl bg-amber-50 border border-amber-200 flex items-center gap-3 justify-center">
              <AlertCircle className="h-5 w-5 text-amber-600" />
              <span className="text-amber-800">Please generate experiments first on the Gaps page.</span>
            </div>
          )}

          {experiments.length > 0 && !codeGenerated && (
            <div className="mb-8 p-6 rounded-xl bg-secondary/30 border border-border/50 text-center animate-slide-up">
              <Lightbulb className="w-12 h-12 text-beige-dark mx-auto mb-4" />
              <h3 className="text-lg font-medium text-foreground mb-2">Generate Experiment Code</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Generate code structure and implementation files for your proposed experiments.
              </p>
              <Button 
                onClick={generateCode} 
                variant="premium" 
                size="lg" 
                className="gap-2"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Generating Code...
                  </>
                ) : (
                  <>
                    <FileCode className="h-5 w-5" />
                    Generate Code
                  </>
                )}
              </Button>
              {error && (
                <div className="mt-4 p-3 rounded-lg bg-red-50 border border-red-200 text-red-800 text-sm">
                  {error}
                </div>
              )}
            </div>
          )}

          {codeGenerated && (
            <>
              {/* Download Actions */}
              <div className="flex items-center justify-center gap-4 mb-8 animate-slide-up">
                <Button variant="premium" size="lg" className="gap-2">
                  <Download className="h-5 w-5" />
                  Download Notebook
                </Button>
                <Button variant="outline" size="lg" className="gap-2">
                  <Download className="h-5 w-5" />
                  Download Project ZIP
                </Button>
              </div>

              {/* Code Viewer */}
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 animate-slide-up-delay-1">
                {/* File Tree */}
                <div className="lg:col-span-1 p-4 rounded-2xl bg-card border border-border/50 shadow-premium">
                  <h3 className="text-sm font-medium text-muted-foreground mb-3 px-3">
                    Project Files
                  </h3>
                  <div className="space-y-1">
                    {generatedStructure && renderFileTree(generatedStructure)}
                  </div>
                </div>

            {/* Code Preview */}
            <div className="lg:col-span-3 rounded-2xl bg-card border border-border/50 shadow-premium overflow-hidden">
              {/* File Header */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-border/50 bg-secondary/30">
                <div className="flex items-center gap-2">
                  <FileCode className="w-4 h-4 text-beige-dark" />
                  <span className="text-sm font-medium text-foreground">
                    {selectedFile?.name || "Select a file"}
                  </span>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleCopy}
                  className="gap-2"
                  disabled={!selectedFile?.content}
                >
                  {copied ? (
                    <Check className="h-4 w-4" />
                  ) : (
                    <Copy className="h-4 w-4" />
                  )}
                  {copied ? "Copied" : "Copy"}
                </Button>
              </div>

              {/* Code Content */}
              <div className="p-6 overflow-auto max-h-[600px]">
                <pre className="text-sm text-muted-foreground font-mono whitespace-pre-wrap leading-relaxed">
                  {selectedFile?.content || "Select a file to view its contents."}
                </pre>
              </div>
            </div>
          </div>

              {/* Quick Stats */}
              {generatedStructure && (
                <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4 animate-slide-up-delay-2">
                  {[
                    { label: "Files Generated", value: String(countFiles(generatedStructure)), icon: FileCode },
                    { label: "Experiments", value: String(experiments.length), icon: Target },
                    { label: "Project Ready", value: "Yes", icon: CheckCircle },
                    { label: "Future Extensions", value: "Included", icon: TrendingUp },
                  ].map((stat) => (
                    <div
                      key={stat.label}
                      className="p-4 rounded-xl bg-card border border-border/50 text-center"
                    >
                      <div className="flex items-center justify-center gap-2 mb-1">
                        <stat.icon className="w-4 h-4 text-beige-dark" />
                        <span className="text-2xl font-semibold text-beige-dark">
                          {stat.value}
                        </span>
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {stat.label}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </PageLayout>
  );
}
