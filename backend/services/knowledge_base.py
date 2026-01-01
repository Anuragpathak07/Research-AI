# services/knowledge_base.py
from storage.vector_store import VectorStore
from services.embedding_service import EmbeddingService
import json

class KnowledgeBase:
    def __init__(self):
        self.vector_store = VectorStore(dim=384)
        self.embedding_service = EmbeddingService()
        self.is_initialized = False
        self.content_storage = {}  # Store full content by (type, id)
        
    def build_knowledge_base(self, papers, clusters=None, synthesis=None, gaps=None, experiments=None):
        """Build knowledge base from all available data"""
        texts = []
        metadata = []
        
        # Add papers
        for paper in papers:
            paper_id = paper.get("paper_id") or paper.get("id")
            text = f"Title: {paper.get('title', '')}\nAbstract: {paper.get('abstract', '')}\n"
            if paper.get('authors'):
                text += f"Authors: {', '.join(paper.get('authors', []))}\n"
            if paper.get('year'):
                text += f"Year: {paper.get('year', '')}\n"
            if paper.get('venue'):
                text += f"Venue: {paper.get('venue', '')}\n"
            
            texts.append(text)
            metadata.append({
                "type": "paper",
                "id": paper_id,
                "title": paper.get("title", ""),
                "source": "discovered_papers"
            })
            # Store full content
            self.content_storage[("paper", paper_id)] = {
                "title": paper.get("title", ""),
                "abstract": paper.get("abstract", ""),
                "authors": paper.get("authors", []),
                "year": paper.get("year"),
                "venue": paper.get("venue", "")
            }
        
        # Add clusters
        if clusters:
            for cluster in clusters:
                cluster_id = cluster.get("cluster_id") or str(cluster.get("id", ""))
                if not cluster_id:
                    continue  # Skip clusters without ID
                    
                cluster_text = f"Cluster: {cluster.get('name', '')}\n"
                cluster_text += f"Papers: {cluster.get('paper_count', cluster.get('papers', 0))}\n"
                cluster_text += f"Trajectory: {cluster.get('trajectory', cluster.get('trajectoryStatus', ''))}\n"
                key_papers = cluster.get('key_papers') or cluster.get('keyPapers', [])
                if key_papers:
                    cluster_text += f"Key Papers: {', '.join(key_papers) if isinstance(key_papers, list) else str(key_papers)}\n"
                
                texts.append(cluster_text)
                metadata.append({
                    "type": "cluster",
                    "id": str(cluster_id),
                    "name": cluster.get("name", ""),
                    "source": "clusters"
                })
                # Store full content
                self.content_storage[("cluster", str(cluster_id))] = {
                    "name": cluster.get("name", ""),
                    "papers": cluster.get("papers", []),
                    "key_papers": key_papers
                }
        
        # Add synthesis content
        if synthesis and synthesis.get("sections"):
            for section_key, section_data in synthesis["sections"].items():
                if section_data.get("content"):
                    text = f"Section: {section_data.get('title', section_key)}\n"
                    text += f"Content: {section_data.get('content', '')}\n"
                    
                    texts.append(text)
                    metadata.append({
                        "type": "synthesis",
                        "id": section_key,
                        "title": section_data.get("title", ""),
                        "source": "synthesis"
                    })
                    # Store full content
                    self.content_storage[("synthesis", section_key)] = {
                        "title": section_data.get("title", ""),
                        "content": section_data.get("content", "")
                    }
        
        # Add gaps
        if gaps:
            for gap in gaps:
                gap_id = gap.get("id")
                gap_text = f"Research Gap: {gap.get('title', gap.get('gap', ''))}\n"
                gap_text += f"Why: {gap.get('why', gap.get('reason', ''))}\n"
                gap_text += f"Evidence: {gap.get('evidence', '')}\n"
                gap_text += f"Viability: {gap.get('temporalViability', gap.get('viability', ''))}\n"
                
                texts.append(gap_text)
                metadata.append({
                    "type": "gap",
                    "id": gap_id,
                    "title": gap.get("title") or gap.get("gap", ""),
                    "source": "gaps"
                })
                # Store full content
                self.content_storage[("gap", gap_id)] = {
                    "title": gap.get("title") or gap.get("gap", ""),
                    "why": gap.get("why") or gap.get("reason", ""),
                    "evidence": gap.get("evidence", "")
                }
        
        # Add experiments
        if experiments:
            for exp in experiments:
                exp_id = exp.get("id")
                exp_text = f"Experiment: {exp.get('objective', '')}\n"
                exp_text += f"Dataset: {exp.get('dataset', '')}\n"
                if exp.get('models'):
                    exp_text += f"Models: {', '.join(exp.get('models', []))}\n"
                if exp.get('metrics'):
                    exp_text += f"Metrics: {', '.join(exp.get('metrics', []))}\n"
                exp_text += f"Outcome: {exp.get('outcome', '')}\n"
                
                texts.append(exp_text)
                metadata.append({
                    "type": "experiment",
                    "id": exp_id,
                    "title": exp.get("objective", ""),
                    "source": "experiments"
                })
                # Store full content
                self.content_storage[("experiment", exp_id)] = {
                    "objective": exp.get("objective", ""),
                    "dataset": exp.get("dataset", ""),
                    "models": exp.get("models", []),
                    "metrics": exp.get("metrics", [])
                }
        
        if not texts:
            return 0
        
        # Generate embeddings
        try:
            embeddings = self.embedding_service.embed_texts(texts)
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return 0
        
        # Add to vector store
        try:
            self.vector_store = VectorStore(dim=384)  # Reset
            self.vector_store.add(embeddings, metadata)
            self.is_initialized = True
        except Exception as e:
            print(f"Error adding to vector store: {e}")
            return 0
        
        return len(texts)
    
    def search(self, query, k=10):
        """Search knowledge base for relevant content"""
        if not self.is_initialized:
            return []
        
        query_embedding = self.embedding_service.embed_texts([query])[0]
        results = self.vector_store.search(query_embedding, k=k)
        return results
    
    def get_full_content(self, papers, clusters, synthesis, gaps, experiments):
        """Get full content for retrieved metadata - uses stored content"""
        # Return the stored content map
        return self.content_storage
    
    def get_context_for_paper_generation(self, topic, max_chunks=15):
        """Get relevant context for paper generation"""
        # Search for relevant content
        search_results = self.search(topic, k=max_chunks)
        
        # Organize by type
        context = {
            "papers": [],
            "synthesis": [],
            "gaps": [],
            "experiments": [],
            "clusters": []
        }
        
        for result in search_results:
            result_type = result.get("type", "")
            if result_type == "paper":
                context["papers"].append(result)
            elif result_type == "synthesis":
                context["synthesis"].append(result)
            elif result_type == "gap":
                context["gaps"].append(result)
            elif result_type == "experiment":
                context["experiments"].append(result)
            elif result_type == "cluster":
                context["clusters"].append(result)
        
        return context

