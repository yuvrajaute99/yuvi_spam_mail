"""
Cloud storage module for uploading prediction data to Azure Blob Storage.

This module provides functionality to store prediction history and statistics
in Azure Blob Storage for persistence and analysis.
"""

import os
import json
import logging
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceExistsError, AzureError

logger = logging.getLogger(__name__)

# Azure configuration - these should be set as environment variables
AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "spam-detector-data")

class CloudStorage:
    """Handles cloud storage operations for spam detector data."""

    def __init__(self):
        self.blob_service_client = None
        self.container_name = AZURE_STORAGE_CONTAINER_NAME

        if AZURE_STORAGE_ACCOUNT_NAME:
            try:
                account_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
                credential = DefaultAzureCredential()
                self.blob_service_client = BlobServiceClient(
                    account_url=account_url,
                    credential=credential
                )
                self._ensure_container_exists()
                logger.info("Azure Blob Storage client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Azure Blob Storage: {e}")
        else:
            logger.warning("Azure Storage account name not configured. Cloud storage disabled.")

    def is_available(self) -> bool:
        """Check if cloud storage is available."""
        return self.blob_service_client is not None

    def _ensure_container_exists(self):
        """Create the container if it does not already exist."""
        if not self.is_available():
            return

        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            container_client.create_container()
            logger.info(f"Azure container '{self.container_name}' created.")
        except ResourceExistsError:
            logger.info(f"Azure container '{self.container_name}' already exists.")
        except AzureError as e:
            logger.warning(f"Could not create or access Azure container '{self.container_name}': {e}")

    def upload_prediction_data(self, prediction_history: list, stats: dict) -> bool:
        """
        Upload prediction history and statistics to cloud storage.

        Parameters
        ----------
        prediction_history : list
            List of prediction records
        stats : dict
            Statistics dictionary

        Returns
        -------
        bool
            True if upload successful, False otherwise
        """
        if not self.is_available():
            logger.warning("Cloud storage not available.")
            return False

        try:
            # Prepare data
            data = {
                "timestamp": datetime.now().isoformat(),
                "prediction_history": prediction_history,
                "statistics": stats
            }

            # Create blob name with timestamp
            blob_name = f"spam_detector_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            # Convert to JSON
            json_data = json.dumps(data, indent=2)

            # Upload to blob storage
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )

            blob_client.upload_blob(json_data, overwrite=True)
            logger.info(f"Successfully uploaded data to {blob_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to upload data to cloud: {e}")
            return False

    def upload_single_prediction(self, prediction_record: dict) -> bool:
        """
        Upload a single prediction record to cloud storage.

        Parameters
        ----------
        prediction_record : dict
            A single prediction entry containing message, label, confidence, and timestamp.

        Returns
        -------
        bool
            True if upload successful, False otherwise
        """
        if not self.is_available():
            logger.warning("Cloud storage not available.")
            return False

        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "prediction": prediction_record
            }
            blob_name = f"prediction_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
            json_data = json.dumps(data, indent=2)
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            blob_client.upload_blob(json_data, overwrite=True)
            logger.info(f"Successfully uploaded single prediction to {blob_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload single prediction to cloud: {e}")
            return False

    def upload_batch_results(self, batch_results: list, filename: str = None) -> bool:
        """
        Upload batch processing results to cloud storage.

        Parameters
        ----------
        batch_results : list
            List of batch prediction results
        filename : str, optional
            Custom filename for the blob

        Returns
        -------
        bool
            True if upload successful, False otherwise
        """
        if not self.is_available():
            logger.warning("Cloud storage not available.")
            return False

        try:
            # Prepare data
            data = {
                "timestamp": datetime.now().isoformat(),
                "batch_results": batch_results,
                "total_processed": len(batch_results)
            }

            # Create blob name
            if filename:
                blob_name = f"batch_results_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            else:
                blob_name = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            # Convert to JSON
            json_data = json.dumps(data, indent=2)

            # Upload to blob storage
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )

            blob_client.upload_blob(json_data, overwrite=True)
            logger.info(f"Successfully uploaded batch results to {blob_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to upload batch results to cloud: {e}")
            return False

# Global instance
cloud_storage = CloudStorage()