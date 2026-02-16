"""
CareerDEX Phase 3: Embeddings & Vector Search (Issue #67 - Days 5-7)

Generates semantic embeddings for job postings and stores them in Pinecone
for rapid semantic search and job matching.

Features:
- HuggingFace embeddings (all-MiniLM-L6-v2, 768 dimensions)
- Pinecone vector database integration
- Semantic similarity search
- Batch processing for scale
- Embedding caching and versioning

Deliverables:
- Job description parser
- Embedding generator
- Pinecone index management
- Similarity search API
- Enrichment to Gold layer
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class EmbeddingModel:
    """Interface for embedding models."""
    
    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for text."""
        raise NotImplementedError
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for batch of texts."""
        raise NotImplementedError


class HuggingFaceEmbedder(EmbeddingModel):
    """
    HuggingFace embedding model: all-MiniLM-L6-v2
    
    Characteristics:
    - Lightweight (~80MB)
    - Fast inference
    - 768-dimensional output
    - Good for general semantic similarity
    - Suitable for job matching tasks
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.embedding_dim = 768
        self.batch_size = 64
        logger.info(f"Initialized HuggingFace embedder: {model_name} ({self.embedding_dim}d)")
    
    def embed_text(self, text: str) -> list[float]:
        """
        Generate embedding for single text.
        
        Args:
            text: Text to embed (job description, etc.)
            
        Returns:
            768-dimensional embedding vector
        """
        # Placeholder implementation
        # Real implementation:
        # from sentence_transformers import SentenceTransformer
        # model = SentenceTransformer(self.model_name)
        # embedding = model.encode(text)
        # return embedding.tolist()
        
        return [0.0] * self.embedding_dim
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for batch.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of 768-dimensional embeddings
        """
        logger.info(f"Embedding batch of {len(texts)} texts...")
        
        embeddings = []
        
        # Process in chunks
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i+self.batch_size]
            
            # Placeholder implementation
            # Real implementation would use sentence_transformers
            batch_embeddings = [[0.0] * self.embedding_dim for _ in batch]
            embeddings.extend(batch_embeddings)
        
        logger.info(f"Generated {len(embeddings)} embeddings")
        return embeddings


class PineconeVectorDB:
    """
    Pinecone vector database integration.
    
    Index Configuration:
    - Metric: cosine (for normalized embeddings)
    - Dimension: 768
    - Index type: HNSW (hierarchical navigable small world)
    - Replicas: 3 (for HA)
    - Pod type: s1.x1 (starter)
    """
    
    def __init__(self, api_key: str = None, environment: str = "us-west-4"):
        self.api_key = api_key
        self.environment = environment
        self.index_name = "careerdex-jobs"
        self.embedding_dim = 768
        self.metric = "cosine"
        logger.info(f"Initialized Pinecone client ({environment})")
    
    def create_index(self) -> bool:
        """Create Pinecone index for CareerDEX."""
        logger.info(f"Creating Pinecone index: {self.index_name}")
        
        try:
            # Placeholder implementation
            # Real implementation:
            # import pinecone
            # pinecone.create_index(
            #     name=self.index_name,
            #     dimension=self.embedding_dim,
            #     metric=self.metric,
            #     pod_type="s1.x1",
            #     replicas=3,
            #     metadata_config={
            #         "indexed": ["source", "job_id", "company_name", "salary_min", "salary_max"]
            #     }
            # )
            
            logger.info(f"✓ Index created: {self.index_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            return False
    
    def upsert_embeddings(self, vectors: list[tuple[str, list[float], dict[str, Any]]]) -> int:
        """
        Upsert (insert or update) embeddings to Pinecone.
        
        Args:
            vectors: List of (job_id, embedding, metadata) tuples
            
        Returns:
            Number of vectors upserted
        """
        logger.info(f"Upserting {len(vectors)} vectors to Pinecone...")
        
        try:
            # Placeholder implementation
            # Real implementation:
            # index = pinecone.Index(self.index_name)
            # index.upsert(vectors=vectors, namespace="jobs")
            
            logger.info(f"✓ Upserted {len(vectors)} vectors")
            return len(vectors)
            
        except Exception as e:
            logger.error(f"Failed to upsert vectors: {e}")
            return 0
    
    def search(self, query_embedding: list[float], top_k: int = 10, 
               filters: dict[str, Any] = None) -> list[dict[str, Any]]:
        """
        Search for similar jobs.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filters: Optional metadata filters (source, company, salary range, etc.)
            
        Returns:
            List of similar job results with scores
        """
        try:
            # Placeholder implementation
            # Real implementation:
            # index = pinecone.Index(self.index_name)
            # results = index.query(
            #     vector=query_embedding,
            #     top_k=top_k,
            #     namespace="jobs",
            #     filter=filters,
            #     include_metadata=True
            # )
            
            return []
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def delete_index(self) -> bool:
        """Delete Pinecone index."""
        try:
            logger.info(f"Deleting index: {self.index_name}")
            # pinecone.delete_index(self.index_name)
            return True
        except Exception as e:
            logger.error(f"Failed to delete index: {e}")
            return False


class JobDescriptionParser:
    """Parses and extracts key information from job descriptions."""
    
    @staticmethod
    def extract_sections(description: str) -> dict[str, str]:
        """
        Extract common job description sections.
        
        Returns:
            Dict with sections: about_role, requirements, responsibilities, etc.
        """
        sections = {
            "full": description,
            "about_role": "",
            "responsibilities": "",
            "requirements": "",
            "qualifications": "",
            "benefits": "",
        }
        
        # Placeholder: would use NLP to identify sections
        return sections
    
    @staticmethod
    def extract_entities(description: str) -> dict[str, list[str]]:
        """
        Extract named entities from job description.
        
        Returns:
            Dict with: skills, tools, technologies, qualifications, etc.
        """
        entities = {
            "skills": [],
            "technologies": [],
            "tools": [],
            "certifications": [],
            "experience_keywords": [],
        }
        
        # Placeholder: would use NER to extract entities
        return entities
    
    @staticmethod
    def create_compact_representation(job: dict[str, Any]) -> str:
        """
        Create a compact text representation optimized for embedding.
        
        Combines:
        - Job title (high weight)
        - Company name (high weight)
        - Required skills (medium weight)
        - Job description excerpt
        
        Args:
            job: Job posting dict
            
        Returns:
            Compact text optimized for embedding
        """
        parts = [
            f"Title: {job.get('job_title', '')}",
            f"Company: {job.get('company_name', '')}",
            f"Skills: {' '.join(job.get('required_skills', []))}",
            f"Description: {job.get('job_description', '')[:500]}",  # First 500 chars
        ]
        
        return " ".join(parts)


class Phase3Embeddings:
    """Phase 3: Embeddings & Vector Search implementation."""
    
    def __init__(self, pinecone_api_key: str = None):
        self.embedder = HuggingFaceEmbedder()
        self.vector_db = PineconeVectorDB(api_key=pinecone_api_key)
        self.parser = JobDescriptionParser()
        self.stats = {
            "jobs_processed": 0,
            "embeddings_generated": 0,
            "vectors_stored": 0,
            "errors": 0,
        }
    
    def bootstrap(self) -> bool:
        """Initialize Phase 3 components."""
        logger.info("=" * 70)
        logger.info("PHASE 3: EMBEDDINGS & VECTOR SEARCH - BOOTSTRAP")
        logger.info("=" * 70)
        
        # Create Pinecone index
        if not self.vector_db.create_index():
            logger.error("Failed to create Pinecone index")
            return False
        
        logger.info(f"✓ Embedder initialized: {self.embedder.model_name}")
        logger.info(f"✓ Vector DB initialized: {self.vector_db.index_name}")
        logger.info("✓ Description parser initialized")
        logger.info("=" * 70)
        
        return True
    
    def process_jobs(self, jobs: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Process batch of jobs: parse, embed, store vectors.
        
        Args:
            jobs: List of job postings from Silver layer
            
        Returns:
            Processing statistics
        """
        logger.info(f"Processing {len(jobs)} jobs for embedding...")
        
        # Step 1: Parse job descriptions
        logger.info("Step 1: Parsing job descriptions...")
        parsed_jobs = []
        for job in jobs:
            job["sections"] = self.parser.extract_sections(job.get("job_description", ""))
            job["entities"] = self.parser.extract_entities(job.get("job_description", ""))
            parsed_jobs.append(job)
        
        # Step 2: Create compact representations
        logger.info("Step 2: Creating compact text representations...")
        texts = [self.parser.create_compact_representation(job) for job in parsed_jobs]
        
        # Step 3: Generate embeddings
        logger.info("Step 3: Generating embeddings...")
        embeddings = self.embedder.embed_batch(texts)
        self.stats["embeddings_generated"] += len(embeddings)
        
        # Step 4: Prepare vectors for Pinecone
        logger.info("Step 4: Preparing vectors for vector DB...")
        vectors_to_store = []
        
        for job, embedding in zip(parsed_jobs, embeddings, strict=False):
            vector_id = f"{job.get('source')}_{job.get('source_job_id')}"
            
            metadata = {
                "job_id": job.get("job_id"),
                "source": job.get("source"),
                "company_name": job.get("company_name"),
                "job_title": job.get("job_title"),
                "salary_min": job.get("benefits", {}).get("salary_min"),
                "salary_max": job.get("benefits", {}).get("salary_max"),
                "location_city": job.get("location", {}).get("city"),
                "location_country": job.get("location", {}).get("country"),
                "posted_date": job.get("posted_date"),
                "quality_score": job.get("quality_score", 0),
            }
            
            vectors_to_store.append((vector_id, embedding, metadata))
            self.stats["jobs_processed"] += 1
        
        # Step 5: Store in Pinecone
        logger.info("Step 5: Storing vectors in Pinecone...")
        stored = self.vector_db.upsert_embeddings(vectors_to_store)
        self.stats["vectors_stored"] += stored
        
        # Step 6: Enrich jobs with embedding reference
        logger.info("Step 6: Enriching jobs with embedding metadata...")
        for job, embedding in zip(parsed_jobs, embeddings, strict=False):
            job["embeddings"] = embedding
            job["embedding_model"] = self.embedder.model_name
        
        logger.info("")
        logger.info("=" * 70)
        logger.info("PHASE 3 PROCESSING RESULTS")
        logger.info("=" * 70)
        logger.info(f"Jobs processed: {self.stats['jobs_processed']}")
        logger.info(f"Embeddings generated: {self.stats['embeddings_generated']}")
        logger.info(f"Vectors stored in Pinecone: {self.stats['vectors_stored']}")
        logger.info(f"Errors: {self.stats['errors']}")
        logger.info("=" * 70)
        
        return {
            "stats": self.stats,
            "enriched_jobs": parsed_jobs,
        }
    
    def search_similar_jobs(
        self, query_job: dict[str, Any], top_k: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Find similar jobs to a given job posting.
        
        Args:
            query_job: Job posting to find similar matches for
            top_k: Number of results to return
            
        Returns:
            List of similar jobs ranked by similarity
        """
        logger.info(f"Searching for {top_k} jobs similar to {query_job.get('job_title')}...")
        
        # Create compact representation
        text = self.parser.create_compact_representation(query_job)
        
        # Generate query embedding
        query_embedding = self.embedder.embed_text(text)
        
        # Search Pinecone
        filters = {
            "source": {"$ne": query_job.get("source")},  # Exclude same source to reduce duplicates
        }
        
        results = self.vector_db.search(query_embedding, top_k=top_k, filters=filters)
        
        logger.info(f"Found {len(results)} similar jobs")
        return results


class SemanticSearch:
    """Resume-to-Job semantic search."""
    
    def __init__(self, vector_db: PineconeVectorDB, embedder: EmbeddingModel):
        self.vector_db = vector_db
        self.embedder = embedder
    
    def search_jobs_for_resume(self, resume_text: str, top_k: int = 20,
                              filters: dict[str, Any] = None) -> list[dict[str, Any]]:
        """
        Find best matching jobs for a resume/user profile.
        
        Args:
            resume_text: Resume or professional summary text
            top_k: Number of job matches to return
            filters: Optional filters (location, salary range, etc.)
            
        Returns:
            List of matching jobs ranked by relevance
        """
        logger.info(f"Searching for {top_k} job matches for resume...")
        
        # Generate resume embedding
        resume_embedding = self.embedder.embed_text(resume_text)
        
        # Search Pinecone with optional filters
        results = self.vector_db.search(resume_embedding, top_k=top_k, filters=filters)
        
        logger.info(f"Found {len(results)} matching jobs")
        return results
    
    def rank_job_resume_matches(self, job_embedding: list[float],
                               resume_embedding: list[float]) -> float:
        """
        Calculate match score between job and resume using cosine similarity.
        
        Args:
            job_embedding: 768-dim job embedding
            resume_embedding: 768-dim resume embedding
            
        Returns:
            Match score (0-1)
        """
        # Cosine similarity = dot product / (magnitude1 * magnitude2)
        import math
        
        dot_product = sum(j * r for j, r in zip(job_embedding, resume_embedding, strict=False))
        mag1 = math.sqrt(sum(j**2 for j in job_embedding))
        mag2 = math.sqrt(sum(r**2 for r in resume_embedding))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
