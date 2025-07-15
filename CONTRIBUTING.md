# Contributing to OpenMusic

Thank you for your interest in contributing to **OpenMusic**! 🎶  
We welcome contributions of all kinds—bug fixes, features, documentation, tests, and suggestions.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Ways to Contribute](#ways-to-contribute)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Development Setup](#development-setup)
- [Style Guide](#style-guide)
- [Releasing to PyPI](#releasing-to-pypi)
- [License](#license)

---

## Code of Conduct


### Our Pledge

We as members, contributors, and maintainers of **OpenMusic** pledge to make participation in our community a respectful, harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

We are committed to fostering a positive environment where everyone feels welcome to contribute, learn, and grow.

---

### Our Standards

Examples of behavior that contributes to a positive environment include:

- Being kind and respectful to others
- Giving and gracefully accepting constructive feedback
- Actively listening and being open to differing viewpoints
- Helping others and encouraging collaboration
- Acknowledging the contributions of others

Examples of unacceptable behavior include:

- Harassment or discrimination of any kind
- Personal attacks, insults, or derogatory comments
- Publishing others’ private information (e.g., address or contact info) without permission
- Disruptive behavior in community spaces (spamming, trolling, etc.)

---

### Enforcement Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

Maintainers have the right and responsibility to remove, edit, or reject contributions, comments, issues, or other interactions that violate this Code of Conduct.

---

### Scope

This Code of Conduct applies within all project spaces—online and offline—including the GitHub repo, discussion boards, social media, and in-person events related to **OpenMusic**.

---

### Reporting Issues

If you experience or witness unacceptable behavior, please report it by contacting the maintainers at:

@frankanator. on Discord

Reports will be handled confidentially. Please include as much detail as possible (links, context, screenshots if relevant).

---

### Enforcement Guidelines

Maintainers will follow these guidelines in determining consequences for any actions they deem in violation of this Code of Conduct:

1. **Warning**: A private warning with clarity on the violation.
2. **Temporary Ban**: A temporary removal from interactions with the project.
3. **Permanent Ban**: Removal from all project spaces indefinitely.

---

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant, version 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html).

---

Thank you for helping us keep OpenMusic a safe, respectful, and welcoming place for all.

---

## Getting Started

1. **Fork** the repository
2. **Clone** your fork:
```bash
   git clone https://github.com/your-username/openmusic.git
   cd openmusic
```

3. **Install dependencies** using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
See [README.md's Installation section](https://github.com/Frankanator8/openmusic/README.md)

---

## Ways to Contribute

* Suggest new features or enhancements
* Report or fix bugs
* Improve documentation
* Add or improve tests
* Translate the UI (if applicable)
* Build plugins or extensions

---

## Pull Request Guidelines

1. Create a new branch from `main`:

   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Follow the [Style Guide](#style-guide)
3. Ensure tests pass with:

   ```bash
   pytest
   ```
4. Open a Pull Request with a clear title and description.

> Tip: Prefix your PR titles with `feat:`, `fix:`, `docs:`, `refactor:`, etc.

---

## Style Guide

* **Python**: [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* **Docstrings**: Use [PEP 257](https://www.python.org/dev/peps/pep-0257/) format
* **Type Hints**: Use wherever possible
* **Imports**: Organize with `isort` and format with `black`

Run the style checks with:

```bash
black openmusic
isort openmusic
flake8 openmusic
```

---

## Releasing to PyPI

Only maintainers can publish releases. To request a release:

1. Ensure your code is merged into `main`
2. Bump the version in `setup.py`
3. Add a changelog entry
4. Tag a release:

   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

Maintainers will then publish to PyPI:

```bash
twine upload dist/*
```

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project: **MIT**.

---

Thank you for your help!

