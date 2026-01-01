# services/data_cache.py
from storage.object_store import ObjectStore
import hashlib
import json

class DataCache:
    """Cache for generated data to avoid regeneration"""
    
    def __init__(self):
        self.object_store = ObjectStore(base_path="data_cache")
    
    def _get_hash(self, data):
        """Generate hash from data for cache key"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get_clusters(self, papers):
        """Get cached clusters for given papers"""
        cache_key = f"clusters_{self._get_hash(papers)}"
        return self.object_store.load_json(cache_key)
    
    def save_clusters(self, papers, clusters):
        """Save clusters to cache"""
        cache_key = f"clusters_{self._get_hash(papers)}"
        self.object_store.save_json(cache_key, {
            "papers": papers,
            "clusters": clusters
        })
        return cache_key
    
    def get_synthesis(self, papers):
        """Get cached synthesis for given papers"""
        cache_key = f"synthesis_{self._get_hash(papers)}"
        return self.object_store.load_json(cache_key)
    
    def save_synthesis(self, papers, synthesis):
        """Save synthesis to cache"""
        cache_key = f"synthesis_{self._get_hash(papers)}"
        self.object_store.save_json(cache_key, {
            "papers": papers,
            "synthesis": synthesis
        })
        return cache_key
    
    def get_all_data(self):
        """Get all cached data (for paper generation)"""
        # This is a simple implementation - in production, you'd want a proper DB
        # For now, we'll return the most recent cache entries
        return {
            "clusters": None,
            "synthesis": None,
            "papers": None
        }

