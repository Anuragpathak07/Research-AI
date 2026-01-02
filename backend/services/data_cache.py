# services/data_cache.py
from storage.object_store import ObjectStore
import hashlib
import json
import os
import glob

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
    
    def clear_cache(self):
        """Clear all cached clusters and synthesis data"""
        try:
            cache_dir = self.object_store.base_path
            if os.path.exists(cache_dir):
                # Find all JSON files in cache directory
                pattern = os.path.join(cache_dir, "*.json")
                cache_files = glob.glob(pattern)
                
                # Remove all cache files
                for cache_file in cache_files:
                    try:
                        os.remove(cache_file)
                        print(f"Cleared cache file: {os.path.basename(cache_file)}")
                    except Exception as e:
                        print(f"Error removing cache file {cache_file}: {e}")
                
                print(f"Cache cleared: {len(cache_files)} files removed")
                return len(cache_files)
            else:
                print("Cache directory does not exist, nothing to clear")
                return 0
        except Exception as e:
            print(f"Error clearing cache: {e}")
            import traceback
            traceback.print_exc()
            return 0
    
    def get_all_data(self):
        """Get all cached data (for paper generation)"""
        # This is a simple implementation - in production, you'd want a proper DB
        # For now, we'll return the most recent cache entries
        return {
            "clusters": None,
            "synthesis": None,
            "papers": None
        }

