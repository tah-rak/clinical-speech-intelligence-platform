"""Firestore database provider (optional GCP integration)."""

import logging
from typing import Any
from uuid import UUID

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class FirestoreProvider:
    """Optional Firestore persistence layer for visits."""

    def __init__(self) -> None:
        self._db = None

    def _get_db(self):
        if self._db is None:
            try:
                from google.cloud import firestore

                self._db = firestore.Client(project=settings.FIRESTORE_PROJECT_ID or None)
            except ImportError:
                raise RuntimeError(
                    "google-cloud-firestore required. "
                    "Install with: pip install google-cloud-firestore"
                )
        return self._db

    def save_visit(self, visit_id: UUID, data: dict[str, Any]) -> None:
        if not settings.GCP_ENABLED:
            return
        try:
            db = self._get_db()
            db.collection("visits").document(str(visit_id)).set(data, merge=True)
        except Exception as e:
            logger.warning("Firestore sync failed: %s", e)

    def get_visit(self, visit_id: UUID) -> dict[str, Any] | None:
        if not settings.GCP_ENABLED:
            return None
        try:
            db = self._get_db()
            doc = db.collection("visits").document(str(visit_id)).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            logger.warning("Firestore read failed: %s", e)
            return None
