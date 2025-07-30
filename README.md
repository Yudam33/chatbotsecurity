# Chatbot Security MCP Project

A Model Context Protocol (MCP) server for analyzing and securing chatbot interactions using SonnyLabs API for prompt injection detection and PII analysis.

## ⚠️ Security Notice

**IMPORTANT**: This repository contains example API keys and configuration values that are NOT valid. These are placeholder values for demonstration purposes only.

For proper setup and security configuration, see: [SECURITY.md](SECURITY.md)

## 🚀 Features

- **Prompt Injection Detection**: Analyzes text for potential prompt injection attacks
- **PII Detection**: Identifies personally identifiable information in text
- **Advanced Sanitization**: Multiple layers of text sanitization and attack detection
- **Unicode Normalization**: Detects evasion techniques using unicode characters
- **Base64 Decoding**: Handles encoded attack attempts
- **Hex String Analysis**: Identifies hex-encoded malicious content

## 📋 Prerequisites

- Python 3.8+
- SonnyLabs API account
- Required Python packages (see requirements.txt)

## 🔧 Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatbotsecurity
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   - Create a `.env` file with your real API credentials
   - See [SECURITY.md](SECURITY.md) for detailed setup instructions

4. **Run the server**
   ```bash
   python mcp/main.py
   ```

## 📁 Project Structure

```
chatbotsecurity/
├── .gitignore          # Git ignore rules for sensitive files
├── SECURITY.md         # Security configuration guide
├── README.md           # This file
├── mcp/               # Main MCP server implementation
│   ├── main.py        # Core server logic
│   ├── client_ui.py   # Client interface
│   └── README.txt     # Detailed documentation
└── mcp_server_example-main/  # Example server implementation
    ├── mcp/
    │   ├── server.py  # Example server
    │   ├── client.py  # Example client
    │   └── .gitignore # Example gitignore
    └── requirements.txt
```

## 🛡️ Security Features

- **Environment Variable Protection**: All sensitive data stored in `.env` files
- **Git Ignore Configuration**: Prevents accidental commit of sensitive files
- **Example Value Warnings**: Clear indication of non-functional example values
- **Input Sanitization**: Multiple layers of text cleaning and validation
- **Attack Detection**: Comprehensive detection of various attack vectors

## 🔍 Usage

The MCP server provides tools for:

1. **Text Analysis**: Analyze text for security threats
2. **Prompt Validation**: Validate and sanitize user inputs
3. **Attack Detection**: Identify various types of attacks
4. **PII Detection**: Find personally identifiable information

## 📚 Documentation

- [SECURITY.md](SECURITY.md) - Security configuration and best practices
- `mcp/README.txt` - Detailed technical documentation
- Code comments - Inline documentation for all major functions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all security guidelines are followed
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This project is for educational and demonstration purposes. Always follow security best practices when deploying in production environments.