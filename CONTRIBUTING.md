# 🤝 Contributing to MaestroAI

Thank you for your interest in contributing to MaestroAI! This document provides guidelines for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

Be respectful, inclusive, and collaborative. We're all here to build something great!

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/tahammnour/MaestroAI.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Submit a pull request

## 💻 Development Process

### Setting Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your values
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=api

# Run specific test file
pytest tests/test_intent_classifier.py
```

## 📝 Coding Standards

### Python Style Guide

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

### Example

```python
def classify_intent(
    user_message: str,
    context: Optional[dict] = None
) -> IntentClassification:
    """
    Classifies user intent from a message.
    
    Args:
        user_message: The user's input message
        context: Optional conversation context
        
    Returns:
        IntentClassification object with intent and confidence
        
    Raises:
        ValueError: If user_message is empty
    """
    if not user_message:
        raise ValueError("user_message cannot be empty")
    
    # Implementation here
    return IntentClassification(
        intent="LEAVE_REQUEST",
        confidence=0.95
    )
```

## 🔀 Pull Request Process

1. Update README.md if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Create a descriptive PR with:
   - What changed
   - Why it changed
   - How to test

## ✅ Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] Tests are added/updated
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No linter errors
- [ ] Commit messages are clear

## 📞 Questions?

Open an issue or reach out to the team!

---

Thank you for contributing! 🎉

