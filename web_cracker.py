#!/usr/bin/env python3
"""
Core cracking simulation logic for the web app.

This module provides a CPU-only, non-automation, educational password
"cracking" simulation suitable for running inside a web server.
It does NOT perform any desktop automation or screen scraping.
"""

from __future__ import annotations

import itertools
import threading
import time
import hashlib
from dataclasses import dataclass, field
from typing import Optional, Literal, Dict, Any


HashMethod = Literal["plain", "md5", "sha256", "zip"]


@dataclass
class CrackerConfig:
    target_password: str = "1234"
    password_length: int = 4
    delay_seconds: float = 0.01
    method: HashMethod = "plain"
    charset: str = "0123456789"
    zip_path: Optional[str] = None
    job_id: Optional[str] = None
    output_zip_path: Optional[str] = None


@dataclass
class CrackerStatus:
    is_running: bool = False
    attempts: int = 0
    current_password: str = ""
    start_time: Optional[float] = None
    found_password: Optional[str] = None
    completed: bool = False
    success: bool = False
    artifact_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        elapsed = 0.0
        if self.start_time:
            elapsed = max(0.0, time.time() - self.start_time)
        rate = (self.attempts / elapsed) if elapsed > 0 else 0.0
        return {
            "is_running": self.is_running,
            "attempts": self.attempts,
            "current_password": self.current_password,
            "elapsed_seconds": round(elapsed, 3),
            "rate_per_second": round(rate, 2),
            "found_password": self.found_password,
            "completed": self.completed,
            "success": self.success,
            "artifact_path": self.artifact_path,
        }


class PasswordCracker:
    """CPU-only cracking simulation suitable for a web backend."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._config: CrackerConfig = CrackerConfig()
        self._status: CrackerStatus = CrackerStatus()
        self._should_stop: bool = False

    # Public API
    def start(self, config: CrackerConfig) -> None:
        with self._lock:
            if self._status.is_running:
                raise RuntimeError("Cracker already running")

            self._config = config
            self._status = CrackerStatus(
                is_running=True,
                attempts=0,
                current_password="",
                start_time=time.time(),
                found_password=None,
                completed=False,
                success=False,
                artifact_path=None,
            )
            self._should_stop = False

            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

    def stop(self) -> None:
        with self._lock:
            self._should_stop = True

    def status(self) -> CrackerStatus:
        with self._lock:
            # Return a shallow copy to avoid external mutation
            s = self._status
            copy = CrackerStatus(
                is_running=s.is_running,
                attempts=s.attempts,
                current_password=s.current_password,
                start_time=s.start_time,
                found_password=s.found_password,
                completed=s.completed,
                success=s.success,
                artifact_path=s.artifact_path,
            )
            return copy

    # Internal
    def _hash(self, password: str) -> str:
        method = self._config.method
        if method == "md5":
            return hashlib.md5(password.encode()).hexdigest()
        if method == "sha256":
            return hashlib.sha256(password.encode()).hexdigest()
        return password

    def _target_value(self) -> str:
        if self._config.method in ("md5", "sha256"):
            return self._hash(self._config.target_password)
        return self._config.target_password

    def _run(self) -> None:
        try:
            mode = self._config.method
            charset = self._config.charset
            length = self._config.password_length
            delay = max(0.0, float(self._config.delay_seconds))

            if mode == "zip":
                if not self._config.zip_path:
                    raise ValueError("zip_path is required for zip mode")
                self._run_zip(charset, length, delay)
                return

            target_value = self._target_value()

            for combo in itertools.product(charset, repeat=length):
                with self._lock:
                    if self._should_stop:
                        self._status.is_running = False
                        self._status.completed = True
                        self._status.success = False
                        return

                password = "".join(combo)

                # Update status
                with self._lock:
                    self._status.current_password = password
                    self._status.attempts += 1

                # Check match
                value = self._hash(password) if self._config.method != "plain" else password
                if value == target_value:
                    with self._lock:
                        self._status.found_password = password
                        self._status.is_running = False
                        self._status.completed = True
                        self._status.success = True
                    return

                if delay:
                    time.sleep(delay)

            # Exhausted combinations
            with self._lock:
                self._status.is_running = False
                self._status.completed = True
                self._status.success = False
        except Exception:
            # Ensure we mark as completed on error
            with self._lock:
                self._status.is_running = False
                self._status.completed = True
                self._status.success = False

    def _run_zip(self, charset: str, length: int, delay: float) -> None:
        import os
        import zipfile
        try:
            import pyzipper  # type: ignore
        except Exception:
            pyzipper = None  # type: ignore

        zip_path = self._config.zip_path  # type: ignore[assignment]
        output_zip = self._config.output_zip_path

        def try_password(pw: str) -> bool:
            pwd_bytes = pw.encode()
            # Try with pyzipper (AES + legacy) if available
            if pyzipper is not None:
                try:
                    with pyzipper.AESZipFile(zip_path) as zf:  # type: ignore[arg-type]
                        zf.pwd = pwd_bytes
                        names = zf.namelist()
                        if not names:
                            return False
                        # Attempt to read a small portion to validate password
                        with zf.open(names[0]) as f:
                            _ = f.read(1)
                        return True
                except Exception:
                    pass
            # Fallback to stdlib zipfile (legacy crypto only)
            try:
                with zipfile.ZipFile(zip_path) as zf:  # type: ignore[arg-type]
                    names = zf.namelist()
                    if not names:
                        return False
                    _ = zf.read(names[0], pwd=pwd_bytes)
                return True
            except Exception:
                return False

        for combo in itertools.product(charset, repeat=length):
            with self._lock:
                if self._should_stop:
                    self._status.is_running = False
                    self._status.completed = True
                    self._status.success = False
                    return

            password = "".join(combo)

            with self._lock:
                self._status.current_password = password
                self._status.attempts += 1

            if try_password(password):
                # Extract all contents with found password and, if requested, write an unlocked zip
                try:
                    extract_dir = None
                    if output_zip:
                        extract_dir = f"{output_zip}.d"
                        os.makedirs(extract_dir, exist_ok=True)
                        # Extract using pyzipper if possible for AES, else stdlib
                        if 'pyzipper' in globals() and pyzipper is not None:
                            with pyzipper.AESZipFile(zip_path) as zf:  # type: ignore[arg-type]
                                zf.pwd = password.encode()
                                zf.extractall(path=extract_dir)
                        else:
                            with zipfile.ZipFile(zip_path) as zf:  # type: ignore[arg-type]
                                zf.extractall(path=extract_dir, pwd=password.encode())
                        # Re-zip without password
                        import shutil
                        shutil.make_archive(output_zip, 'zip', extract_dir)
                        artifact = f"{output_zip}.zip"
                    else:
                        artifact = None
                except Exception:
                    artifact = None

                with self._lock:
                    self._status.found_password = password
                    self._status.is_running = False
                    self._status.completed = True
                    self._status.success = True
                    self._status.artifact_path = artifact
                return

            if delay:
                time.sleep(delay)

        with self._lock:
            self._status.is_running = False
            self._status.completed = True
            self._status.success = False


