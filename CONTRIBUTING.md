# Contributing to Object Tracking

Thank you for your interest in contributing! Here are the guidelines:

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/object-tracking.git
   cd object-tracking
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set up the development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

## Development Workflow

1. **Make your changes** following the code style guide
2. **Test your changes**:
   ```bash
   python tracker.py
   ```
3. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: description of changes"
   ```
4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a Pull Request** on GitHub

## Code Style

- Use PEP 8 style guide
- Add docstrings to functions and classes
- Keep functions focused and small
- Add comments for complex logic

## Types of Contributions

### Bug Reports
Create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Feature Requests
- Explain the use case
- How it benefits users
- Potential implementation approach

### Improvements
- Performance optimizations
- Code refactoring
- Documentation improvements
- Test additions

## Code Review Process

All submissions require review before merging:
- We'll review for code quality, style, and functionality
- May request changes or ask questions
- Once approved, your PR will be merged

## Questions?

Feel free to open an issue for discussions or questions!

---

Thank you for making this project better! 🙏
