# 🤖 ChatGPT Apps Integration Guide

Complete guide for integrating CAIO Translate with ChatGPT Apps using the Model Context Protocol (MCP).

---

## Overview

CAIO Translate is built as an **MCP Server** that integrates seamlessly with ChatGPT Apps. The integration allows ChatGPT to:

1. **Call translation tools** directly from conversations
2. **Render interactive widgets** for user interaction
3. **Persist user settings** across conversations
4. **Provide AI recommendations** for learning

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ChatGPT Apps                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  User Conversation                              │   │
│  │  "Translate 'Hello' to Arabic"                  │   │
│  └──────────────────────────────────────────────────┘   │
│                         ↓                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │  MCP Client (ChatGPT)                           │   │
│  │  - Calls: caio-translate                        │   │
│  │  - Passes: {text: "Hello"}                      │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         ↓ (HTTP/WebSocket)
┌─────────────────────────────────────────────────────────┐
│              CAIO MCP Server (Python)                   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Tool Handlers                                  │   │
│  │  - caio-initialize                              │   │
│  │  - caio-translate                               │   │
│  │  - caio-update-settings                         │   │
│  │  - caio-save                                    │   │
│  │  - caio-get-ai-recommendations                  │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Data Layer                                     │   │
│  │  - store.py (JSON persistence)                  │   │
│  │  - languages.py (Language definitions)          │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              Widget Hosting (CDN)                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  /widgets/translate/index.html                  │   │
│  │  /widgets/settings/index.html                   │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              ChatGPT Interface                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  🌍 CAIO Translate Widget                       │   │
│  │  ┌────────────────────────────────────────────┐ │   │
│  │  │ Target: Arabic ▼                           │ │   │
│  │  │ [Paste text...]                            │ │   │
│  │  │ [Translate]                                │ │   │
│  │  │ ────────────────────────────────────────── │ │   │
│  │  │ Translation: مرحبا                         │ │   │
│  │  │ [Copy] [Save] [Clear]                      │ │   │
│  │  └────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Integration

### Phase 1: Prepare Your MCP Server

1. **Deploy server** (see DEPLOYMENT_GUIDE.md)
   - Get your server URL: `https://your-server.com`

2. **Verify server is running**
   ```bash
   curl https://your-server.com/api/tools
   ```

3. **Test a tool call**
   ```bash
   curl -X POST https://your-server.com/api/tools \
     -H "Content-Type: application/json" \
     -d '{"name": "caio-initialize", "arguments": {}}'
   ```

---

### Phase 2: Host Widget Files

1. **Deploy widgets** to CDN (see DEPLOYMENT_GUIDE.md)
   - Translate widget: `https://your-cdn.com/widgets/translate/index.html`
   - Settings widget: `https://your-cdn.com/widgets/settings/index.html`

2. **Verify widgets load**
   - Open URLs in browser
   - Check browser console for errors

---

### Phase 3: Register with ChatGPT

#### Step 1: Access GPT Editor

1. Go to https://chatgpt.com/gpts/editor
2. Click "Create a GPT" or edit existing GPT
3. Click "Configure" tab

#### Step 2: Add Custom Action (MCP Server)

1. Scroll down to **"Custom Actions"** section
2. Click **"Create new action"**
3. Select **"Model Context Protocol"**
4. Enter your server URL:
   ```
   https://your-server.com
   ```
5. Click **"Test Connection"**
   - Should show green checkmark
   - If fails, verify server is running

#### Step 3: Configure Tool Visibility

1. In the same Custom Actions section, configure which tools ChatGPT can use:
   - ✓ `caio-initialize` - Enable
   - ✓ `caio-translate` - Enable
   - ✓ `caio-update-settings` - Enable
   - ✓ `caio-save` - Enable
   - ✓ `caio-get-ai-recommendations` - Enable
   - ✓ `caio-get-word-builder` - Enable
   - ✓ `caio-get-sentence-builder` - Enable

#### Step 4: Register Widgets

1. Click **"Add Widget"** in Custom Actions
2. **Add Translate Widget**
   - Name: `caio-translate`
   - URL: `https://your-cdn.com/widgets/translate/index.html`
   - Trigger: Automatic (when tool returns widget data)

3. **Add Settings Widget**
   - Name: `caio-settings`
   - URL: `https://your-cdn.com/widgets/settings/index.html`
   - Trigger: On-demand (user clicks settings)

4. Click **"Save Configuration"**

---

### Phase 4: Test Integration

#### Test 1: Basic Translation

```
User: "Translate 'Good morning' to Spanish"

Expected:
1. ChatGPT calls caio-translate tool
2. Server returns translation
3. Translate widget appears with result
4. User can copy, save, or clear
```

#### Test 2: Settings Update

```
User: "Change my translation language to French"

Expected:
1. ChatGPT calls caio-update-settings tool
2. Settings widget appears
3. User selects French
4. Settings are saved
5. Future translations use French
```

#### Test 3: Save Translation

```
User: "Translate 'Thank you' to German and save it"

Expected:
1. Translation appears in widget
2. User clicks Save button
3. caio-save tool is called
4. Success message appears
```

#### Test 4: AI Recommendations

```
User: "Translate this paragraph and show me words to learn"

Expected:
1. Translation appears
2. AI recommendations section shows below
3. Each recommendation has a Learn button
4. Clicking Learn opens word builder
```

---

## Protocol Details

### MCP Server Initialization

When ChatGPT connects to your MCP server:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2026-01-26",
    "capabilities": {},
    "clientInfo": {
      "name": "ChatGPT",
      "version": "1.0.0"
    }
  }
}
```

Your server responds:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2026-01-26",
    "capabilities": {},
    "serverInfo": {
      "name": "caio-translate",
      "version": "1.0.0"
    }
  }
}
```

---

### Tool Call Flow

#### 1. ChatGPT Lists Available Tools

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

Server responds with all available tools (see API Reference in README.md).

#### 2. ChatGPT Calls a Tool

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "caio-translate",
    "arguments": {
      "text": "Hello world",
      "target_language": "Arabic"
    }
  }
}
```

#### 3. Server Returns Result

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "type": "text",
    "text": "{\"status\": \"success\", \"translation\": \"...\"}"
  }
}
```

#### 4. ChatGPT Renders Widget (if included)

If the result includes widget metadata:

```json
{
  "widget": {
    "type": "translate",
    "data": {
      "translation": "مرحبا بالعالم",
      "original": "Hello world",
      "target_language": "Arabic"
    }
  }
}
```

ChatGPT loads and renders the widget HTML.

---

## Widget Communication

### Widget-to-Server Communication

Widgets communicate with the MCP server via **postMessage** and **JSON-RPC 2.0**:

```javascript
// Widget sends request to server
window.parent.postMessage({
  jsonrpc: "2.0",
  id: 1,
  method: "tools/call",
  params: {
    name: "caio-translate",
    arguments: { text: "Hello" }
  }
}, "*");

// Server sends response
window.addEventListener("message", (event) => {
  const response = event.data;
  // {
  //   jsonrpc: "2.0",
  //   id: 1,
  //   result: { ... }
  // }
});
```

### Widget Lifecycle

```
1. Widget HTML loads in iframe
2. Widget initializes via postMessage
3. Widget registers with MCP server
4. User interacts with widget
5. Widget calls tools via postMessage
6. Server processes and returns result
7. Widget updates UI with result
8. User can copy, save, or take further action
```

---

## Best Practices

### For Tool Implementation

1. **Always return valid JSON**
   ```python
   return [types.TextContent(type="text", text=json.dumps(response))]
   ```

2. **Include widget metadata when relevant**
   ```python
   response = {
       "status": "success",
       "result": "...",
       "widget": {
           "type": "translate",
           "data": {...}
       }
   }
   ```

3. **Handle errors gracefully**
   ```python
   response = {
       "status": "error",
       "error": "Invalid language",
       "supported": SUPPORTED_LANGUAGES
   }
   ```

4. **Validate all inputs**
   ```python
   if not is_valid_language(target_language):
       return error_response()
   ```

### For Widget Implementation

1. **Always initialize with server**
   ```javascript
   await rpcRequest("ui/initialize", {...});
   ```

2. **Handle loading states**
   ```javascript
   setLoading(true);
   try {
       const result = await rpcRequest("tools/call", {...});
   } finally {
       setLoading(false);
   }
   ```

3. **Show user feedback**
   ```javascript
   showStatus("Translation completed!", "success");
   ```

4. **Gracefully handle errors**
   ```javascript
   catch (error) {
       showStatus("Error: " + error.message, "error");
   }
   ```

---

## Troubleshooting

### ChatGPT Can't Find Tools

**Problem:** ChatGPT says "Tool not found"

**Solution:**
1. Verify tool name matches exactly (case-sensitive)
2. Check server is running and responding
3. Verify tool is in the list returned by `tools/list`
4. Restart ChatGPT conversation

### Widget Doesn't Appear

**Problem:** Tool works but widget doesn't show

**Solution:**
1. Verify widget URL is registered in ChatGPT settings
2. Test widget URL in browser - should load
3. Check widget includes widget metadata in response
4. Verify widget HTML has no syntax errors

### Widget Can't Call Server

**Problem:** Widget loads but buttons don't work

**Solution:**
1. Check browser console for errors
2. Verify postMessage protocol is correct
3. Test RPC communication manually
4. Check server logs for failed requests

### Settings Don't Persist

**Problem:** Settings change but don't save

**Solution:**
1. Verify store.py has write permissions
2. Check `store.json` file exists and is writable
3. Verify `caio-update-settings` tool is called
4. Check server logs for save errors

---

## Advanced Features

### Custom Tool Integration

Add new tools to extend functionality:

```python
@app.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="caio-custom-tool",
            description="Your custom tool",
            inputSchema={...}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "caio-custom-tool":
        return await handle_custom_tool(arguments)
```

### Custom Widget Integration

Create new widgets for specialized features:

```html
<!-- custom-widget/index.html -->
<script type="module">
    const rpcRequest = (method, params) => {
        return new Promise((resolve, reject) => {
            window.parent.postMessage({
                jsonrpc: "2.0",
                id: ++rpcId,
                method,
                params
            }, "*");
        });
    };
    
    // Your widget logic here
</script>
```

### Real-Time Updates

Use WebSocket for real-time tool result streaming:

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "caio-stream-translation":
        # Stream translation chunks
        for chunk in translate_stream(arguments["text"]):
            yield types.TextContent(type="text", text=chunk)
```

---

## Performance Optimization

### Server-Side

1. **Cache language lists**
   ```python
   SUPPORTED_LANGUAGES_CACHE = SUPPORTED_LANGUAGES
   ```

2. **Use async operations**
   ```python
   async def handle_translate(arguments):
       # Non-blocking operations
   ```

3. **Implement rate limiting**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

### Widget-Side

1. **Minimize bundle size**
   - No external dependencies
   - Inline CSS
   - Minify JavaScript

2. **Optimize rendering**
   - Use CSS animations instead of JavaScript
   - Debounce input handlers
   - Lazy load content

3. **Cache responses**
   ```javascript
   const cache = new Map();
   if (cache.has(key)) return cache.get(key);
   ```

---

## Security Considerations

1. **Validate all inputs** on server
2. **Sanitize HTML** in widgets
3. **Use HTTPS** for all communication
4. **Implement CORS** properly
5. **Limit request size** to prevent abuse
6. **Rate limit** tool calls
7. **Log all activities** for monitoring

---

## Monitoring & Debugging

### Server Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Tool called: {name}")
logger.error(f"Error: {error}")
```

### Widget Debugging

```javascript
// Enable debug logging
const DEBUG = true;

function log(message, data) {
    if (DEBUG) {
        console.log(`[CAIO] ${message}`, data);
    }
}
```

### ChatGPT Debugging

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for messages from widgets
4. Check Network tab for RPC calls

---

## Support Resources

- **MCP Spec**: https://modelcontextprotocol.io/specification
- **ChatGPT Docs**: https://platform.openai.com/docs/guides/gpts
- **JSON-RPC 2.0**: https://www.jsonrpc.org/specification
- **postMessage API**: https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage

---

**Last Updated:** July 19, 2026  
**Version:** 1.0.0
