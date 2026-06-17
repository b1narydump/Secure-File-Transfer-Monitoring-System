# Secure File Transfer Monitoring System

![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python&logoColor=white)
![Watchdog](https://img.shields.io/badge/Powered%20by-watchdog-orange)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

A lightweight, Python-based file system monitor that watches a directory in real time, verifies file integrity with SHA-256 hashing, and raises alerts when activity touches sensitive locations. Built for audit logging, secure-transfer monitoring, and detecting unauthorized access.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Example Output](#example-output)
- [Security Considerations](#security-considerations)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The Secure File Transfer Monitoring System continuously tracks file creation, modification, deletion, and movement events inside a specified directory (and its subdirectories) using the [`watchdog`](https://pypi.org/project/watchdog/) library.

It is particularly useful for:

- Monitoring secure file transfers
- Detecting unauthorized access to sensitive directories
- Maintaining a comprehensive, timestamped audit trail of file system changes

---

## Features

| Feature | Description |
| --- | --- |
| Real-time Monitoring | Continuously watches a directory and its subdirectories for file system events. |
| Sensitive Directory Alerts | Triggers alerts for operations inside predefined sensitive paths. |
| File Integrity Verification | Calculates SHA-256 hashes for created and modified files. |
| Event Deduplication | Prevents log spam by ignoring rapid successive events on the same file. |
| Comprehensive Logging | Logs all events to a file and prints them to the console. |
| Configurable Settings | Easily adjust the monitored directory, sensitive paths, and log file. |

---

## Requirements

- Python 3.6+
- watchdog library

---

## Installation

1. Ensure Python 3.6+ is installed on your system.

2. Install the required dependency:

   ```bash
   pip install watchdog
   ```

3. Download or clone the repository:

   ```bash
   git clone https://github.com/<your-username>/secure-file-transfer-monitoring-system.git
   cd secure-file-transfer-monitoring-system
   ```

---

## Configuration

The script includes several configurable variables at the top of the file:

| Variable | Description | Default |
| --- | --- | --- |
| `MONITORED_DIRECTORY` | The directory to monitor | `"."` (current directory) |
| `SENSITIVE_DIRECTORIES` | List of directories considered sensitive | `["./secret"]` |
| `LOG_FILE` | Path to the log file | `"file_transfer_log.txt"` |
| `EVENT_DELAY` | Time in seconds to debounce events | `1` |

Modify these values as needed before running the script.

---

## Usage

1. Navigate to the directory containing the script.

2. Run it:

   ```bash
   python Secure_File_Transfer_Monitoring_System.py
   ```

3. Monitoring starts and prints the watched directory.
4. Perform file operations inside the monitored directory to see them tracked live.
5. Press `Ctrl+C` to stop monitoring.

---

## How It Works

**Hash Function** — `calculate_hash(file_path)` computes the SHA-256 hash of a file for integrity checking, returning `None` if the file cannot be read.

**Authorization Check** — `is_sensitive(path)` checks whether a path falls within any configured sensitive directory.

**Event Deduplication** — `should_ignore(file_path)` suppresses events that occur too frequently on the same file to avoid log spam.

**File Event Handler** — `FileMonitorHandler` extends watchdog's `FileSystemEventHandler`:
- `process()` is the core method that classifies the event type, checks for sensitive operations, calculates hashes, and logs results.
- Event hooks (`on_created`, `on_modified`, `on_deleted`, `on_moved`) are invoked by watchdog for each event type.

**Monitor Start** — `start_monitoring()` sets up the observer, schedules the handler, and runs the monitoring loop until interrupted.

---

## Example Output

```text
Monitoring Started...
Watching directory: /path/to/monitored/directory

FILE CREATED | Path: /path/to/monitored/directory/newfile.txt | Hash: a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
FILE MODIFIED | Path: /path/to/monitored/directory/newfile.txt | Hash: b8b7c1d4f1e9c2a3b5d6e8f7a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6

ALERT: Sensitive file created -> /path/to/monitored/directory/secret/important.txt
FILE CREATED | Path: /path/to/monitored/directory/secret/important.txt | Hash: c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0
```

---

## Security Considerations

- This system monitors and alerts but does not prevent unauthorized actions.
- Store the log file securely to prevent tampering.
- Consider integrating with an intrusion detection system (IDS) for stronger coverage.
- Review logs regularly for suspicious activity.

---

## Limitations

- Only monitors file system events; it does not track network transfers directly.
- Hash calculation may impact performance for very large files.
- Event deduplication may miss some extremely rapid changes.
- Requires appropriate file system permissions to monitor directories.

---

## Troubleshooting

| Issue | Suggested Fix |
| --- | --- |
| Monitoring doesn't start | Check file system permissions for the target directory. |
| `ModuleNotFoundError: watchdog` | Reinstall with `pip install watchdog`. |
| Too much log noise | Increase `EVENT_DELAY` for high-volume operations. |
| Unexpected behavior | Check the log file for errors or warnings. |

---

## License

This project is released under the MIT License. See the [`LICENSE`](LICENSE) file for details.

---

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.
