# main.py
"""
⚠️  SECURITY WARNING ⚠️
This repository contains example API keys and configuration values that are NOT valid.
These are placeholder values for demonstration purposes only.

If you see any API keys, tokens, or credentials in this code:
- They are EXAMPLE values only
- They are NOT valid or functional
- They should NOT be used in production
- They are included only for code structure demonstration

For actual use, you must:
1. Create your own .env file with real credentials
2. Never commit real API keys to version control
3. Use environment variables for all sensitive data
"""

from fastmcp import FastMCP
from sonnylabs_py import SonnyLabsClient
from deep_translator import GoogleTranslator
from langdetect import detect
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import re
import html
import base64
import hashlib
import logging
from datetime import datetime

"""
IMPORTANT: The current analysis ID (187) is only configured for PII detection.
To get prompt_injection analysis, you need to:

1. Go to https://sonnylabs-service.onrender.com/analysis
2. Create a NEW analysis with prompt injection scanning enabled
3. Update your .env file with the new analysis ID

The current setup only returns PII analysis, not prompt_injection scores.
"""

# 보안 로깅 설정
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.WARNING)

def find_env_file():
    """Search for .env file in current and parent directories"""
    current_path = Path(__file__).resolve().parent
    search_paths = []
    
    while current_path != current_path.parent:
        search_paths.append(current_path / '.env')
        current_path = current_path.parent
    
    for env_path in search_paths:
        if env_path.exists():
            print(f"✅ Found .env file at: {env_path}")
            return env_path
    
    print("❌ No .env file found in search paths")
    return None

def load_environment():
    """Load environment variables with detailed logging"""
    env_file = find_env_file()
    
    if env_file:
        load_dotenv(env_file)
        print(f"✅ Loaded environment from: {env_file}")
    else:
        load_dotenv()  # Try default locations
        print("⚠️  Using default .env search")
    
    # Get credentials with detailed logging
    # NOTE: These environment variables should contain REAL API credentials
    # The values "YOUR_API_KEY" and "YOUR_ANALYSIS_ID" are placeholders only
    # You must set up your own .env file with actual credentials
    api_token = os.getenv("SONNYLABS_API_TOKEN")
    analysis_id = os.getenv("SONNYLABS_ANALYSIS_ID")
    
    print(f"🔑 API Token: {'✅ Set' if api_token and api_token != 'YOUR_API_KEY' else '❌ Missing/Invalid'}")
    print(f"🆔 Analysis ID: {'✅ Set' if analysis_id and analysis_id != 'YOUR_ANALYSIS_ID' else '❌ Missing/Invalid'}")
    
    if not api_token or api_token == "YOUR_API_KEY":
        print("❌ ERROR: SONNYLABS_API_TOKEN not found or invalid!")
        print("   This is expected if you haven't set up your .env file yet")
        return None, None
    
    if not analysis_id or analysis_id == "YOUR_ANALYSIS_ID":
        print("❌ ERROR: SONNYLABS_ANALYSIS_ID not found or invalid!")
        print("   This is expected if you haven't set up your .env file yet")
        return None, None
    
    return api_token, analysis_id

# Load environment variables
api_token, analysis_id = load_environment()

# Initialize the SonnyLabsClient with validated credentials
# NOTE: This will only work with REAL API credentials from your .env file
# The example values in this repository are not functional
if api_token and analysis_id:
    client = SonnyLabsClient(
        api_token=api_token,
        analysis_id=analysis_id,
        base_url="https://sonnylabs-service.onrender.com"
    )
    print("✅ SonnyLabs client initialized with valid credentials")
    print(f"⚠️  NOTE: Analysis ID {analysis_id} may not be configured for prompt injection scanning")
    print("   To get prompt_injection analysis, create a new analysis at:")
    print("   https://sonnylabs-service.onrender.com/analysis")
else:
    print("❌ Cannot initialize SonnyLabs client - missing credentials")
    print("   This is normal if you haven't set up your .env file with real credentials yet")
    client = None

# Create a FastMCP server instance with stateless configuration
mcp = FastMCP(
    "Language Analysis MCP Server",
    stateless_http=True  # Use stateless mode - no session IDs needed
)

def decode_base64(text: str) -> str:
    """Decode base64 encoded text"""
    try:
        return base64.b64decode(text).decode('utf-8')
    except:
        return text

def normalize_unicode(text: str) -> str:
    """Normalize unicode characters to detect evasion"""
    # 전각 문자를 반각으로 변환
    full_to_half = str.maketrans('ＳｙｓｔｅｍＯｖｅｒｒｉｄｅ', 'SystemOverride')
    return text.translate(full_to_half)

def extract_hex_strings(text: str) -> list:
    """Extract hex encoded strings"""
    import re
    hex_pattern = r'[0-9a-fA-F]{8,}'
    return re.findall(hex_pattern, text)

def advanced_sanitize_prompt(prompt: str) -> tuple[str, dict]:
    """Advanced prompt sanitization with attack detection"""
    
    original_prompt = prompt
    attack_indicators = []
    
    # 1. Base64 디코딩 시도
    try:
        decoded = decode_base64(prompt)
        if decoded != prompt:
            attack_indicators.append("base64_encoding")
            prompt = decoded
    except:
        pass
    
    # 2. 유니코드 정규화
    prompt = normalize_unicode(prompt)
    
    # 3. 16진수 문자열 추출
    hex_strings = extract_hex_strings(prompt)
    if hex_strings:
        attack_indicators.append("hex_encoding")
        for hex_str in hex_strings:
            try:
                decoded_hex = bytes.fromhex(hex_str).decode('utf-8')
                if any(keyword in decoded_hex.lower() for keyword in ['system', 'override', 'ignore']):
                    attack_indicators.append("hex_encoded_injection")
            except:
                pass
    
    # 4. 위험한 패턴 검사 (개선된 버전)
    dangerous_patterns = [
        (r'system\s*override', 'system_override'),
        (r'ignore\s+previous\s+instructions', 'ignore_instructions'),
        (r'os\.environ', 'os_environ_access'),
        (r'environment\s+variables', 'env_vars_access'),
        (r'api\s+token', 'api_token_request'),
        (r'api\s+key', 'api_key_request'),
        (r'password', 'password_request'),
        (r'secret', 'secret_request'),
        (r'credential', 'credential_request'),
        (r'<script', 'script_injection'),
        (r'javascript:', 'javascript_injection'),
        (r'data:text/html', 'data_url_injection'),
        (r'vbscript:', 'vbscript_injection'),
        (r'onload=', 'event_handler_injection'),
        (r'onerror=', 'event_handler_injection'),
        (r'onclick=', 'event_handler_injection'),
        (r'fetch\s*\(', 'fetch_request'),
        (r'xmlhttprequest', 'xhr_request'),
        (r'localstorage', 'storage_access'),
        (r'sessionstorage', 'storage_access'),
        (r'cookie', 'cookie_access'),
        (r'document\.', 'dom_access'),
        (r'window\.', 'window_access'),
        (r'location\.', 'location_access'),
        (r'history\.', 'history_access'),
        (r'navigator\.', 'navigator_access'),
        (r'screen\.', 'screen_access'),
        (r'innerhtml', 'innerhtml_injection'),
        (r'outerhtml', 'outerhtml_injection'),
        (r'eval\s*\(', 'eval_injection'),
        (r'setTimeout\s*\(', 'settimeout_injection'),
        (r'setInterval\s*\(', 'setinterval_injection'),
        (r'Function\s*\(', 'function_injection'),
        (r'constructor', 'constructor_injection'),
        (r'prototype', 'prototype_injection'),
        (r'__proto__', 'proto_injection'),
        (r'toString', 'tostring_injection'),
        (r'valueOf', 'valueof_injection'),
    ]
    
    for pattern, indicator in dangerous_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            attack_indicators.append(indicator)
            prompt = re.sub(pattern, '[REDACTED]', prompt, flags=re.IGNORECASE)
    
    # 5. 주석 제거 후 검사
    comment_removed = re.sub(r'/\*.*?\*/', '', prompt, flags=re.DOTALL)
    comment_removed = re.sub(r'//.*$', '', comment_removed, flags=re.MULTILINE)
    
    if comment_removed != prompt:
        attack_indicators.append("comment_evasion")
        prompt = comment_removed
    
    # 6. 공백 문자 정규화
    prompt = re.sub(r'\s+', ' ', prompt)
    
    # 7. 길이 제한
    if len(prompt) > 500:
        attack_indicators.append("excessive_length")
        prompt = prompt[:500] + "..."
    
    # 8. HTML 엔티티 이스케이프
    prompt = html.escape(prompt)
    
    # 공격 탐지 로깅
    if attack_indicators:
        security_logger.warning(f"Attack detected: {attack_indicators}")
        security_logger.warning(f"Original prompt: {original_prompt}")
        security_logger.warning(f"Sanitized prompt: {prompt}")
    
    return prompt, {
        "attack_detected": len(attack_indicators) > 0,
        "attack_indicators": attack_indicators,
        "original_length": len(original_prompt),
        "sanitized_length": len(prompt)
    }

def validate_prompt(prompt: str) -> tuple[bool, dict]:
    """Enhanced prompt validation with detailed analysis"""
    
    validation_result = {
        "is_safe": True,
        "reasons": [],
        "risk_level": "low"
    }
    
    # 빈 프롬프트 체크
    if not prompt or not prompt.strip():
        validation_result["is_safe"] = False
        validation_result["reasons"].append("empty_prompt")
        return False, validation_result
    
    # 위험한 키워드 체크 (확장된 목록)
    dangerous_keywords = [
        'system', 'override', 'ignore', 'previous', 'instructions',
        'os.environ', 'environment', 'variables', 'api', 'token',
        'password', 'secret', 'credential', 'script', 'javascript',
        'fetch', 'xmlhttprequest', 'localstorage', 'sessionstorage',
        'cookie', 'document', 'window', 'location', 'history',
        'navigator', 'screen', 'innerhtml', 'outerhtml', 'eval',
        'settimeout', 'setinterval', 'function', 'constructor',
        'prototype', '__proto__', 'tostring', 'valueof'
    ]
    
    prompt_lower = prompt.lower()
    found_keywords = []
    
    for keyword in dangerous_keywords:
        if keyword in prompt_lower:
            found_keywords.append(keyword)
    
    if found_keywords:
        validation_result["is_safe"] = False
        validation_result["reasons"].append(f"dangerous_keywords: {found_keywords}")
        validation_result["risk_level"] = "high"
    
    # 길이 체크
    if len(prompt) > 1000:
        validation_result["is_safe"] = False
        validation_result["reasons"].append("excessive_length")
        validation_result["risk_level"] = "medium"
    
    # 특수 문자 비율 체크
    special_chars = len(re.findall(r'[^a-zA-Z0-9가-힣\s.,!?]', prompt))
    if special_chars > len(prompt) * 0.3:  # 30% 이상이 특수문자
        validation_result["is_safe"] = False
        validation_result["reasons"].append("high_special_char_ratio")
        validation_result["risk_level"] = "medium"
    
    return validation_result["is_safe"], validation_result

@mcp.tool()
def analyze_text_prompt(prompt: str) -> dict:
    """
    Analyzes a text prompt after ensuring it is in English.
    If the prompt is not in English, it is translated before analysis.
    
    NOTE: This analysis ID is currently only configured for PII detection.
    To get prompt_injection analysis, create a new analysis with prompt injection enabled.
    """
    try:
        # Check if client is available
        if not client:
            return {"error": "SonnyLabs client not initialized - check API credentials"}
        
        # 고급 보안 검증
        is_safe, validation_result = validate_prompt(prompt)
        if not is_safe:
            security_logger.error(f"Unsafe prompt rejected: {validation_result}")
            return {
                "error": "Potentially unsafe input detected",
                "security_info": {
                    "risk_level": validation_result["risk_level"],
                    "reasons": validation_result["reasons"]
                }
            }
        
        # 고급 입력 sanitization
        sanitized_prompt, sanitization_result = advanced_sanitize_prompt(prompt)
        
        # 공격 탐지 시 추가 로깅
        if sanitization_result["attack_detected"]:
            security_logger.critical(f"Attack detected and sanitized: {sanitization_result}")
        
        # Detect the language of the input prompt
        language = detect(sanitized_prompt)
        print(f"Detected language: {language}")

        translated_prompt = sanitized_prompt
        # If the detected language is not English, translate it
        if language != 'en':
            print("Translating to English...")
            translated_prompt = GoogleTranslator(source='auto', target='en').translate(sanitized_prompt)
            print(f"Translated prompt: {translated_prompt}")

        # Analyze the English text using SonnyLabs (single API call)
        print("Analyzing with SonnyLabs...")
        input_result = client.analyze_text(translated_prompt, scan_type="input")
        
        # Check if we got a successful analysis
        if isinstance(input_result, dict) and input_result.get('success'):
            print("✅ SonnyLabs analysis successful!")
            analysis_data = input_result.get('analysis', [])
            
            # Check for prompt_injection specifically
            prompt_injection_found = any(
                item.get('name') == 'prompt_injection' 
                for item in analysis_data if isinstance(item, dict)
            )
            
            if not prompt_injection_found:
                print("⚠️  No prompt_injection analysis found - analysis ID may not support it")
                print("💡 To enable prompt_injection, create a new analysis at:")
                print("   https://sonnylabs-service.onrender.com/analysis")
        else:
            print(f"❌ SonnyLabs analysis failed: {input_result}")

        # 보안 정보와 함께 안전한 결과 반환
        safe_result = {
            "original_prompt": "[REDACTED]",  # 원본 프롬프트 숨김
            "detected_language": language,
            "translated_prompt": "[REDACTED]",  # 번역된 프롬프트 숨김
            "analysis_result": {
                "success": input_result.get('success', False),
                "analysis": input_result.get('analysis', [])
            },
            "security_info": {
                "attack_detected": sanitization_result["attack_detected"],
                "attack_indicators": sanitization_result["attack_indicators"],
                "validation_passed": is_safe,
                "risk_level": validation_result["risk_level"]
            }
        }

        return safe_result

    except Exception as e:
        security_logger.error(f"Analysis error: {e}")
        return {"error": "Analysis failed"}

if __name__ == "__main__":
    print("Starting Language Analysis MCP Server on http://127.0.0.1:8001 (STATELESS MODE)")
    print("⚠️  NOTE: Current analysis ID may not support prompt_injection scanning")
    print("   To enable prompt_injection analysis, create a new analysis at:")
    print("   https://sonnylabs-service.onrender.com/analysis")
    mcp.run(transport="http", host="127.0.0.1", port=8001)