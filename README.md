# ryon
Ryon: A statically typed, compiled language designed for scientific, AI, and engineering applications, featuring a Python-like syntax with advanced type systems, explicit error handling, and contract programming.

Certainly! Here's an updated version of your `README.md` with a new section on how to install the project in a virtual environment:

## Installation

To install the `ryon` project in an isolated virtual environment, follow the steps below:

### Prerequisites
Ensure you have Python 3.10 or higher installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

Additionally, it's recommended to install `virtualenv` if you don't have it:

```bash
pip install virtualenv
```

### Installation Steps

1. **Clone the repository:**

   If you haven't already, clone the repository using:

   ```bash
   git clone git@github.com:bigr/ryon.git
   cd ryon
   ```

2. **Create and activate a virtual environment:**

   - On macOS and Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

   This will create and activate a virtual environment named `venv` where all dependencies will be installed.

3. **Install Flit in the virtual environment:**

   After activating the virtual environment, you need to install Flit locally in that environment:

   ```bash
   pip install flit
   ```

4. **Install the project dependencies using Flit:**

   Once Flit is installed, you can install the project and its dependencies with:

   ```bash
   flit install
   ```

   This command installs the project and its dependencies from `pyproject.toml`.

5. **Install optional development or testing dependencies (optional):**

   If you're working on the project and need development tools (e.g., for linting and testing), you can install the
6. optional dependencies using Flit.

   To install the **development** dependencies:

   ```bash
   flit install --extras=dev
   ```

   To install the **testing** dependencies:

   ```bash
   flit install --extras=test
   ```

   This command installs the respective optional dependencies defined under `[project.optional-dependencies]`
   in `pyproject.toml`. You can specify any other optional extras similarly if needed.


## Setting Up Pre-commit

To ensure code quality and consistency, we use `pre-commit` hooks in our project. `Pre-commit` is a framework that manages and maintains multi-language pre-commit hooks. It checks your code for errors before you commit it to version control.

### Prerequisites
Before you can use `pre-commit`, make sure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

### Installation

Follow these steps to set up `pre-commit` in your local development environment:

1. **Install pre-commit:**
   Open a terminal and run the following command to install `pre-commit` globally or in your virtual environment:

   ```bash
   pip install pre-commit
   ```

2. **Clone the repository:**
   If you haven't already cloned the repository, clone it using:

   ```bash
   git clone git@github.com:bigr/ryon.git
   cd ryon
   ```

3. **Install the pre-commit hook:**
   Run the following command within the repository directory to set up the git hook scripts:

   ```bash
   pre-commit install
   ```

   This command installs the pre-commit hook into your `.git/hooks` directory which will automatically check your commits for any issues before they are committed.

### Running Pre-commit

After installation, `pre-commit` will run automatically on `git commit`, but you can manually run it on all files in the repository with:

```bash
pre-commit run --all-files
```

This command is useful for initial setup or to check files after modifying the configuration.

### Updating Hooks

To update the versions of the hooks to the latest available versions, use:

```bash
pre-commit autoupdate
```

This will modify your `.pre-commit-config.yaml` to update the hooks to their latest versions as specified by the repositories.

---

This section should guide contributors on how to install and use `pre-commit` effectively in your project. Adjust the repository URL and directory as necessary to match your project's specific details.
```

This new section explains how to install the project into a virtual environment, along with installing both the main and optional dependencies. Let me know if you'd like to tweak any part of it further!

## Setting Up Pre-commit

To ensure code quality and consistency, we use `pre-commit` hooks in our project. `Pre-commit` is a framework that manages and maintains multi-language pre-commit hooks. It checks your code for errors before you commit it to version control.

### Prerequisites
Before you can use `pre-commit`, make sure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

### Installation

Follow these steps to set up `pre-commit` in your local development environment:

1. **Install pre-commit:**
   Open a terminal and run the following command to install `pre-commit` globally or in your virtual environment:

   ```bash
   pip install pre-commit
   ```

2. **Clone the repository:**
   If you haven't already cloned the repository, clone it using:

   ```bash
   git clone git@github.com:bigr/ryon.git
   cd ryon
   ```

3. **Install the pre-commit hook:**
   Run the following command within the repository directory to set up the git hook scripts:

   ```bash
   pre-commit install
   ```

   This command installs the pre-commit hook into your `.git/hooks` directory which will automatically check your commits for any issues before they are committed.

### Running Pre-commit

After installation, `pre-commit` will run automatically on `git commit`, but you can manually run it on all files in the repository with:

```bash
pre-commit run --all-files
```

This command is useful for initial setup or to check files after modifying the configuration.

### Updating Hooks

To update the versions of the hooks to the latest available versions, use:

```bash
pre-commit autoupdate
```

This will modify your `.pre-commit-config.yaml` to update the hooks to their latest versions as specified by the repositories.

---

This section should guide contributors on how to install and use `pre-commit` effectively in your project. Adjust the repository URL and directory as necessary to match your project's specific details.
