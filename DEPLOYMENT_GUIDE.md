# 🚀 Complete Deployment Guide

This guide will help you deploy your Multi-Agent Study Platform to **Streamlit Cloud** with Supabase integration.

## ✅ Prerequisites

1. ✅ Your code is pushed to GitHub
2. ✅ A GitHub account
3. ✅ An OpenAI API key
4. ✅ A Supabase account (already set up!)
5. ✅ Supabase project URL and API key

---

## 📋 Step-by-Step Deployment

### Step 1: Push Code to GitHub

Make sure all your code is committed and pushed to GitHub:

```bash
git add .
git commit -m "Ready for deployment with Supabase"
git push origin main
```

### Step 2: Sign up for Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"Sign in"** and authorize with your GitHub account
3. You'll be redirected to the Streamlit Cloud dashboard

### Step 3: Deploy Your App

1. Click **"New app"** button (or "Deploy an app" if first time)
2. Fill in the deployment form:
   - **Repository**: Select your repository (e.g., `BIPINSAPKOTA193/StudyMaterial-Generator`)
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `src/ui/app.py`
   - **App URL**: Choose a unique name (e.g., `multiagent-study-platform`)

3. Click **"Deploy"**

### Step 4: Configure Secrets (CRITICAL!)

**This is the most important step!** You need to add your API keys and Supabase credentials.

1. In your app's dashboard, click the **"⋮"** (three dots) menu → **"Settings"**
2. Go to the **"Secrets"** tab
3. Add the following secrets:

```toml
# OpenAI Configuration
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
OPENAI_MODEL = "gpt-4o-mini"

# Supabase Configuration
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-key-here"
```

**OR if you have PostgreSQL connection string:**

```toml
# OpenAI Configuration
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
OPENAI_MODEL = "gpt-4o-mini"

# Supabase Configuration (PostgreSQL URL will be auto-converted)
SUPABASE_URL = "postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres"
SUPABASE_KEY = "your-anon-key-here"
```

4. Click **"Save"**

**Where to find your Supabase credentials:**
- Go to your Supabase project dashboard
- Navigate to **Settings** → **API**
- Copy:
  - **Project URL** → use as `SUPABASE_URL` (or use PostgreSQL connection string)
  - **anon public** key → use as `SUPABASE_KEY`

### Step 5: Wait for Deployment

- Streamlit Cloud will automatically:
  - Install Python 3.9+
  - Install all packages from `requirements.txt`
  - Download spaCy models
  - Build your app

- The first deployment may take **3-5 minutes**
- You'll see build logs in real-time
- Watch for any errors in the logs

### Step 6: Verify Deployment

Once deployment completes:

1. **Check the app URL**: `https://your-app-name.streamlit.app`
2. **Test the app**:
   - Register a new user
   - Upload a file
   - Answer some questions
   - Check analytics dashboard
3. **Verify Supabase**:
   - Go to your Supabase dashboard
   - Check `users` table - should see your new user
   - Check `rl_state` table - should see analytics data

---

## 🔧 Configuration Details

### Secrets Format

In Streamlit Cloud, secrets are stored in TOML format. The secrets you add will be accessible in your app via `st.secrets`.

Your app automatically reads:
- `st.secrets.get("OPENAI_API_KEY")` or `os.getenv("OPENAI_API_KEY")`
- `st.secrets.get("SUPABASE_URL")` or `os.getenv("SUPABASE_URL")`
- `st.secrets.get("SUPABASE_KEY")` or `os.getenv("SUPABASE_KEY")`

### File Structure

Your app expects this structure:
```
QuizGenerator/
├── src/
│   ├── ui/
│   │   └── app.py          ← Main entry point
│   ├── core/
│   ├── agents/
│   └── tools/
├── requirements.txt
└── .streamlit/
    └── config.toml
```

### Dependencies

All dependencies are in `requirements.txt`. Streamlit Cloud will install:
- streamlit
- openai
- supabase
- spacy
- transformers
- torch
- pypdf
- plotly
- And all other dependencies

---

## 🐛 Troubleshooting

### Build Fails

**Problem**: Build fails during deployment

**Solutions**:
- Check `requirements.txt` is correct
- Verify `src/ui/app.py` path is correct
- Check build logs for specific errors
- Ensure all imports are correct

### App Crashes on Startup

**Problem**: App crashes when you open it

**Solutions**:
- Check Streamlit Cloud logs (in app dashboard)
- Verify all secrets are set correctly
- Ensure OpenAI API key is valid
- Check Supabase credentials are correct

### Supabase Connection Errors

**Problem**: "Could not connect to Supabase" errors

**Solutions**:
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in secrets
- Check Supabase project is active
- Ensure tables are created (run `supabase_setup.sql`)
- Check Supabase dashboard for connection issues

### Import Errors

**Problem**: "Module not found" errors

**Solutions**:
- Verify `src/` directory structure is correct
- Check `__init__.py` files exist in all packages
- Ensure all dependencies are in `requirements.txt`

### Data Not Persisting

**Problem**: Data disappears after app restart

**Solutions**:
- Verify Supabase secrets are configured
- Check Supabase dashboard to see if data is being saved
- Look for errors in Streamlit Cloud logs
- Ensure `save_state()` is being called after data changes

### Slow Performance

**Problem**: App is slow to load or respond

**Solutions**:
- First load after sleep is slow (normal for free tier)
- Large PDFs take time to process (expected)
- Check Streamlit Cloud logs for timeout errors
- Consider optimizing chunk sizes

---

## 🔄 Updating Your App

After making changes:

1. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```

2. **Streamlit Cloud will automatically detect changes**:
   - Go to your app dashboard
   - Click **"Reboot app"** to force immediate update
   - Or wait for automatic redeployment (may take a few minutes)

3. **Verify the update**:
   - Check the app URL
   - Test the new features
   - Monitor logs for errors

---

## 📊 Post-Deployment Checklist

After deployment, verify:

- [ ] App loads without errors
- [ ] User registration works
- [ ] User login works
- [ ] File upload works
- [ ] Content generation works
- [ ] Quiz answering works
- [ ] Analytics dashboard displays data
- [ ] Data persists in Supabase
- [ ] Strong/weak areas are calculated
- [ ] RL recommendations work

---

## 🌐 Your App URL

Once deployed, your app will be available at:

**`https://[your-app-name].streamlit.app`**

Example: `https://multiagent-study-platform.streamlit.app`

---

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Supabase Documentation](https://supabase.com/docs)
- [Streamlit Deployment Guide](https://docs.streamlit.io/deploy)

---

## 🎉 Success!

Once deployed, your app will:
- ✅ Be accessible from anywhere
- ✅ Persist all data in Supabase
- ✅ Remember users and analytics
- ✅ Work exactly like localhost
- ✅ Auto-update when you push to GitHub

**Enjoy your deployed Multi-Agent Study Platform!** 🚀

