# 🚀 CAIO Translate - Deployment Guide for ChatGPT Apps

Complete step-by-step guide for deploying the CAIO Translate MCP Server and integrating it with ChatGPT Apps.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Deploy MCP Server](#deploy-mcp-server)
3. [Host Widget Files](#host-widget-files)
4. [Register with ChatGPT](#register-with-chatgpt)
5. [Testing & Verification](#testing--verification)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

**Total setup time: 15-20 minutes**

### What You'll Need
- Python 3.8+ (for local testing)
- A hosting platform account (Render, Railway, etc.)
- A CDN or static file hosting (Vercel, Netlify, GitHub Pages, etc.)
- ChatGPT Plus/Pro subscription
- Access to ChatGPT Apps builder

---

## Deploy MCP Server

### Step 1: Choose a Hosting Platform

#### Option A: Render (Recommended - Free tier available)

1. **Create account** at https://render.com
2. **Create new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Name: `caio-translate`
   - Environment: `Python 3`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python server/main.py`
   - Instance type: Free (or Starter for production)

3. **Configure environment**
   - No environment variables needed for basic setup
   - Advanced: Add `STORE_FILE=/tmp/store.json` for ephemeral storage

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Your server URL: `https://caio-translate.onrender.com`

---

#### Option B: Railway (Free tier available)

1. **Create account** at https://railway.app
2. **Create new project**
   - Click "New Project"
   - Select "GitHub Repo" and connect your repository
   - Railway auto-detects Python and installs dependencies

3. **Configure**
   - Add environment variable: `PYTHON_VERSION=3.11`
   - Start command: `python server/main.py`

4. **Deploy**
   - Railway auto-deploys on push
   - Your server URL: `https://caio-translate-production.up.railway.app`

---

#### Option C: Heroku (Paid tier required)

1. **Create account** at https://www.heroku.com
2. **Create Procfile** in project root:
   ```
   web: python server/main.py
   ```

3. **Deploy via CLI**
   ```bash
   heroku create caio-translate
   git push heroku main
   ```

4. **Your server URL**: `https://caio-translate.herokuapp.com`

---

#### Option D: AWS Lambda + API Gateway

1. **Create Lambda function**
   - Runtime: Python 3.11
   - Upload code as ZIP

2. **Create API Gateway**
   - HTTP API → Integration: Lambda
   - Deploy to stage

3. **Your server URL**: `https://your-api-id.lambda-url.region.on.aws/`

---

### Step 2: Verify Server Deployment

Test your deployed server:

```bash
# Test initialization
curl -X POST https://your-server-url/api/tools \
  -H "Content-Type: application/json" \
  -d '{"name": "caio-initialize", "arguments": {}}'

# Expected response:
# {
#   "status": "initialized",
#   "message": "CAIO Translate initialized successfully",
#   "settings": {"target_language": "English"},
#   "supported_languages": [...]
# }
```

---

## Host Widget Files

### Step 1: Choose a CDN/Static Hosting

#### Option A: Vercel (Recommended)

1. **Create account** at https://vercel.com
2. **Create new project**
   - Import your repository
   - Framework: Other
   - Root directory: `./`

3. **Configure**
   - Add `vercel.json`:
     ```json
     {
       "buildCommand": "echo 'No build needed'",
       "outputDirectory": ".",
       "public": true
     }
     ```

4. **Deploy**
   - Vercel auto-deploys on push
   - Widget URLs:
     - Translate: `https://your-project.vercel.app/widgets/translate/index.html`
     - Settings: `https://your-project.vercel.app/widgets/settings/index.html`

---

#### Option B: Netlify

1. **Create account** at https://netlify.com
2. **Connect repository**
   - Click "Add new site" → "Import an existing project"
   - Select your repo

3. **Configure**
   - Build command: (leave empty)
   - Publish directory: `.`

4. **Deploy**
   - Netlify auto-deploys
   - Widget URLs:
     - Translate: `https://your-site.netlify.app/widgets/translate/index.html`
     - Settings: `https://your-site.netlify.app/widgets/settings/index.html`

---

#### Option C: GitHub Pages

1. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: main branch / root

2. **Your URLs**
   - Translate: `https://your-username.github.io/caio_mcp_server/widgets/translate/index.html`
   - Settings: `https://your-username.github.io/caio_mcp_server/widgets/settings/index.html`

---

#### Option D: AWS S3 + CloudFront

1. **Create S3 bucket**
   - Enable static website hosting
   - Upload `widgets/` folder

2. **Create CloudFront distribution**
   - Origin: Your S3 bucket
   - Enable HTTPS

3. **Your URLs**
   - Translate: `https://d123456.cloudfront.net/widgets/translate/index.html`
   - Settings: `https://d123456.cloudfront.net/widgets/settings/index.html`

---

### Step 2: Verify Widget Hosting

Test your widget URLs in a browser:

```
https://your-cdn.com/widgets/translate/index.html
https://your-cdn.com/widgets/settings/index.html
```

Both should load without errors (they'll show initialization messages).

---

## Register with ChatGPT

### Step 1: Access ChatGPT Apps Builder

1. **Go to** https://chatgpt.com/gpts/editor
2. **Create new GPT** or edit existing one
3. **Click "Configure"** tab

---

### Step 2: Add MCP Server

1. **Scroll to "Custom Actions"**
2. **Click "Create new action"**
3. **Select "Model Context Protocol"**
4. **Enter your server URL**
   - Example: `https://caio-translate.onrender.com`
5. **Test connection**
   - ChatGPT will verify the server responds correctly
   - You should see a green checkmark

---

### Step 3: Register Widgets

1. **In Custom Actions, click "Add Widget"**
2. **Add Translate Widget**
   - Name: `caio-translate`
   - URL: `https://your-cdn.com/widgets/translate/index.html`
   - Type: `Interactive`

3. **Add Settings Widget**
   - Name: `caio-settings`
   - URL: `https://your-cdn.com/widgets/settings/index.html`
   - Type: `Configuration`

4. **Save Configuration**
   - Click "Save" and wait for deployment

---

### Step 4: Test Integration

1. **In the chat**, ask:
   ```
   Translate "Hello world" to Arabic
   ```

2. **Expected behavior**
   - ChatGPT calls the `caio-translate` tool
   - The translate widget appears below the response
   - Widget shows translation and action buttons

3. **Test settings**
   - Click the language dropdown in the widget
   - Settings widget should appear
   - Change language and save

---

## Testing & Verification

### Comprehensive Test Checklist

- [ ] Server responds to `caio-initialize` tool
- [ ] Server responds to `caio-translate` tool
- [ ] Server responds to `caio-update-settings` tool
- [ ] Settings are persisted (restart server and verify)
- [ ] Translate widget loads without errors
- [ ] Settings widget loads without errors
- [ ] Copy button works in translate widget
- [ ] Save button works in translate widget
- [ ] Language dropdown works in translate widget
- [ ] Settings save in settings widget
- [ ] ChatGPT recognizes and calls tools
- [ ] Widgets appear in ChatGPT conversation
- [ ] All buttons are clickable and responsive

---

### Test Scenarios

#### Scenario 1: Basic Translation
```
User: "Translate 'Good morning' to Spanish"
Expected: Widget appears with translation
```

#### Scenario 2: Language Change
```
User: "Change target language to French"
Expected: Settings widget appears, language updates
```

#### Scenario 3: Save Translation
```
User: "Translate 'Thank you' to German and save it"
Expected: Translation appears, save button works
```

#### Scenario 4: Multiple Languages
```
User: "Translate to Arabic, French, and Spanish"
Expected: Multiple translations shown, each with widget
```

---

## Troubleshooting

### Server Issues

#### Problem: "Server not responding"
**Solution:**
1. Check server URL is correct
2. Verify server is running: `curl https://your-server-url`
3. Check server logs for errors
4. Restart server deployment

#### Problem: "Tool not found"
**Solution:**
1. Verify tool name matches exactly: `caio-translate`, `caio-initialize`, etc.
2. Check server has latest code deployed
3. Redeploy server

#### Problem: "Settings not persisting"
**Solution:**
1. Check server has write permissions to `store.json`
2. For ephemeral storage (Lambda, etc.), use database instead
3. Check file path in environment variables

---

### Widget Issues

#### Problem: "Widget fails to load"
**Solution:**
1. Check widget URL is accessible in browser
2. Check CORS headers are correct
3. Verify widget HTML has no syntax errors
4. Check browser console for JavaScript errors

#### Problem: "Widget can't communicate with server"
**Solution:**
1. Check server URL in widget RPC calls
2. Verify postMessage protocol is correct
3. Check browser console for network errors
4. Ensure server CORS allows widget origin

#### Problem: "Buttons don't work"
**Solution:**
1. Check JavaScript is enabled
2. Verify event listeners are attached
3. Check browser console for errors
4. Test in different browser

---

### ChatGPT Integration Issues

#### Problem: "Tool not appearing in ChatGPT"
**Solution:**
1. Verify MCP server URL is correct
2. Test tool manually: `curl -X POST https://server-url/api/tools`
3. Check ChatGPT configuration saved
4. Try refreshing ChatGPT page
5. Clear browser cache

#### Problem: "Widget not appearing in chat"
**Solution:**
1. Verify widget URLs are registered
2. Check widget URLs are publicly accessible
3. Verify tool returns correct widget metadata
4. Check ChatGPT console for widget loading errors

#### Problem: "Tool calls fail with error"
**Solution:**
1. Check tool arguments match schema
2. Verify server handles arguments correctly
3. Check server logs for detailed error
4. Test tool with curl to isolate issue

---

### Performance Issues

#### Problem: "Slow response time"
**Solution:**
1. Check server CPU/memory usage
2. Upgrade hosting tier if needed
3. Add caching layer (Redis, etc.)
4. Optimize database queries

#### Problem: "Widget loads slowly"
**Solution:**
1. Minimize widget HTML/CSS/JS
2. Use CDN for widget files
3. Enable gzip compression
4. Optimize images

---

## Advanced Configuration

### Environment Variables

```bash
# Server configuration
STORE_FILE=/tmp/store.json          # Store location
LOG_LEVEL=INFO                      # Logging level
PORT=8000                           # Server port
DEBUG=false                         # Debug mode

# API configuration
API_TIMEOUT=30                      # Request timeout (seconds)
MAX_TRANSLATION_LENGTH=5000         # Max text length
```

### Database Backend (Optional)

For production with multiple instances:

```python
# Replace store.py with database adapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/caio"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

### Real Translation API Integration

```python
# In main.py, replace placeholder translation
from google.cloud import translate_v2

def translate_text(text, target_language):
    client = translate_v2.Client()
    result = client.translate_text(
        source_language='en',
        target_language=LANGUAGE_CODES[target_language],
        values=[text]
    )
    return result['translations'][0]['translatedText']
```

---

## Support & Resources

- **MCP Documentation**: https://modelcontextprotocol.io
- **ChatGPT Apps Guide**: https://platform.openai.com/docs/guides/gpts
- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app

---

**Last Updated:** July 19, 2026  
**Version:** 1.0.0
