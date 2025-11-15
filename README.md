# Tic Tac Toe - Python GUI Project Template

A modern, fully-featured Tic Tac Toe game built with Python and CustomTkinter. This project serves as a **comprehensive template for Python GUI applications**, demonstrating best practices for project structure, packaging, distribution, and installation.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

## 🎯 Project Goals

This project was created as a **reference template** for building professional Python GUI applications. It demonstrates:

- ✅ **Modern GUI Development** using CustomTkinter
- ✅ **Proper Project Structure** with separation of concerns
- ✅ **Python Packaging** with setuptools and wheel distribution
- ✅ **Isolated Virtual Environment** installation
- ✅ **Professional Windows Distribution** with automated installer
- ✅ **Desktop Integration** with shortcuts and icons
- ✅ **Clean Architecture** following best practices
- ✅ **Complete Documentation** for users and developers

**Use this as a starting point** for your own Python GUI projects!

---

## 🎮 Features

### Game Features
- Classic Tic Tac Toe gameplay (3x3 grid)
- Two-player mode (X vs O)
- Win detection (rows, columns, diagonals)
- Draw detection
- Game reset functionality
- Clean, modern UI with CustomTkinter

### Technical Features
- **Isolated Installation**: Uses virtual environment (no global dependency conflicts)
- **Windows Integration**: Custom icons for desktop, titlebar, and taskbar
- **One-Click Installation**: Automated installer with automatic updates
- **Professional Packaging**: Wheel distribution for easy deployment
- **Clean Uninstall**: Simple folder deletion removes everything
- **OneDrive Compatible**: Smart desktop path detection

---

## 📁 Project Structure

```
tic-tac-toe/
├── src/
│   └── tictactoe/
│       ├── __init__.py
│       ├── __main__.py              # Entry point
│       ├── assets/
│       │   └── favicon.ico          # Application icon
│       ├── config/                  # Configuration (future use)
│       ├── domain/
│       │   └── logic.py             # Game logic (model)
│       └── ui/
│           └── gui/
│               └── main.py          # GUI implementation (view)
├── tests/                           # Unit tests
├── docs/
│   ├── INSTALLATION-GUIDE.md        # User installation guide
│   └── INSTALLATION-TECHNICAL-DETAILS.md  # Technical deep-dive
├── dist/                            # Built distribution files
├── pyproject.toml                   # Project metadata & dependencies
├── requirements.txt                 # Development dependencies
├── wheel-builder.bat                # Build script
└── README.md

Architecture: MVC-inspired separation
- domain/: Business logic (Model)
- ui/: User interface (View)
- Future: Add controller layer if needed
```

---

## 🚀 Quick Start

### For Users

1. **Download** the latest release (tic-tac-toe.zip)
2. **Extract** the ZIP file
3. **Run** `installation.bat`
4. **Launch** from desktop shortcut

See [INSTALLATION-GUIDE.md](docs/INSTALLATION-GUIDE.md) for detailed instructions.

### For Developers

#### Prerequisites
- Python 3.8 or higher
- Git (optional)

#### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd tic-tac-toe

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

#### Run in Development Mode

```bash
# Activate virtual environment first
.venv\Scripts\activate

# Run the game
python -m tictactoe
# or
tictactoe
```

#### Build Distribution

```bash
# Run the build script
.\wheel-builder.bat

# Output will be in dist/ folder:
# - tictactoe-0.1.0-py3-none-any.whl
# - installation.bat
# - tic-tac-toe-starter.vbs
# - favicon.ico
```

---

## 📦 Distribution & Installation

### Building for Distribution

This project includes an automated build system:

1. **Run** `wheel-builder.bat`
2. **Outputs** to `dist/` folder:
   - Python wheel package
   - Windows installer script
   - VBScript launcher (for silent execution)
   - Application icon

### Installation System

The installer (`installation.bat`) performs:

1. ✅ Removes old version (if exists)
2. ✅ Creates installation directory
3. ✅ Copies distribution files
4. ✅ Creates isolated virtual environment
5. ✅ Installs package and dependencies
6. ✅ Creates desktop shortcut with icon
7. ✅ Configures taskbar integration

**Installation Path**: `%LOCALAPPDATA%\Programs\ttt.v0.1.0`

For technical details, see [INSTALLATION-TECHNICAL-DETAILS.md](docs/INSTALLATION-TECHNICAL-DETAILS.md).

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Programming language
- **CustomTkinter**: Modern UI framework (enhanced Tkinter)
- **setuptools**: Python packaging
- **wheel**: Binary distribution format

### Dependencies
- `customtkinter>=5.2.2` - Modern UI components
- `pillow>=12.0.0` - Image handling
- `darkdetect>=0.8.0` - OS theme detection
- `packaging>=25.0` - Version management

### Development Tools
- `pytest` - Unit testing
- `black` - Code formatting
- `ruff` - Linting
- `mypy` - Type checking

---

## 🎨 Using This Template

### Adapting for Your Project

1. **Clone/Download** this repository
2. **Rename** the project folder and package
3. **Update** `pyproject.toml`:
   - Change `name`, `version`, `description`
   - Update author information
   - Modify dependencies as needed
4. **Replace** game logic in `domain/` with your business logic
5. **Redesign** UI in `ui/gui/` for your application
6. **Update** `favicon.ico` with your application icon
7. **Modify** `wheel-builder.bat` to match your project name/version
8. **Rebuild** and test installation

### Key Concepts to Reuse

- **Virtual Environment Installation**: Keeps user's Python clean
- **Wheel Distribution**: Professional packaging method
- **Desktop Integration**: Icons and shortcuts
- **VBScript Launcher**: Silent execution without console
- **AppUserModelID**: Proper Windows taskbar integration
- **Automated Installer**: One-click installation experience

---

## 📚 Documentation

- **[INSTALLATION-GUIDE.md](docs/INSTALLATION-GUIDE.md)**: User-friendly installation instructions
- **[INSTALLATION-TECHNICAL-DETAILS.md](docs/INSTALLATION-TECHNICAL-DETAILS.md)**: Technical deep-dive for developers

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tictactoe

# Run specific test file
pytest tests/test_logic.py
```

---

## 🤝 Contributing

This is a template project, but improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎓 Learning Resources

### If You're New To:

**Python Packaging:**
- [Python Packaging User Guide](https://packaging.python.org/)
- [setuptools documentation](https://setuptools.pypa.io/)

**CustomTkinter:**
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)

**Virtual Environments:**
- [venv documentation](https://docs.python.org/3/library/venv.html)
- [Real Python: Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)

**Windows Scripting:**
- [VBScript Reference](https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/)
- [Batch Scripting Guide](https://ss64.com/nt/)

---

## 🚧 Roadmap / Future Enhancements

Potential improvements for this template:

- [ ] AI opponent (single-player mode)
- [ ] Settings/preferences system
- [ ] Multiple themes (dark/light mode)
- [ ] Sound effects
- [ ] Statistics tracking
- [ ] Linux/Mac installer support
- [ ] PyInstaller build for standalone .exe
- [ ] Automated testing in CI/CD
- [ ] Internationalization (i18n)

---

## 💡 Design Decisions

### Why CustomTkinter?
- Modern, professional look
- Easy to use (similar to Tkinter)
- Built-in theming support
- Active development and community

### Why Virtual Environment Installation?
- **Isolation**: No conflicts with user's Python packages
- **Clean**: Easy uninstall (just delete folder)
- **Professional**: Industry standard for Python applications
- **Versioning**: Each version can have different dependencies

### Why Wheel Distribution?
- **Standard**: Python-recommended distribution format
- **Fast**: Binary format, no compilation needed
- **Compatible**: Works with pip and all package managers
- **Professional**: Used by major Python projects

### Why VBScript Launcher?
- **Silent**: Runs without console window (pythonw.exe)
- **Integration**: Allows custom icon in taskbar
- **Simple**: No additional dependencies needed
- **Windows-native**: Uses built-in Windows Script Host

---

## ❓ FAQ

**Q: Can I use this for commercial projects?**  
A: Yes! MIT License allows commercial use.

**Q: Does this work on Linux/Mac?**  
A: The installer is Windows-specific, but the code runs on any platform. You'd need to create platform-specific installers.

**Q: Can I package this as a standalone .exe?**  
A: Yes! Use PyInstaller or similar tools. This template focuses on wheel distribution, but .exe packaging is compatible.

**Q: Why not use Qt/wxPython instead of Tkinter?**  
A: CustomTkinter provides a modern look with Tkinter's simplicity. Qt/wxPython are great alternatives but have larger dependencies.

**Q: How do I update users to a new version?**  
A: Users just run the new installer - it automatically removes the old version first.

---

## 🙏 Acknowledgments

- **CustomTkinter** by Tom Schimansky - Modern Tkinter components
- **Python Packaging Authority** - Packaging tools and guidance
- **Microsoft** - Windows integration APIs

---

## 📧 Contact

For questions about using this template:
- Open an issue on GitHub
- Check existing documentation
- Review the technical details document

---

**Built with ❤️ as a learning resource and project template**

*Last Updated: November 15, 2025*