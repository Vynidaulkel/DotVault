# DotVault

**DotVault** is a command-line tool for managing and organizing dotfiles using symbolic links and profile-based configurations. It helps you version-control your configuration files and easily switch between setups across Linux environments.

## ✨ Features

- Profile-based dotfile organization (e.g., `work`, `personal`, `gaming`)
- Automatic symbolic link creation
- Easily switch between profiles without manual file edits
- Portable and Git-friendly dotfile management

## 🚀 Why use DotVault?

Maintaining consistent dotfiles across environments can be tedious. DotVault simplifies the process by:

- Keeping your configuration files clean and centralized
- Letting you track changes with Git
- Enabling fast environment setup through symbolic linking

## 🧰 Tech Stack

- Python 3
- `argparse`, `os`, `json`
- Shell-level operations (Linux file system, symlink creation)

> ⚠️ **Note:** This tool is intended for use on Linux-based systems. It was developed and tested on Fedora. Basic knowledge of the terminal and symbolic links is recommended.

## 📦 Installation

Clone the repository and add `dotvault` to your PATH manually, or run it using `python`:

```bash
git clone https://github.com/Vynidaulkel/dotvault.git
cd dotvault
python3 -m dotvault.cli.main --help
