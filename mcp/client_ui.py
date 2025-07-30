# client_ui.py
import streamlit as st
import requests
import json
import re

st.set_page_config(page_title="Language Analysis Client", layout="centered")
st.title("Language Analysis MCP Client")

# Server URL
BASE_URL = "http://localhost:8001"

def parse_sse_response(response_text):
    """Parse Server-Sent Events response to extract JSON data"""
    try:
        # Look for data lines in SSE format
        data_lines = re.findall(r'data: (.+)', response_text)
        if data_lines:
            # Take the last data line (most recent)
            json_str = data_lines[-1].strip()
            return json.loads(json_str)
        else:
            # If no SSE format, try parsing as regular JSON
            return json.loads(response_text)
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse response: {e}")
        st.code(response_text)
        return None

prompt = st.text_area("Enter text to analyze:", height=150, placeholder="Type your text here...")

def send_request(endpoint, payload):
    """Send request without session ID (stateless mode)"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream, application/json",
    }
    
    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=30
        )
        return response
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

if st.button("Analyze", type="primary"):
    if not prompt.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing text..."):
            # Test server connectivity first
            try:
                test_response = requests.get(f"{BASE_URL}/health", timeout=5)
                st.success("✅ Server is reachable")
            except:
                try:
                    test_response = requests.get(BASE_URL, timeout=5)
                    st.success("✅ Server is running")
                except:
                    st.error("❌ Cannot connect to server. Make sure it's running on localhost:8001")
                    st.stop()
            
            # Use the correct FastMCP endpoint pattern
            endpoint = f"{BASE_URL}/mcp/tools/call"
            payload = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "analyze_text_prompt",
                    "arguments": {"prompt": prompt.strip()}
                },
                "id": 1
            }
            
            response = send_request(endpoint, payload)
            
            if response and response.status_code == 200:
                try:
                    # Parse SSE response to get JSON data
                    result = parse_sse_response(response.text)
                    if result:
                        st.success("✅ Analysis complete!")
                        st.json(result)
                    else:
                        st.error("Failed to parse server response")
                except Exception as e:
                    st.error(f"Failed to parse response: {e}")
                    st.code(response.text)
            elif response:
                st.error(f"Server returned error {response.status_code}: {response.text}")

if st.button("Send JSON-RPC initialize", type="secondary"):
    endpoint = f"{BASE_URL}/mcp/initialize"
    payload = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {},
        "id": 1
    }
    
    response = send_request(endpoint, payload)
    
    if response and response.status_code == 200:
        try:
            result = parse_sse_response(response.text)
            if result:
                st.success("✅ Initialization succeeded!")
                st.json(result)
            else:
                st.error("Failed to parse initialization response")
        except Exception as e:
            st.error(f"Failed to parse response: {e}")
            st.code(response.text)
    elif response:
        st.error(f"Initialization failed: {response.status_code} - {response.text}")

st.markdown("---")
st.caption("Powered by FastMCP, SonnyLabs, and Streamlit")