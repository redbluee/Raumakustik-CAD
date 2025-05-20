# Raumakustik-CAD

## Table of Contents
- [Raumakustik-CAD](#raumakustik-cad)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
    - [Python Environment Setup](#python-environment-setup)
      - [1. Create a Virtual Environment](#1-create-a-virtual-environment)
      - [2. Activate the Virtual Environment](#2-activate-the-virtual-environment)
      - [3. Ensure Pip is Up-to-Date](#3-ensure-pip-is-up-to-date)
      - [4. Using `requirements.txt` for Package Management](#4-using-requirementstxt-for-package-management)
      - [5. Deactivating the Virtual Environment](#5-deactivating-the-virtual-environment)
  - [Using the Virtual Environment](#using-the-virtual-environment)
    - [Activating the Environment](#activating-the-environment)
    - [Installing/Managing Packages](#installingmanaging-packages)
    - [Deactivating the Environment](#deactivating-the-environment)

## Prerequisites


### Python Environment Setup

This guide outlines the steps to set up a consistent development environment for this project using Python's built-in `venv` module for virtual environments and `pip` for package management. [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments)

#### 1. Create a Virtual Environment

A virtual environment creates an isolated space for your Python project, allowing you to manage dependencies for this project separately from others.

*   **Navigate to your project directory:**
    Open your terminal or command prompt and change to the root directory of this project.

*   **Create the virtual environment:**
    Execute the following command. It's a common convention to name the virtual environment directory `.venv`.
    ```bash
    python3 -m venv .venv
    ```
    This command creates a `.venv` folder in your project directory. This folder contains a copy of the Python interpreter, the standard library, and other supporting files.

#### 2. Activate the Virtual Environment

Before you can install or use packages within the virtual environment, you need to activate it.

*   **On macOS and Linux:**
    ```bash
    source .venv/bin/activate
    ```

*   **On Windows (Command Prompt):**
    ```bash
    .\.venv\Scripts\activate.bat
    ```

*   **On Windows (PowerShell):**
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
    If you encounter an error on PowerShell stating that running scripts is disabled, you might need to set the execution policy for the current session:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```
    Then, try running the activation script again.

    Once activated, your shell prompt will typically be prefixed with `(.venv)` to indicate that the virtual environment is active.

#### 3. Ensure Pip is Up-to-Date

`pip` is the Python package installer. It's good practice to ensure you have the latest version within your activated virtual environment.

```bash
python -m pip install --upgrade pip
```
Using `python -m pip` is recommended as it guarantees you are using the `pip` associated with the activated virtual environment's Python interpreter.

#### 4. Using `requirements.txt` for Package Management

A `requirements.txt` file lists the project dependencies, making it easy to install the same set of packages across different environments or for other collaborators.

*   **Install packages from `requirements.txt`:**
    If a `requirements.txt` file is present in the project (or once you create one), you can install all listed packages with:
    ```bash
    pip install -r requirements.txt
    ```

*   **Generating `requirements.txt`:**
    After installing new packages or changing versions, you should update the `requirements.txt` file. To do this, run:
    ```bash
    pip freeze > requirements.txt
    ```
    This command records all packages currently installed in the active virtual environment into the `requirements.txt` file. It's recommended to commit this file to your version control system.

#### 5. Deactivating the Virtual Environment

When you are finished working on the project, you can deactivate the virtual environment:

```bash
deactivate
```
This command returns you to your system's default Python environment.

## Using the Virtual Environment

Once the initial setup is complete and your virtual environment (`.venv`) is created, here's how you typically work with it:

### Activating the Environment

Each time you want to work on this project in a new terminal session, you need to activate the virtual environment. This ensures that you are using the project-specific Python interpreter and packages.

*   **On macOS and Linux:**
    ```bash
    source .venv/bin/activate
    ```

*   **On Windows (Command Prompt):**
    ```bash
    .\.venv\Scripts\activate.bat
    ```

*   **On Windows (PowerShell):**
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
    Your terminal prompt should change to indicate the active environment (e.g., `(.venv) your-prompt$`).

### Installing/Managing Packages

With the environment active, you can use `pip` to install, update, or remove packages. Remember to update your `requirements.txt` if you make changes to the project's dependencies:

```bash
pip install <new-package>
pip freeze > requirements.txt
```

### Deactivating the Environment

When you're done working on the project for the session, you can deactivate the environment:

```bash
deactivate
```
This will return you to your system's global Python environment.
