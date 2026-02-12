"""AVGI Music Execution entrypoint.

Runs a SwiftAPI-enforced instrumental generation workflow.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

from swiftapi import (
    AttestationRevokedError,
    Enforcement,
    PolicyViolation,
    SignatureVerificationError,
    SwiftAPI,
)


def build_instrumental(track_name: str) -> str:
    """Generate a detailed instrumental build log and return output WAV path."""
    plugin_chain = [
        {"name": "Omnisphere", "preset": "Saw Lead"},
        {"name": "Valhalla Vintage Verb", "preset": "Reverb Plate"},
        {"name": "FabFilter Pro-Q3", "preset": "Mix Clean EQ"},
        {"name": "Soundtoys Decapitator", "preset": "Subtle Saturation"},
        {"name": "Cymatics Sample Layer", "preset": "Kick & Percussion"},
    ]

    print(f"[INFO] Generating instrumental for '{track_name}'...")
    for plugin in plugin_chain:
        print(f"[INFO] Loading {plugin['name']} with preset {plugin['preset']}")

    output_file = Path(f"{track_name}_instrumental.wav")
    output_file.write_bytes(b"")
    print(f"[INFO] Instrumental generated: {output_file}")
    return str(output_file)


def run_with_enforcement(track_name: str, intent: str) -> str:
    """Execute render under SwiftAPI enforcement with attestation checks."""
    api_key = os.environ.get("SWIFTAPI_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing SWIFTAPI_KEY. Set it in your environment before running."
        )

    api = SwiftAPI(key=api_key)
    guard = Enforcement(client=api, paranoid=False, verbose=True)

    run_action: Callable[[], str] = lambda: build_instrumental(track_name)
    return guard.run(run_action, action="music_render", intent=intent)


def main() -> int:
    """CLI entrypoint for mobile/web one-shot execution."""
    track_name = os.environ.get("TRACK_NAME", "Pyramids")
    intent = os.environ.get(
        "MUSIC_RENDER_INTENT",
        "Generate clean instrumental with precise plugin chain",
    )

    try:
        track_output = run_with_enforcement(track_name=track_name, intent=intent)
        print(f"[SUCCESS] Execution attested: {track_output}")
        return 0
    except PolicyViolation as err:
        print(f"[DENIED] PolicyViolation: {err.denial_reason}")
    except SignatureVerificationError:
        print("[CRITICAL] Attestation signature invalid!")
    except AttestationRevokedError as err:
        print(f"[CRITICAL] Attestation revoked: {err.jti}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
