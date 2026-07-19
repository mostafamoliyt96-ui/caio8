# ⚡ CAIO Translate - Quick Start (5 Minutes)

**Get CAIO Translate running in 5 minutes!**

---

## 🚀 Option 1: Local Testing (Right Now)

### Step 1: Install Dependencies
```bash
cd caio_mcp_server
pip install -r requirements.txt
```

### Step 2: Run the Server
```bash
python server/main.py
```

**Expected Output:**
```
[MCP Server] Starting CAIO Translate...
[MCP Server] Listening on stdin/stdout
```

### Step 3: Test in Another Terminal
```bash
# Test initialization
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"name": "caio-initialize", "arguments": {}}'
```

✅ **Done!** Your MCP server is running locally.

---

## 🌐 Option 2: Deploy to Render (10 Minutes)

### Step 1: Push to GitHub
```bash
cd caio_mcp_server
git init
git add .
git commit -m "CAIO Translate MCP Server"
git remote add origin https://github.com/YOUR_USERNAME/caio_mcp_server.git
git push -u origin main
```

### Step 2: Create Render Account
- Go to https://render.com
- Sign up with GitHub
- Click "New +" → "Web Service"
- Select your repository

### Step 3: Configure
- **Name:** `caio-translate`
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python server/main.py`
- **Instance Type:** Free

### Step 4: Deploy
- Click "Create Web Service"
- Wait 2-3 minutes
- Get your URL: `https://caio-translate.onrender.com`

✅ **Done!** Your server is live on the internet.

---

## 🔌 Option 3: Register with ChatGPT (5 Minutes)

### Step 1: Open ChatGPT Apps Editor
- Go to https://chatgpt.com/gpts/editor
- Create new GPT or edit existing

### Step 2: Add MCP Server
1. Click "Configure" tab
2. Scroll to "Custom Actions"
3. Click "Create new action"
4. Select "Model Context Protocol"
5. Enter your server URL:
   ```
   https://caio-translate.onrender.com
   ```
6. Click "Test Connection" (should show ✅)

### Step 3: Register Widgets
1. Click "Add Widget"
2. **For Translate Widget:**
   - Name: `caio-translate`
   - URL: `https://your-cdn.com/widgets/translate/index.html`
3. **For Settings Widget:**
   - Name: `caio-settings`
   - URL: `https://your-cdn.com/widgets/settings/index.html`

### Step 4: Save & Test
- Click "Save Configuration"
- In chat, ask: "Translate 'Hello world' to Arabic"
- Widget should appear!

✅ **Done!** CAIO Translate is integrated with ChatGPT!

---

## 📋 File Structure Reference

```
caio_mcp_server/
├── server/                      # MCP Server code
│   ├── main.py                 # Main server (8 tools)
│   ├── store.py                # Data persistence
│   ├── languages.py            # Language definitions
│   └── widget_router.py        # Widget data routing
├── widgets/                     # Interactive widgets
│   ├── translate/index.html    # Translation widget
│   └── settings/index.html     # Settings widget
├── README.md                    # Full documentation
├── DEPLOYMENT_GUIDE.md          # Detailed deployment
├── CHATGPT_INTEGRATION.md       # ChatGPT setup
└── requirements.txt             # Python dependencies
```

---

## 🛠 Available Tools

Your MCP server provides 8 tools:

| Tool | Purpose |
|------|---------|
| `caio-initialize` | Initialize app |
| `caio-translate` | Translate text |
| `caio-update-settings` | Change language |
| `caio-get-settings` | Get current settings |
| `caio-save` | Save translation |
| `caio-get-saved-translations` | Get saved items |
| `caio-get-ai-recommendations` | Get learning suggestions |
| `caio-get-word-builder` | Word building game |

---

## 🎯 Supported Languages

**Translation:** All languages supported by ChatGPT (unlimited)

**Full Features (Word Builder, Sentence Builder):**
- English, Arabic, French, German, Spanish, Italian, Russian, Turkish

**Translation + Alternative Activities:**
- Japanese, Chinese, Korean, Thai, and other non-alphabetic languages

**Note:** See [LANGUAGE_SUPPORT.md](LANGUAGE_SUPPORT.md) for comprehensive language documentation

---

## 🔗 Important Links

| Resource | Link |
|----------|------|
| **Full README** | `README.md` |
| **Deployment Guide** | `DEPLOYMENT_GUIDE.md` |
| **ChatGPT Integration** | `CHATGPT_INTEGRATION.md` |
| **Project Summary** | `PROJECT_SUMMARY.md` |
| **MCP Spec** | https://modelcontextprotocol.io |
| **ChatGPT Apps** | https://chatgpt.com/gpts/editor |

---

## ❓ Troubleshooting

### Server won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Try again
python server/main.py
```

### Can't deploy to Render
- Verify GitHub repository is public
- Check `requirements.txt` exists
- Verify Python files have no syntax errors

### ChatGPT can't find tools
- Test server URL directly: `curl https://your-server-url`
- Verify MCP server is running
- Check ChatGPT configuration saved

---

## 📞 Need Help?

1. **Read full docs:** `README.md`
2. **Check deployment:** `DEPLOYMENT_GUIDE.md`
3. **Review integration:** `CHATGPT_INTEGRATION.md`
4. **See examples:** `PROJECT_SUMMARY.md`

---

## ✅ Checklist

- [ ] Installed dependencies
- [ ] Server runs locally
- [ ] Deployed to hosting platform
- [ ] Got server URL
- [ ] Registered with ChatGPT
- [ ] Tested translation
- [ ] Widget appears in chat
- [ ] Settings work
- [ ] Save button works

---

**You're all set! 🎉**

Next: Read `DEPLOYMENT_GUIDE.md` for production setup.

---

**Last Updated:** July 19, 2026  
**Version:** 1.0.0
