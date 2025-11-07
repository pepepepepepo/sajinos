# Contributing to SaijinOS

Thank you for your interest in contributing to SaijinOS! 🎉

This document provides guidelines and information for contributors who want to help improve our multi-persona AI integration system.

## 🌟 Ways to Contribute

### Code Contributions
- **Bug fixes**: Help us identify and fix issues
- **New features**: Implement new personas, AI models, or system capabilities
- **Performance optimizations**: Improve system efficiency and response times
- **Documentation**: Enhance guides, API docs, and examples

### Non-Code Contributions
- **Issue reporting**: Submit detailed bug reports and feature requests
- **Testing**: Help test new features and provide feedback
- **Documentation**: Improve guides, tutorials, and API documentation
- **Community support**: Help other users in discussions and issues

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Git for version control
- Basic understanding of FastAPI and AI systems
- Familiarity with YAML configuration files

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/sajinos.git
   cd sajinos
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv saijin-env
   source saijin-env/bin/activate  # On Windows: saijin-env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Development Server**
   ```bash
   python src/saijinos_real_ai.py
   ```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 for Python code formatting
- Use meaningful variable and function names
- Add docstrings for classes and functions
- Keep functions focused and modular

### Commit Messages
Use conventional commit format:
```
type(scope): description

Examples:
feat(personas): add new Touri persona integration
fix(api): resolve FastAPI routing issue
docs(readme): update installation instructions
refactor(config): improve YAML parsing logic
```

### Branch Naming
- `feature/description` for new features
- `fix/description` for bug fixes
- `docs/description` for documentation updates
- `refactor/description` for code improvements

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_personas.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Writing Tests
- Add tests for new features and bug fixes
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies appropriately

## 🎭 Persona Development Guidelines

### Adding New Personas
1. **Create Persona Definition**
   - Add YAML file in `personas/` directory
   - Define personality traits, voice settings, and behavioral patterns
   - Include emotional response templates

2. **Implement Persona Logic**
   - Add Python class in `src/personas/`
   - Implement required methods: `process_input()`, `generate_response()`
   - Handle BMP synchronization and emotional state

3. **Update Documentation**
   - Add persona description to `docs/en/persona-system.md`
   - Update README persona list
   - Create usage examples

### Persona Configuration Schema
```yaml
name: "PersonaName"
type: "specialized"  # mirror, specialized, support
personality:
  traits: ["trait1", "trait2"]
  emotional_range: [0.0, 1.0]
  response_style: "descriptive"
voice:
  speed: 1.0
  pitch: 1.0
  accent: "neutral"
bmp_sync:
  preferred_tempo: 120
  rhythm_pattern: "4/4"
```

## 🔧 API Development

### Adding New Endpoints
1. **Define Route**
   ```python
   @app.post("/api/new-endpoint")
   async def new_endpoint(request: RequestModel):
       # Implementation
       return {"status": "success"}
   ```

2. **Add Request/Response Models**
   ```python
   from pydantic import BaseModel
   
   class RequestModel(BaseModel):
       field: str
       
   class ResponseModel(BaseModel):
       result: str
   ```

3. **Update API Documentation**
   - Add endpoint to `docs/en/api-reference.md`
   - Include request/response examples
   - Document error codes and responses

## 📚 Documentation Guidelines

### Writing Style
- Use clear, concise language
- Provide practical examples
- Include both English and Japanese versions when possible
- Use consistent formatting and structure

### Documentation Structure
```
docs/
├── en/                 # English documentation
│   ├── api-reference.md
│   ├── persona-system.md
│   └── bmp-system.md
├── architecture/       # System architecture
└── handovers/         # Development handover notes
```

## 🐛 Issue Reporting

### Bug Reports
Please include:
- **Environment**: OS, Python version, dependency versions
- **Steps to reproduce**: Detailed reproduction steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Full error logs and stack traces
- **Screenshots**: If applicable

### Feature Requests
Please include:
- **Problem description**: What problem does this solve?
- **Proposed solution**: How should it work?
- **Use cases**: When would this be useful?
- **Implementation ideas**: Any technical suggestions

## 🔍 Code Review Process

### For Contributors
1. **Self-review**: Check your code before submitting
2. **Small PRs**: Keep pull requests focused and reasonably sized
3. **Tests**: Ensure all tests pass and add new tests as needed
4. **Documentation**: Update relevant documentation

### For Reviewers
1. **Be constructive**: Provide helpful feedback and suggestions
2. **Focus on code quality**: Look for bugs, performance issues, and maintainability
3. **Consider alternatives**: Suggest different approaches when appropriate
4. **Be timely**: Review PRs promptly to keep development moving

## 🏷️ Release Process

### Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist
- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create GitHub release
- [ ] Tag commit with version

## 💬 Community Guidelines

### Code of Conduct
- **Be respectful**: Treat all contributors with respect and kindness
- **Be inclusive**: Welcome people of all backgrounds and experience levels
- **Be collaborative**: Work together to improve the project
- **Be patient**: Help newcomers learn and contribute effectively

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community chat
- **Pull Requests**: Code review and technical discussions

## 🎯 Priority Areas

We're especially looking for help with:

1. **AI Model Integration**: Support for new language models
2. **Performance Optimization**: System speed and efficiency improvements
3. **Docker Containerization**: Production deployment solutions
4. **CI/CD Pipeline**: Automated testing and deployment
5. **Internationalization**: Multi-language support expansion
6. **Voice System Enhancement**: Advanced TTS integration
7. **Mobile Integration**: Mobile app development
8. **Cloud Deployment**: AWS/GCP/Azure deployment guides

## 📞 Getting Help

If you need help or have questions:
1. Check existing [Issues](https://github.com/pepepepepepo/sajinos/issues)
2. Search [Documentation](docs/en/)
3. Start a [Discussion](https://github.com/pepepepepepo/sajinos/discussions)
4. Create a new issue with the `question` label

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- CHANGELOG.md for significant contributions
- Release notes for major features
- Annual contributor appreciation posts

---

Thank you for contributing to SaijinOS! Together, we're building the future of emotionally intelligent AI. 🚀✨