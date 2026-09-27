#!/usr/bin/env python3
"""
Upload Ready-to-Publish Assets to Google Drive
Authenticates using Desktop App OAuth credentials (google.json).
Uploads clean master video, subtitles, metadata, and snapshots to Google Drive.
"""

import os
import sys
import argparse
import mimetypes
from pathlib import Path
from typing import List, Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, build_http
import httplib2
import google_auth_httplib2
import requests
import urllib3

urllib3.disable_warnings()

# If modifying these scopes, delete token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

PROJECTS_CONFIG = {
    'episode8_voynich_manuscript': {
        'name': 'episode8_voynich_manuscript',
        'title': "The 600-Year-Old Code That Even Modern AI Can't Crack (The Voynich Manuscript)",
        'dir': 'output/episode8_voynich_manuscript',
        'files': [
            'episode8_voynich_manuscript.mp4',
            'voynich_subtitles.srt',
            'voynich_subtitles.vtt',
            'tiktok_metadata_ep8.md',
        ],
        'include_snapshots': True,
    },
    'episode7_wow_signal': {
        'name': 'episode7_wow_signal',
        'title': "The 72-Second Deep Space Transmission That Science Still Can't Explain (The Wow! Signal)",
        'dir': 'output/episode7_wow_signal',
        'files': [
            'episode7_wow_signal.mp4',
            'wow_signal_subtitles.srt',
            'wow_signal_subtitles.vtt',
            'tiktok_metadata_ep7.md',
        ],
        'include_snapshots': True,
    },
    'episode6_project_azorian': {
        'name': 'episode6_project_azorian',
        'title': "How the CIA Secretly Stole a Soviet Nuclear Submarine from 3 Miles Deep (Project Azorian)",
        'dir': 'output/episode6_project_azorian',
        'files': [
            'episode6_project_azorian.mp4',
            'azorian_subtitles.srt',
            'azorian_subtitles.vtt',
            'tiktok_metadata_ep6.md',
        ],
        'include_snapshots': True,
    },
    'episode5_iridium_layer': {
        'name': 'episode5_iridium_layer',
        'title': "The 1-Centimeter Layer of Mud That Solved Earth's Biggest Murder Mystery",
        'dir': 'output/episode5_iridium_layer',
        'files': [
            'episode5_iridium_layer.mp4',
            'iridium_layer_subtitles.srt',
            'iridium_layer_subtitles.vtt',
            'tiktok_metadata_ep5.md',
        ],
        'include_snapshots': True,
    },
    'episode4_chicxulub': {
        'name': 'episode4_chicxulub',
        'title': "What Happened in the First 60 Minutes After the Asteroid Hit",
        'dir': 'output/episode4_chicxulub',
        'files': [
            'episode4_chicxulub.mp4',
            'chicxulub_subtitles.srt',
            'chicxulub_subtitles.vtt',
            'tiktok_metadata_ep4.md',
        ],
        'include_snapshots': True,
    },
    'episode3_carnian_pluvial': {
        'name': 'episode3_carnian_pluvial',
        'title': 'The Carnian Pluvial Episode',
        'dir': 'output/episode3_carnian_pluvial',
        'files': [
            'episode3_carnian_pluvial.mp4',
            'carnian_pluvial_subtitles.srt',
            'carnian_pluvial_subtitles.vtt',
            'tiktok_metadata_ep3.md',
        ],
        'include_snapshots': True,
    },
    'episode2_great_dying': {
        'name': 'episode2_great_dying',
        'title': 'The Great Dying',
        'dir': 'output/episode2_great_dying',
        'files': [
            'episode2_the_great_dying.mp4',
            'the_great_dying_subtitles.srt',
            'the_great_dying_subtitles.vtt',
            'tiktok_metadata_ep2.md',
        ],
        'include_snapshots': True,
    },
    'episode1_dinosaurus': {
        'name': 'episode1_dinosaurus',
        'title': 'Dinosaurus Pilot Catalog',
        'dir': 'output/episode1_dinosaurus',
        'files': [
            'pilot_dinosaurus_catalog.mp4',
            'tiktok_viral_metadata.md',
        ],
        'include_snapshots': True,
    },
}


import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)


def authenticate(creds_path: str = 'google.json', token_path: str = 'token.json') -> Credentials:
    """Authenticates using OAuth 2.0 InstalledAppFlow."""
    creds = None
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            print(f"[!] Warning reading {token_path}: {e}", flush=True)
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[*] Refreshing expired credentials...", flush=True)
            session = requests.Session()
            session.verify = False
            creds.refresh(Request(session=session))
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(
                    f"OAuth credentials file '{creds_path}' not found! "
                    "Please make sure google.json exists in root."
                )
            print("\n" + "="*70, flush=True)
            print("[*] Initiating Google OAuth authorization flow...", flush=True)
            print("[*] Opening browser for Google Drive permission approval...", flush=True)
            print("="*70 + "\n", flush=True)
            import wsgiref.simple_server
            from google_auth_oauthlib.flow import _RedirectWSGIApp, _WSGIRequestHandler

            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            wsgi_app = _RedirectWSGIApp("Authentication successful! You may now close this window.")
            local_server = wsgiref.simple_server.make_server(
                'localhost', 8080, wsgi_app, handler_class=_WSGIRequestHandler
            )
            flow.redirect_uri = f"http://localhost:{local_server.server_port}/"
            auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

            with open('AUTH_URL.txt', 'w', encoding='utf-8') as f:
                f.write(auth_url)

            print("\n" + "="*70, flush=True)
            print("[*] GOOGLE DRIVE OAUTH AUTHORIZATION REQUIRED", flush=True)
            print(f"[*] URL: {auth_url}", flush=True)
            print("="*70 + "\n", flush=True)

            try:
                import webbrowser
                webbrowser.open(auth_url)
            except Exception:
                pass

            print(f"[*] Waiting for authorization callback on http://localhost:{local_server.server_port}/...", flush=True)
            local_server.handle_request()
            local_server.server_close()

            authorization_response = wsgi_app.last_request_uri.replace("http", "https")
            flow.fetch_token(authorization_response=authorization_response)
            creds = flow.credentials

            if os.path.exists('AUTH_URL.txt'):
                try:
                    os.remove('AUTH_URL.txt')
                except Exception:
                    pass

        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())
        print(f"[+] Token cached to {token_path}", flush=True)

    return creds


def get_or_create_folder(service, folder_name: str, parent_id: Optional[str] = None) -> str:
    """Finds an existing folder by name (and parent) or creates it."""
    query = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}' and trashed = false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name, parents)'
    ).execute()
    files = results.get('files', [])

    if files:
        folder_id = files[0]['id']
        print(f"[+] Found existing folder: '{folder_name}' (ID: {folder_id})")
        return folder_id

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    folder = service.files().create(body=file_metadata, fields='id').execute()
    folder_id = folder.get('id')
    print(f"[+] Created new folder: '{folder_name}' (ID: {folder_id})")
    return folder_id


def upload_file(service, file_path: str, target_folder_id: str, remote_filename: Optional[str] = None) -> str:
    """Uploads a file to Google Drive with resumable upload and progress reporting."""
    p = Path(file_path)
    if not p.exists():
        print(f"[-] File not found: {file_path}")
        return ""

    filename = remote_filename or p.name
    file_size = p.stat().st_size
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'application/octet-stream'

    # Check if file with same name exists in folder
    query = f"name = '{filename}' and '{target_folder_id}' in parents and trashed = false"
    existing = service.files().list(q=query, fields='files(id, name, size)').execute().get('files', [])

    media = MediaFileUpload(
        str(p),
        mimetype=mime_type,
        resumable=True,
        chunksize=1024 * 1024 * 5 # 5MB chunks
    )

    if existing:
        file_id = existing[0]['id']
        print(f"[*] Updating existing file '{filename}' (ID: {file_id}, {file_size / (1024*1024):.2f} MB)...")
        request = service.files().update(
            fileId=file_id,
            media_body=media,
            fields='id, name, size'
        )
    else:
        print(f"[*] Uploading '{filename}' ({file_size / (1024*1024):.2f} MB)...")
        file_metadata = {
            'name': filename,
            'parents': [target_folder_id]
        }
        request = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, size'
        )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"    -> Progress: {progress}%", end='\r', flush=True)

    print(f"\n[+] Uploaded successfully: '{filename}' (ID: {response.get('id')})")
    return response.get('id')


def upload_project_assets(service, project_key: str, parent_folder_id: Optional[str] = None):
    """Uploads all clean and ready-to-publish assets for a given project."""
    if project_key not in PROJECTS_CONFIG:
        print(f"[-] Unknown project key: {project_key}")
        return

    cfg = PROJECTS_CONFIG[project_key]
    proj_dir = Path(cfg['dir'])
    if not proj_dir.exists():
        print(f"[-] Project output directory not found: {proj_dir}")
        return

    # Folder naming convention: "YTF - AG-Bang - {project_key}"
    folder_name = f"YTF - AG-Bang - {cfg['name']}"
    print(f"\n{'='*60}\nPreparing upload for: {cfg['title']}\nTarget folder: {folder_name}\n{'='*60}")

    project_folder_id = get_or_create_folder(service, folder_name, parent_id=parent_folder_id)

    # 1. Upload primary release files
    for fname in cfg['files']:
        fpath = proj_dir / fname
        if fpath.exists():
            upload_file(service, str(fpath), project_folder_id)
        else:
            print(f"[-] Missing expected file: {fpath}")

    # 2. Upload clean snapshots if available
    if cfg.get('include_snapshots', False):
        snap_dir = proj_dir / 'snapshots'
        if snap_dir.exists() and snap_dir.is_dir():
            snap_folder_id = get_or_create_folder(service, 'snapshots', parent_id=project_folder_id)
            for snap_file in sorted(snap_dir.glob('*.jpg')):
                upload_file(service, str(snap_file), snap_folder_id)


def main():
    parser = argparse.ArgumentParser(description="Upload clean AG-Bang video assets to Google Drive")
    parser.add_argument(
        '--project',
        type=str,
        default='episode5_iridium_layer',
        help="Project key (e.g. episode5_iridium_layer, or 'all'). Default: episode5_iridium_layer"
    )
    parser.add_argument(
        '--parent-folder',
        type=str,
        default='YTF - AG-Bang',
        help="Optional top-level Google Drive parent folder name. Set to '' for root."
    )
    parser.add_argument(
        '--creds',
        type=str,
        default='google.json',
        help="Path to google.json OAuth client secret"
    )
    parser.add_argument(
        '--token',
        type=str,
        default='token.json',
        help="Path to token.json credential cache"
    )
    args = parser.parse_args()

    print("[*] Authenticating with Google Drive API...")
    creds = authenticate(args.creds, args.token)
    http = build_http()
    http.disable_ssl_certificate_validation = True
    authorized_http = google_auth_httplib2.AuthorizedHttp(creds, http=http)
    service = build('drive', 'v3', http=authorized_http)

    parent_folder_id = None
    if args.parent_folder.strip():
        parent_folder_id = get_or_create_folder(service, args.parent_folder.strip())

    if args.project.lower() == 'all':
        for pkey in PROJECTS_CONFIG:
            upload_project_assets(service, pkey, parent_folder_id)
    else:
        upload_project_assets(service, args.project, parent_folder_id)

    print("\n[OK] All tasks completed successfully.")


if __name__ == '__main__':
    main()
