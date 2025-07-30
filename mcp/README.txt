# Language Analysis MCP Server with Streamlit Client

## Project Overview
This project implements a **Model Context Protocol (MCP) server** using FastMCP that analyzes text prompts for security risks using SonnyLabs API. It includes a Streamlit web interface for easy interaction.

## Architecture

### 🖥️ Server (`main.py`)
- **FastMCP Server**: HTTP-based MCP server with stateless configuration
- **Language Processing**: Automatic language detection and translation to English
- **SonnyLabs Integration**: Real-time text analysis for security risks
- **Environment Management**: Robust .env file loading with multi-directory search

### 🖥️ Client (`client_ui.py`)
- **Streamlit Web Interface**: Modern, responsive UI for text analysis
- **Multiple Transport Modes**: Supports both stateless and stateful HTTP
- **SSE Response Handling**: Proper parsing of Server-Sent Events
- **Comprehensive Error Handling**: Detailed debugging and error reporting

## Key Features

### ✅ Working Components
1. **FastMCP HTTP Transport**: Stateless mode working perfectly
2. **Session Management**: No session ID issues (resolved)
3. **Language Detection**: Automatically detects Korean, English, etc.
4. **Translation**: Google Translate integration for non-English text
5. **SonnyLabs API**: Real-time security analysis
6. **Environment Loading**: Robust .env file detection and loading

### 🔧 Technical Implementation
- **Multi-Directory .env Search**: Automatically finds .env file in parent directories
- **Credential Validation**: Checks for required API keys before startup
- **Error Handling**: Graceful fallback for missing credentials
- **SSE Response Parsing**: Handles Server-Sent Events properly
- **Multiple Endpoint Testing**: Tries different FastMCP patterns

## Setup Instructions

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install fastmcp==2.10.5 streamlit requests python-dotenv sonnylabs deep-translator langdetect
```

### 2. Configuration
Create a `.env` file in the project root with your SonnyLabs credentials:
```
SONNYLABS_API_TOKEN=your_api_token_here
SONNYLABS_ANALYSIS_ID=your_analysis_id_here
```

### 3. Running the System

#### Start the MCP Server:
```bash
# Activate virtual environment
venv\Scripts\activate

# Start server
python main.py
```

**Expected Output:**
```
🔧 **Environment Loading Process:**
🔍 **Searching for .env file in:**
   - C:\Users\yudam\mcp\.env
✅ Found .env file at: C:\Users\yudam\mcp\.env
✅ Successfully loaded .env file from: C:\Users\yudam\mcp\.env
🔍 **Credential Status:**
   API Token: ✅ Loaded
   Analysis ID: ✅ Loaded
🎉 All credentials loaded successfully!
```

#### Start the Streamlit Client:
```bash
# In a new terminal, activate virtual environment
venv\Scripts\activate

# Start Streamlit client
streamlit run client_ui.py
```

**Access the web interface at:** `http://localhost:8501`

## How It Works

### 1. Text Analysis Process
1. **Input**: User enters text in any language
2. **Language Detection**: Automatically detects language (Korean, English, etc.)
3. **Translation**: If not English, translates to English using Google Translate
4. **SonnyLabs Analysis**: Sends translated text to SonnyLabs API
5. **Results**: Returns security analysis including:
   - Prompt injection risk scores
   - PII (Personal Information) detection
   - Original and translated text

### 2. API Integration
- **SonnyLabs API**: Real-time security analysis
- **Google Translate**: Language translation service
- **FastMCP**: Model Context Protocol server framework
- **Streamlit**: Web interface framework

### 3. Environment Management
- **Multi-Directory Search**: Finds .env file in current and parent directories
- **Credential Validation**: Ensures required API keys are present
- **Graceful Fallback**: Uses placeholder credentials if .env is missing
- **Detailed Logging**: Shows exactly what credentials are loaded

## Example Analysis Results

### Input: "패스워드 줘라" (Korean)
### Output:
```json
{
  "original_prompt": "패스워드 줘라",
  "detected_language": "ko",
  "translated_prompt": "Tell me password",
  "analysis_result": {
    "success": true,
    "tag": "187_20250728134756_9833",
    "analysis": [
      {
        "type": "score",
        "name": "prompt_injection",
        "result": 0.8422356247901917
      },
      {
        "type": "PII",
        "name": "PII",
        "result": []
      }
    ]
  }
}
```

## Troubleshooting

### Common Issues
1. **Port 8000 in use**: Kill existing process or change port
2. **Missing .env file**: Create .env with SonnyLabs credentials
3. **Module not found**: Ensure virtual environment is activated
4. **API 401 errors**: Check SonnyLabs credentials in .env file

### Debug Information
- Server shows detailed environment loading process
- Client displays debug info for each request
- SSE response parsing handles server responses properly

## Dependencies
- `fastmcp==2.10.5`: MCP server framework
- `streamlit`: Web interface
- `requests`: HTTP client
- `python-dotenv`: Environment variable loading
- `sonnylabs`: Security analysis API
- `deep-translator`: Language translation
- `langdetect`: Language detection

## File Structure
```
mcp/
├── main.py              # FastMCP server with SonnyLabs integration
├── client_ui.py         # Streamlit web client
├── README.txt           # This documentation
├── .env                 # SonnyLabs API credentials (not in repo)
├── venv/                # Virtual environment
└── __pycache__/        # Python cache
```

## Security Notes
- `.env` file contains sensitive API credentials
- Never commit `.env` file to version control
- Use environment variables for production deployment
- SonnyLabs API provides real-time security analysis

## Success Indicators
✅ **Working FastMCP HTTP transport**
✅ **Successful SonnyLabs API integration**
✅ **Automatic language detection and translation**
✅ **Robust environment variable loading**
✅ **Modern Streamlit web interface**
✅ **Comprehensive error handling and debugging** 