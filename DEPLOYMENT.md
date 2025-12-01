# 🚀 Deployment Guide - Streamlit Cloud

This guide will help you deploy your Multi-Agent Study Platform to **Streamlit Cloud** (free hosting for Streamlit apps).

## Prerequisites

1. ✅ Your code is pushed to GitHub (already done!)
2. ✅ A GitHub account
3. ✅ An OpenAI API key

## Step-by-Step Deployment

### 1. Sign up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign in"** and authorize with your GitHub account
3. You'll be redirected to the Streamlit Cloud dashboard

### 2. Deploy Your App

1. Click **"New app"** button
2. Fill in the deployment form:
   - **Repository**: Select `BIPINSAPKOTA193/StudyMaterial-Generator`
   - **Branch**: `main`
   - **Main file path**: `src/ui/app.py`
   - **App URL**: Choose a unique name (e.g., `multiagent-study-platform`)

3. Click **"Deploy"**

### 3. Configure Environment Variables

**IMPORTANT**: You need to add your OpenAI API key as a secret.

1. In your app's settings (click the "⋮" menu → "Settings")
2. Go to **"Secrets"** tab
3. Add the following secrets:

```toml
OPENAI_API_KEY = "sk-your-actual-api-key-here"
OPENAI_MODEL = "gpt-4o-mini"
```

4. Click **"Save"**

### 4. Wait for Deployment

- Streamlit Cloud will automatically install dependencies from `requirements.txt`
- The first deployment may take 2-5 minutes
- You'll see build logs in real-time
- Once complete, your app will be live at: `https://your-app-name.streamlit.app`

## 📋 Important Notes

### File Paths
- All file paths in the code are relative, so they work in the cloud
- User data (state files, logs) will be stored in Streamlit Cloud's temporary storage
- **Note**: Data may be cleared on app restart (this is normal for free tier)

### Dependencies
Your `requirements.txt` includes all necessary packages. Streamlit Cloud will:
- Install Python 3.9+ automatically
- Install all packages from `requirements.txt`
- Download spaCy models automatically

### API Keys
- **Never commit API keys to GitHub!**
- Always use Streamlit Cloud's "Secrets" feature
- Your secrets are encrypted and only accessible to your app

### Resource Limits (Free Tier)
- Apps sleep after 1 hour of inactivity
- First request after sleep may take 30-60 seconds to wake up
- 1 GB RAM limit
- CPU time limits apply

## 🔧 Troubleshooting

### Build Fails
- Check that `requirements.txt` is correct
- Verify `src/ui/app.py` path is correct
- Check build logs for specific errors

### App Crashes
- Check Streamlit Cloud logs (in the app dashboard)
- Verify environment variables are set correctly
- Ensure OpenAI API key is valid

### Import Errors
- Make sure all Python files have proper imports
- Check that `src/` directory structure is correct
- Verify `__init__.py` files exist in all packages

### Slow Performance
- First load after sleep is slow (normal)
- Large PDFs may take time to process
- Consider optimizing chunk sizes for cloud deployment

## 🔄 Updating Your App

1. Push changes to your GitHub repository
2. Streamlit Cloud will automatically detect changes
3. Click **"Reboot app"** in the Streamlit Cloud dashboard
4. Or wait for automatic redeployment (may take a few minutes)

## 🌐 Alternative Deployment Options

If you need more control or resources:

1. **Heroku**: `heroku create` + `git push heroku main`
2. **Railway**: Connect GitHub repo, auto-deploys
3. **Render**: Connect GitHub repo, supports Python apps
4. **AWS/GCP/Azure**: Full cloud platforms (more setup required)

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Deployment Guide](https://docs.streamlit.io/deploy)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

---

**Your app URL will be**: `https://[your-app-name].streamlit.app`

Enjoy your deployed Multi-Agent Study Platform! 🎉

