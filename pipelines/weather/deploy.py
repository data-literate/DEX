#!/usr/bin/env python3
"""Deploy weather pipeline to Databricks."""

import json
import subprocess
import logging
import argparse
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class WeatherPipelineDeployer:
    """Deploy weather pipeline components to Databricks."""
    
    def __init__(self, config_path: str = "weather/config/job_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load job configuration."""
        try:
            with open(self.config_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise
    
    def upload_notebook(self, local_path: str, remote_path: str) -> bool:
        """Upload notebook to Databricks workspace."""
        try:
            result = subprocess.run(
                ["databricks", "workspace", "import", 
                 "--language", "python", "--overwrite",
                 local_path, remote_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info(f"✓ Uploaded {local_path} → {remote_path}")
                return True
            else:
                logger.error(f"Failed to upload {local_path}: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return False
    
    def deploy_notebooks(self) -> bool:
        """Upload all notebooks to Databricks."""
        base_path = Path(__file__).parent
        notebooks = [
            (str(base_path / "notebooks/extract_weather.py"), "/Shared/weather/extract_weather"),
            (str(base_path / "notebooks/load_weather.py"), "/Shared/weather/load_weather")
        ]
        
        success = True
        for local, remote in notebooks:
            if not self.upload_notebook(local, remote):
                success = False
        
        return success
    
    def create_job(self, job_id: str = None) -> bool:
        """Create or update job in Databricks."""
        try:
            with open(self.config_path) as f:
                config_data = json.load(f)
            
            # Create temporary config file
            temp_file = "/tmp/weather_job.json"
            with open(temp_file, "w") as f:
                json.dump(config_data, f)
            
            if job_id:
                # Update existing job
                result = subprocess.run(
                    ["databricks", "jobs", "reset", "--job-id", job_id,
                     "--json-file", temp_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                # Create new job
                result = subprocess.run(
                    ["databricks", "jobs", "create", "--json-file", temp_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            if result.returncode == 0:
                logger.info("✓ Job created/updated successfully")
                if not job_id:
                    try:
                        output = json.loads(result.stdout)
                        logger.info(f"Job ID: {output.get('job_id')}")
                    except (json.JSONDecodeError, ValueError):
                        logger.debug("Could not parse job ID from output")
                return True
            else:
                logger.error(f"Job creation failed: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Job creation error: {e}")
            return False
    
    def check_auth(self) -> bool:
        """Check Databricks authentication."""
        try:
            result = subprocess.run(
                ["databricks", "workspace", "ls", "/"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info("✓ Databricks authentication verified")
                return True
            else:
                logger.error("✗ Databricks authentication failed")
                return False
        except Exception as e:
            logger.error(f"Auth check error: {e}")
            return False
    
    def deploy_all(self, job_id: str = None) -> bool:
        """Deploy entire weather pipeline."""
        logger.info("Deploying weather pipeline...")
        logger.info("=" * 60)
        
        if not self.check_auth():
            logger.error("Cannot proceed without Databricks authentication")
            return False
        
        if not self.deploy_notebooks():
            logger.error("Failed to deploy notebooks")
            return False
        
        if not self.create_job(job_id):
            logger.error("Failed to create job")
            return False
        
        logger.info("=" * 60)
        logger.info("✓ Weather pipeline deployed successfully!")
        return True


def main() -> None:
    """Main entry point for deployment script."""
    parser = argparse.ArgumentParser(
        description="Deploy weather pipeline to Databricks"
    )
    parser.add_argument(
        "--job-id",
        help="Job ID to update (if not provided, creates new job)",
    )
    parser.add_argument(
        "--check-auth",
        action="store_true",
        help="Check Databricks authentication",
    )
    
    args = parser.parse_args()
    
    deployer = WeatherPipelineDeployer()
    
    if args.check_auth:
        deployer.check_auth()
        return
    
    deployer.deploy_all(args.job_id)


if __name__ == "__main__":
    main()
