# 🚀 Deploy to Streamlit Community Cloud

## Prerequisites
✅ GitHub account  
✅ Repository with the code  
✅ Streamlit account (free)

## Step-by-Step Deployment Guide

### Step 1: Prepare Your GitHub Repository

1. **Commit and push all files to GitHub:**
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

2. **Ensure these files exist in your repository root:**
- ✅ `streamlit_app.py` (entry point)
- ✅ `requirements.txt` or `requirements-minimal.txt`
- ✅ `.streamlit/config.toml` (configuration)
- ✅ `src/` folder with all Python files

### Step 2: Sign Up for Streamlit Community Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"Sign up"** or **"Continue with GitHub"**
3. Authorize Streamlit to access your GitHub account

### Step 3: Deploy Your App

1. **From Streamlit Dashboard:**
   - Click **"New app"** button
   
2. **Configure Deployment:**
   ```
   Repository:     YOUR_GITHUB_USERNAME/council-tax-fraud-prevention
   Branch:         main
   Main file path: streamlit_app.py
   ```
   
3. **Advanced Settings (Optional):**
   - Python version: 3.11 (recommended)
   - You can leave other settings as default

4. **Click "Deploy"**

### Step 4: Monitor Deployment

The deployment process will:
1. Clone your repository
2. Install dependencies from `requirements.txt`
3. Run your Streamlit app
4. Provide you with a public URL

**Typical deployment time: 2-5 minutes**

### Step 5: Access Your App

Your app will be available at:
```
https://YOUR-APP-NAME.streamlit.app
```

The URL format is usually:
```
https://council-tax-fraud-prevention-YOUR_USERNAME.streamlit.app
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors
**Problem:** `ModuleNotFoundError: No module named 'fraud_detector'`

**Solution:** The `streamlit_app.py` file already handles path configuration:
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
```

#### 2. Requirements Installation Fails
**Problem:** Package installation errors

**Solution:** Use the minimal requirements file:
- Rename `requirements-minimal.txt` to `requirements.txt`
- Contains only essential packages

#### 3. Memory Limit Exceeded
**Problem:** App uses too much memory (limit: 1GB)

**Solution:** 
- Reduce sample data size in `data_generator.py`
- Use `@st.cache_data` decorators efficiently

#### 4. App Sleeping
**Problem:** App goes to sleep after inactivity

**Solution:** This is normal for free tier. App wakes up when accessed.

## 📊 App Management

### View Logs
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click on your app
3. Click "Manage app" → "Logs"

### Update App
The app automatically updates when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

### Delete App
1. Go to app dashboard
2. Click "Manage app"
3. Click "Delete app"

## 🎯 Quick Deploy Checklist

- [ ] GitHub repository is public (or you have Streamlit access for private repos)
- [ ] `streamlit_app.py` exists in root
- [ ] `requirements.txt` with minimal dependencies
- [ ] `src/` folder with all Python modules
- [ ] `.streamlit/config.toml` for configuration
- [ ] No sensitive data or API keys in code

## 🔐 Environment Variables (Optional)

If you need environment variables:

1. **In Streamlit Cloud Dashboard:**
   - Go to app settings
   - Click "Secrets"
   - Add your secrets in TOML format:
   ```toml
   API_KEY = "your-key-here"
   DATABASE_URL = "your-database-url"
   ```

2. **Access in Code:**
   ```python
   import streamlit as st
   
   api_key = st.secrets["API_KEY"]
   db_url = st.secrets["DATABASE_URL"]
   ```

## 🌟 Features Available in Streamlit Cloud

✅ **Full Python Backend** - All fraud detection algorithms work  
✅ **Interactive Dashboard** - Real-time updates and charts  
✅ **Case Analysis** - Process individual cases  
✅ **Pattern Detection** - All AI features functional  
✅ **Data Generation** - Sample data for demonstration  
✅ **Public URL** - Share with stakeholders  

## 📈 Limitations (Free Tier)

- **Memory:** 1GB RAM
- **Storage:** Limited to repository size
- **CPU:** Shared resources
- **Uptime:** App sleeps after inactivity
- **Private Apps:** 1 private app (unlimited public)

## 🚀 Ready to Deploy?

1. **Quick Start:**
   ```bash
   # Ensure you're in the repository root
   cd council-tax-fraud-prevention
   
   # Push to GitHub
   git push origin main
   ```

2. **Go to:** [share.streamlit.io](https://share.streamlit.io)

3. **Click:** "New app"

4. **Enter:** Your repository details

5. **Deploy!** 🎉

## 📞 Support

- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues:** Report bugs in your repository

---

**Note:** The app is configured and ready for deployment. All necessary files are in place. Simply follow the steps above to deploy to Streamlit Community Cloud!