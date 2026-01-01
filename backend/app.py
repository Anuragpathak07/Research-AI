# app.py
from flask import Flask, jsonify
from flask_cors import CORS
from api.discover import discover_bp
from api.clusters import clusters_bp
from api.synthesis import synthesis_bp
from api.gaps import gaps_bp
from api.experiments import experiments_bp
from api.code import code_bp
from api.paper_generation import paper_generation_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "message": "Backend is running on port 5005"})
    
    app.register_blueprint(discover_bp, url_prefix="/api/discover")
    app.register_blueprint(clusters_bp, url_prefix="/api/clusters")
    app.register_blueprint(synthesis_bp, url_prefix="/api/synthesis")
    app.register_blueprint(gaps_bp, url_prefix="/api/gaps")
    app.register_blueprint(experiments_bp, url_prefix="/api/experiments")
    app.register_blueprint(code_bp, url_prefix="/api/code")
    app.register_blueprint(paper_generation_bp, url_prefix="/api/paper")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5005, debug=True)
