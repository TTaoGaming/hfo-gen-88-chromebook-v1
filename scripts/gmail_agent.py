# Medallion: Bronze | Mutation: 0% | Component: Gmail Agent Scaffold
"""
Local Gmail API agent for VS Code usage.
- Reads message metadata (From/Subject/Date).
- Optional label application (requires gmail.modify scope).
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

READONLY_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
MODIFY_SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

DEFAULT_CREDENTIALS_PATH = Path(".hfo_secret/gmail/credentials.json")
DEFAULT_TOKEN_PATH = Path(".hfo_secret/gmail/token.json")


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _load_credentials(scopes: Iterable[str], creds_path: Path, token_path: Path) -> Credentials:
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not creds_path.exists():
                raise FileNotFoundError(
                    f"Missing OAuth client file at {creds_path}. "
                    "Download from Google Cloud Console (OAuth Desktop app)."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), scopes)
            creds = flow.run_local_server(port=0)
        _ensure_parent(token_path)
        token_path.write_text(creds.to_json())
    return creds


def _get_gmail_service(scopes: Iterable[str], creds_path: Path, token_path: Path):
    creds = _load_credentials(scopes, creds_path, token_path)
    return build("gmail", "v1", credentials=creds)


def _get_header(headers, name: str) -> str:
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")
    return ""


def _ensure_label(service, label_name: str) -> str:
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for label in labels:
        if label.get("name") == label_name:
            return label.get("id")
    new_label = {"name": label_name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
    created = service.users().labels().create(userId="me", body=new_label).execute()
    return created["id"]


def list_messages(
    query: str,
    max_results: int,
    label: str | None,
    apply_label: bool,
    creds_path: Path,
    token_path: Path,
):
    scopes = MODIFY_SCOPES if apply_label else READONLY_SCOPES
    service = _get_gmail_service(scopes, creds_path, token_path)
    response = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    messages = response.get("messages", [])

    label_id = None
    if apply_label and label:
        label_id = _ensure_label(service, label)

    for msg in messages:
        msg_id = msg.get("id")
        full = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="metadata", metadataHeaders=["From", "Subject", "Date"])
            .execute()
        )
        headers = full.get("payload", {}).get("headers", [])
        from_value = _get_header(headers, "From")
        subject_value = _get_header(headers, "Subject")
        date_value = _get_header(headers, "Date")

        print(f"{date_value} | {from_value} | {subject_value}")

        if apply_label and label_id:
            service.users().messages().modify(
                userId="me",
                id=msg_id,
                body={"addLabelIds": [label_id]},
            ).execute()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local Gmail API agent scaffold.")
    parser.add_argument("--query", default="-category:social -category:promotions", help="Gmail search query")
    parser.add_argument("--max-results", type=int, default=20, help="Max messages to list")
    parser.add_argument("--label", default=None, help="Label name to apply")
    parser.add_argument("--apply-label", action="store_true", help="Apply label (requires modify scope)")
    parser.add_argument("--creds", default=str(DEFAULT_CREDENTIALS_PATH), help="Path to OAuth client JSON")
    parser.add_argument("--token", default=str(DEFAULT_TOKEN_PATH), help="Path to token JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    creds_path = Path(os.path.expanduser(args.creds))
    token_path = Path(os.path.expanduser(args.token))
    list_messages(
        query=args.query,
        max_results=args.max_results,
        label=args.label,
        apply_label=args.apply_label,
        creds_path=creds_path,
        token_path=token_path,
    )


if __name__ == "__main__":
    main()
