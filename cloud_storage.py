"""
Cloud storage module for uploading prediction data to Azure Blob Storage or Google Drive.

This module supports Azure Blob Storage and Google Drive using service account credentials.
"""

import io
import json
import logging
import os
from datetime import datetime

from azure.core.exceptions import AzureError, ResourceExistsError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseUpload
except ImportError:  # pragma: no cover
    service_account = None
    build = None
    MediaIoBaseUpload = None

logger = logging.getLogger(__name__)

CLOUD_STORAGE_PROVIDER = os.getenv("CLOUD_STORAGE_PROVIDER", "azure").strip().lower()
AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "spam-detector-data")
GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE",
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
)
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
GOOGLE_DRIVE_ACCOUNT_EMAIL = os.getenv("GOOGLE_DRIVE_ACCOUNT_EMAIL")

class CloudStorage:
    """Handles cloud storage operations for spam detector data."""

    def __init__(self):
        self.provider = CLOUD_STORAGE_PROVIDER
        self.blob_service_client = None
        self.gdrive_service = None
        self.container_name = AZURE_STORAGE_CONTAINER_NAME
        self.folder_id = GOOGLE_DRIVE_FOLDER_ID
        self.drive_account_email = GOOGLE_DRIVE_ACCOUNT_EMAIL

        if self.provider == "azure":
            self._init_azure()
        elif self.provider in {"gdrive", "google_drive", "google-drive"}:
            self._init_google_drive()
        else:
            logger.warning(
                f"Unsupported cloud storage provider '{self.provider}'. "
                "Set CLOUD_STORAGE_PROVIDER to 'azure' or 'gdrive'."
            )

    def is_available(self) -> bool:
        """Check if cloud storage is available."""
        return self.blob_service_client is not None or self.gdrive_service is not None

    @property
    def storage_provider_name(self) -> str:
        if self.provider == "azure":
            return "Azure Blob Storage"
        if self.provider in {"gdrive", "google_drive", "google-drive"}:
            return "Google Drive"
        return self.provider.title()

    def _init_azure(self):
        if not AZURE_STORAGE_ACCOUNT_NAME:
            logger.warning("Azure Storage account name not configured. Cloud storage disabled.")
            return

        try:
            account_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
            credential = DefaultAzureCredential()
            self.blob_service_client = BlobServiceClient(
                account_url=account_url,
                credential=credential,
            )
            self._ensure_container_exists()
            logger.info("Azure Blob Storage client initialized successfully.")
        except Exception as e:
            logger.warning(f"Failed to initialize Azure Blob Storage: {e}")

    def _init_google_drive(self):
        if not build or not service_account or not MediaIoBaseUpload:
            logger.warning(
                "Google Drive support is unavailable because required packages are missing. "
                "Install google-api-python-client and google-auth."
            )
            return

        if not GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE:
            logger.warning(
                "Google Drive service account credentials not configured. "
                "Set GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE or GOOGLE_APPLICATION_CREDENTIALS."
            )
            return

        try:
            scopes = ["https://www.googleapis.com/auth/drive.file"]
            kwargs = {
                "filename": GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE,
                "scopes": scopes,
            }
            if self.drive_account_email:
                kwargs["subject"] = self.drive_account_email
                logger.info(
                    f"Using Google Drive account email for subject impersonation: {self.drive_account_email}"
                )
            credentials = service_account.Credentials.from_service_account_file(
                **kwargs,
            )
            self.gdrive_service = build(
                "drive",
                "v3",
                credentials=credentials,
                cache_discovery=False,
            )
            logger.info("Google Drive client initialized successfully.")
        except Exception as e:
            logger.warning(f"Failed to initialize Google Drive client: {e}")

    def _ensure_container_exists(self):
        """Create the container if it does not already exist."""
        if not self.blob_service_client:
            return

        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            container_client.create_container()
            logger.info(f"Azure container '{self.container_name}' created.")
        except ResourceExistsError:
            logger.info(f"Azure container '{self.container_name}' already exists.")
        except AzureError as e:
            logger.warning(
                f"Could not create or access Azure container '{self.container_name}': {e}"
            )

    def _upload_blob(self, blob_name: str, json_data: str) -> bool:
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name,
            )
            blob_client.upload_blob(json_data, overwrite=True)
            logger.info(f"Successfully uploaded data to {blob_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload data to Azure Blob Storage: {e}")
            return False

    def _upload_google_drive(self, json_data: str, filename: str) -> bool:
        if not self.gdrive_service:
            logger.warning("Google Drive service not available.")
            return False

        try:
            media = MediaIoBaseUpload(
                io.BytesIO(json_data.encode("utf-8")),
                mimetype="application/json",
                resumable=True,
            )
            file_metadata = {
                "name": filename,
                "mimeType": "application/json",
            }
            if self.folder_id:
                file_metadata["parents"] = [self.folder_id]

            file = self.gdrive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id",
            ).execute()
            logger.info(
                f"Successfully uploaded data to Google Drive file ID {file.get('id')}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to upload data to Google Drive: {e}")
            return False

    def upload_prediction_data(self, prediction_history: list, stats: dict) -> bool:
        if not self.is_available():
            logger.warning("Cloud storage not available.")
            return False

        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "prediction_history": prediction_history,
                "statistics": stats,
            }
            filename = f"spam_detector_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            json_data = json.dumps(data, indent=2)

            if self.provider == "azure":
                return self._upload_blob(filename, json_data)
            return self._upload_google_drive(json_data, filename)

        except Exception as e:
            logger.error(f"Failed to upload data to cloud: {e}")
            return False

    def upload_single_prediction(self, prediction_record: dict) -> bool:
        if not self.is_available():
            logger.warning("Cloud storage not available.")
            return False

        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "prediction": prediction_record,
            }
            filename = f"prediction_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
            json_data = json.dumps(data, indent=2)

            if self.provider == "azure":
                return self._upload_blob(filename, json_data)
            return self._upload_google_drive(json_data, filename)

        except Exception as e:
            logger.error(f"Failed to upload single prediction to cloud: {e}")
            return False

    def upload_classification_entry(
        self,
        message: str,
        label: str,
        confidence: float,
        user_email: str | None = None,
    ) -> bool:
        if not self.is_available():
            logger.warning("Cloud storage not available.")
            return False

        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "label": label,
                "confidence": confidence,
                "message": message,
            }
            if user_email:
                entry["user_email"] = user_email

            filename = f"{label}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
            json_data = json.dumps(entry, indent=2)

            if self.provider == "azure":
                return self._upload_blob(filename, json_data)
            return self._upload_google_drive(json_data, filename)

        except Exception as e:
            logger.error(f"Failed to upload classification entry to cloud: {e}")
            return False

    def upload_batch_results(self, batch_results: list, filename: str = None) -> bool:
        if not self.is_available():
            logger.warning("Cloud storage not available.")
            return False

        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "batch_results": batch_results,
                "total_processed": len(batch_results),
            }
            if filename:
                filename = f"batch_results_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            else:
                filename = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            json_data = json.dumps(data, indent=2)

            if self.provider == "azure":
                return self._upload_blob(filename, json_data)
            return self._upload_google_drive(json_data, filename)

        except Exception as e:
            logger.error(f"Failed to upload batch results to cloud: {e}")
            return False


# Global instance
cloud_storage = CloudStorage()
