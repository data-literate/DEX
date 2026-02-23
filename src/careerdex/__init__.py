"""CareerDEX Pipeline - Job Ingestion, Matching, and Recommendation System.

**Phases:**
1. Phase 1: Foundation - Data models and schemas
2. Phase 2: Job Ingestion - Raw data collection
3. Phase 3: Embeddings - Vector representations
4. Phase 4: ML Models - Matching and ranking
5. Phase 5: API Services - REST API endpoints
6. Phase 6: Testing & Deployment - Quality assurance and production deployment

**Architecture:**
- Medallion Architecture: Bronze → Silver → Gold layers
- Dual Storage: Local Parquet + BigQuery cloud
- Real-time Processing: Async/await patterns
- ML Pipeline: scikit-learn based models

**Configuration:**
See config/ directory for pipeline-specific settings.

**Phases:**
See phases/ directory for phase implementations.
"""

__all__ = [
    "phases",
    "config",
]
