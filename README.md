# gta6-discord-rpc

A modular Python client that shows a custom GTA VI themed Discord Rich Presence status.

## Features

- Discord Rich Presence integration
- Modular source code in `src/`
- Start scripts for Windows (`run.bat`) and Linux/macOS (`run.sh`)
- Installer script (`install.py`) and unit tests in `tests/`

## Requirements

- Python 3.8 or newer
- A running Discord desktop client

## Installation

```bash
git clone https://github.com/Higer23/gta6-discord-rpc.git
cd gta6-discord-rpc
python install.py
```

## Configuration

Copy the example configuration and adjust it to your needs:

```bash
cp config.json.example config.json
```

Do not commit your personal `config.json` if it contains private values.

## Usage

- Windows: double-click `run.bat`
- Linux / macOS: `bash run.sh`

Or run directly:

```bash
python main.py
```

## Running Tests

```bash
python -m pytest tests/
```

## License

Released under the MIT License. See [LICENSE](LICENSE).
