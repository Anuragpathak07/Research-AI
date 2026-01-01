# services/clustering_service.py
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_distances

class ClusteringService:
    def cluster(self, embeddings, k=4):
        model = KMeans(n_clusters=k, random_state=42)
        labels = model.fit_predict(embeddings)
        return labels, model.cluster_centers_

    def intra_cluster_distance(self, embeddings, labels):
        distances = {}
        for label in set(labels):
            cluster_points = embeddings[labels == label]
            distances[label] = cosine_distances(cluster_points).mean()
        return distances
