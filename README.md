# 🔐 Password Cracker Pro

A comprehensive password cracking tool with both GUI and command-line interfaces. This tool uses screen automation to attempt password cracking by trying different combinations and detecting success through image recognition.

![Password Cracker Pro](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-Educational-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ⚠️ Important Disclaimer

This tool is intended **ONLY** for:
- Educational purposes
- Authorized security testing
- Testing your own systems

**Never use this tool on systems you don't own or don't have explicit permission to test.** Unauthorized access to computer systems is illegal and unethical.

## ✨ Features

- **🖥️ Modern GUI Interface**: Intuitive graphical interface with real-time progress tracking
- **💻 Command-Line Interface**: Advanced CLI for power users and automation
- **🎯 Image-Based Success Detection**: Uses screenshot comparison to detect successful attempts
- **⚡ Configurable Speed**: Adjustable delays and attempt rates
- **🔒 Built-in Safety Features**: Failsafe mechanisms to prevent accidents
- **📊 Real-time Statistics**: Live progress tracking with detailed metrics
- **🧪 Demo Mode**: Safe testing mode for demonstrations and learning
- **🖼️ Image Preview**: Built-in image browser and preview functionality

## 📋 Requirements

### Desktop Platforms:
- **Python 3.7 or higher**
- **Operating System**: Windows, macOS, or Linux with GUI support
- **Screen Resolution**: 1024x768 minimum recommended
- **Permissions**: Screen recording permissions (macOS/Linux may require additional setup)

### Mobile Platforms:
- **Android 5.0+** (API level 21)
- **Termux** or **Pydroid 3** for Python support
- **RAM**: 2GB+ recommended for smooth operation
- **Storage**: 500MB+ free space

## 🚀 Installation

### Option 1: Quick Setup

1. **Clone or download** this repository:
   ```bash
   git clone <repository-url>
   cd "python cracker"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

### Option 2: Manual Installation

1. **Install Python dependencies**:
   ```bash
   pip install pyautogui Pillow
   ```

2. **Optional dependencies** for enhanced functionality:
   ```bash
   pip install opencv-python
   ```

3. **Download all files** to the same directory and run:
   ```bash
   python app.py
   ```

## 🎮 Usage

### GUI Version (Recommended)

Launch the GUI application:
```bash
python app.py
# or
python app.py --gui
```

**GUI Features:**
- **Configuration Panel**: Set password length, delays, and starting position
- **Image Selection**: Browse and preview success detection images  
- **Real-time Progress**: Live updates of current attempt, elapsed time, and speed
- **Control Buttons**: Start, stop, and create test images
- **Activity Log**: Detailed logging of all actions and results

### CLI Version

Launch the command-line version:
```bash
python app.py --cli
```

### 📱 Android Version

For Android devices using Termux or Pydroid 3:

**Method 1: CLI in Termux**
```bash
# Install Termux from F-Droid
# Setup: pkg install python python-pip
# Run: python app.py --cli
```

**Method 2: Mobile GUI with Kivy**
```bash
# Install: pip install kivy
# Run: python android_app.py
```

**📖 Complete Android Setup:** See `ANDROID_SETUP.md` for detailed instructions.

**✨ Android Features:**
- Touch-friendly interface
- Password cracking simulation  
- Hash comparison (MD5, SHA256)
- Educational demonstrations
- No root required

### Command Line Options

```bash
python app.py [OPTIONS]

Options:
  --gui     Launch GUI version (default)
  --cli     Launch CLI version  
  --info    Show application information
  --check   Check dependencies only
  --help    Show help message
```

## 🛠️ Configuration

### GUI Configuration
All settings can be configured through the GUI interface:

- **Success Image**: Select the image that appears when password is correct
- **Password Length**: Number of digits in password (1-10)
- **Start From**: Starting password number (useful for resuming)
- **Max Attempts**: Maximum number of passwords to try
- **Delay**: Time between attempts (seconds)
- **Demo Mode**: Safe testing mode that simulates cracking

### CLI Configuration
Edit the configuration variables in `password_cracker.py`:

```python
SUCCESS_IMAGE = "success.png"      # Path to success detection image
PASSWORD_LENGTH = 4                # Length of password to try
START_FROM = 0                     # Starting password number
MAX_ATTEMPTS = 10000              # Maximum attempts
ATTEMPT_DELAY = 0.5               # Delay between attempts
DEMO_MODE = False                 # Set to True for safe testing
```

## 🖼️ Success Image Setup

The tool requires a "success image" to detect when the correct password is entered.

### Creating a Success Image

1. **Use the built-in generator**:
   - Click "🖼️ Create Test Image" in the GUI, or
   - Run: `python create_test_image.py`

2. **Take your own screenshot**:
   - Enter a wrong password to see the "failed" state
   - Enter the correct password
   - Take a screenshot of the success message/indicator
   - Save as PNG format
   - Select the image in the GUI or place it as `success.png`

### Image Requirements
- **Format**: PNG, JPG, or other common image formats
- **Content**: Should contain unique elements that only appear on success
- **Size**: Any size (tool will handle scaling)
- **Quality**: Clear, high-contrast images work best

## 🔧 Advanced Usage

### Demo Mode
Perfect for learning and testing:
- Set "Demo Mode" checkbox in GUI or `DEMO_MODE = True` in CLI
- Tool simulates password cracking without actually typing
- Will "find" password "1234" or "0000" for demonstration
- Safe to run anywhere

### Resuming Interrupted Sessions
If cracking is interrupted, you can resume:
1. Note the last attempted password from the log
2. Set "Start From" to that number
3. Restart the process

### Batch Processing
For testing multiple systems:
1. Create different success images for each system
2. Use CLI version with different configuration files
3. Script the process using shell scripts or batch files

## 🛡️ Safety Features

### Built-in Protections
- **Failsafe**: Move mouse to top-left corner to instantly stop
- **Configurable Delays**: Prevent overwhelming target systems  
- **Demo Mode**: Safe testing without actual input
- **Stop Button**: Immediate termination in GUI
- **Keyboard Interrupt**: Ctrl+C support in CLI

### Best Practices
- Always test in Demo Mode first
- Use reasonable delays (0.5+ seconds recommended)
- Test with your own systems only
- Keep success images private and secure
- Monitor system resources during operation

## 📁 File Structure

```
python cracker/
├── app.py                    # Main launcher
├── password_cracker_gui.py   # GUI application
├── password_cracker.py       # Original CLI version
├── create_test_image.py      # Test image generator
├── requirements.txt          # Python dependencies
├── README.md                # This documentation
└── success.png              # Default success image (generated)
```

## 🐛 Troubleshooting

### Common Issues

**"pyautogui not found"**
```bash
pip install pyautogui
```

**"PIL/Pillow not found"**
```bash
pip install Pillow
```

**GUI won't start**
- Check if tkinter is installed: `python -c "import tkinter"`
- On Linux: `sudo apt-get install python3-tk`
- Use CLI version as fallback: `python app.py --cli`

**Success image not detected**
- Verify image file exists and is readable
- Try recreating the success image
- Ensure success condition is visible on screen
- Test with different confidence levels

**Permission errors (macOS/Linux)**
- Grant screen recording permissions in System Preferences
- Run with appropriate permissions for automation

### Getting Help

1. **Check dependencies**: `python app.py --check`
2. **View application info**: `python app.py --info`  
3. **Test with Demo Mode** to verify basic functionality
4. **Check log output** for detailed error messages

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Version Information
Check your Python version:
```bash
python --version
```

Minimum supported version: Python 3.7+

## 📝 License

This project is provided for educational purposes only. Users are responsible for ensuring their use complies with applicable laws and regulations.

## 🤝 Contributing

This is an educational project. If you find bugs or have suggestions for improvements:

1. Test thoroughly in Demo Mode
2. Document any issues clearly
3. Provide screenshots or logs when helpful
4. Consider security implications of any changes

## 📞 Support

For educational use and learning purposes:
- Read through this README carefully
- Test with Demo Mode first
- Check troubleshooting section
- Review log files for error details

Remember: This tool is for authorized testing and education only!
