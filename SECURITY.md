# Security Configuration Guide

## ⚠️ Important Security Notice

This repository contains **example API keys and configuration values that are NOT valid**. These are placeholder values for demonstration purposes only.

### What's in the Repository

- Example API keys and tokens (NOT functional)
- Placeholder configuration values
- Code structure for demonstration

### What's NOT in the Repository

- Real API credentials
- Valid API keys
- Production-ready configuration

## 🔐 Setting Up Your Environment

### 1. Create a .env File

Create a `.env` file in the project root with your real credentials:

```bash
# .env file (create this file with your real credentials)
SONNYLABS_API_TOKEN=your_real_api_token_here
SONNYLABS_ANALYSIS_ID=your_real_analysis_id_here
```

### 2. Get Real API Credentials

1. Go to [SonnyLabs Service](https://sonnylabs-service.onrender.com/analysis)
2. Create a new analysis with prompt injection scanning enabled
3. Get your API token and analysis ID
4. Add them to your `.env` file

### 3. Never Commit Sensitive Data

- ✅ The `.gitignore` file is configured to exclude `.env` files
- ✅ Never commit real API keys to version control
- ✅ Use environment variables for all sensitive data

## 🛡️ Security Best Practices

1. **Environment Variables**: Always use `.env` files for sensitive data
2. **Git Ignore**: The `.gitignore` file prevents accidental commits of sensitive files
3. **Example Values**: Any API keys in the code are examples only
4. **Regular Rotation**: Rotate your API keys regularly
5. **Access Control**: Limit access to your API credentials

## 🔍 What to Look For

If you see any of these in the code, they are examples only:
- `YOUR_API_KEY`
- `YOUR_ANALYSIS_ID`
- Any other placeholder values

## 🚨 If You Accidentally Committed Real Keys

1. **Immediately revoke the exposed keys**
2. **Generate new keys**
3. **Update your `.env` file with the new keys**
4. **Consider the old keys compromised**

## 📝 Code Comments

The code includes warning comments to indicate:
- Which values are examples
- Where real credentials should be used
- How to properly configure the environment

## 🔧 Troubleshooting

If you see error messages about missing credentials:
- This is expected if you haven't set up your `.env` file yet
- Create a `.env` file with your real credentials
- The example values in the code are not functional

## 📞 Support

If you need help setting up your environment or have security concerns:
1. Check the main README.md for setup instructions
2. Ensure your `.env` file is properly configured
3. Verify that your API credentials are valid 