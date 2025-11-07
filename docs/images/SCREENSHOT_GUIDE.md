# Screenshots Guide for SaijinOS

This guide helps you capture the essential screenshots for the project documentation.

## 📸 Required Screenshots

### 1. API Health Check Response
**File**: `api-health-check.png`
**What to capture**: 
- Start the SaijinOS server
- Open browser to `http://localhost:8000/health`
- Capture the JSON response showing system status

**Expected content**:
```json
{
  "status": "healthy",
  "components": {
    "ai_model": "active",
    "voice_system": "active", 
    "persona_manager": "active"
  }
}
```

### 2. FastAPI Swagger UI Documentation
**File**: `swagger-ui-docs.png`
**What to capture**:
- Navigate to `http://localhost:8000/docs`
- Capture the Swagger UI showing all API endpoints
- Include the expanded persona and voice endpoints

**Key elements to show**:
- SaijinOS API title and description
- List of endpoints (/api/personas, /api/voice, /health)
- Clean, professional appearance

## 🎯 Photography Tips

### Browser Settings
- Use Chrome or Edge for clean rendering
- Zoom to 100% for crisp text
- Hide bookmarks bar for cleaner look
- Use full-screen mode (F11) if needed

### Screenshot Quality
- **Resolution**: At least 1200px width
- **Format**: PNG for crisp text
- **Crop**: Include browser address bar to show localhost URL
- **Lighting**: Ensure good screen brightness

### Composition
- Center the content in the frame
- Include enough context (URL bar, page title)
- Avoid personal information in bookmarks/tabs
- Use clean, minimal browser appearance

## 📁 File Naming Convention

- `api-health-check.png` - Health endpoint JSON response
- `swagger-ui-docs.png` - FastAPI documentation interface
- Optional: `persona-chat-example.png` - Live chat interaction

## 🚀 Next Steps After Screenshots

1. Save images to `docs/images/` folder
2. Update README.md with image references:
   ```markdown
   ![API Health Check](docs/images/api-health-check.png)
   ![Swagger UI Documentation](docs/images/swagger-ui-docs.png)
   ```
3. Add images to git and push
4. Update release notes if needed

## 📱 Alternative: API Testing Screenshots

If the server isn't running, you can also capture:
- **Postman** requests to the API endpoints
- **cURL** command responses in terminal
- **Thunder Client** (VS Code extension) API calls

## 🎨 Image Optimization

After taking screenshots:
- Resize to reasonable dimensions (1200-1600px width max)
- Compress to keep file size under 500KB each
- Ensure text remains readable after compression

---

**Ready to capture those professional screenshots!** 📸✨