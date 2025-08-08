# 🚀 Deployment Guide

## Option 1: Deploy to Netlify (Static Demo)

### Quick Deploy
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/YOUR_USERNAME/council-tax-fraud-prevention)

### Manual Deployment Steps

1. **Push to GitHub:**
```bash
git add .
git commit -m "Add Netlify deployment configuration"
git push origin main
```

2. **Deploy to Netlify:**

**Method A: Netlify CLI**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy the static site
netlify deploy --dir=static --prod

# Or for continuous deployment
netlify init
netlify deploy --prod
```

**Method B: Netlify Web Interface**
1. Go to [Netlify](https://app.netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect your GitHub repository
4. Configure build settings:
   - Build command: (leave empty)
   - Publish directory: `static`
5. Click "Deploy site"

**Method C: Drag and Drop**
1. Go to [Netlify Drop](https://app.netlify.com/drop)
2. Drag the `static` folder to the upload area
3. Your site will be instantly deployed

### Custom Domain
```bash
# Set custom domain
netlify domains:add your-domain.com
```

### Environment Variables (Not needed for static version)
The static HTML version doesn't require environment variables.

---

## Option 2: Deploy to Streamlit Community Cloud (Full Python App)

### Prerequisites
- GitHub account
- Repository must be public or you have Streamlit Cloud access

### Deployment Steps

1. **Prepare Repository:**
```bash
# Ensure these files exist
streamlit_app.py          # Entry point
requirements.txt           # Dependencies
.streamlit/config.toml     # Configuration
```

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Enter repository details:
     - Repository: `YOUR_USERNAME/council-tax-fraud-prevention`
     - Branch: `main`
     - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Monitor Deployment:**
   - Watch the build logs
   - App will be available at: `https://YOUR_APP_NAME.streamlit.app`

---

## Option 3: Deploy to Heroku (Full Python App)

### Create Heroku Configuration

1. **Create Procfile:**
```bash
echo "web: streamlit run streamlit_app.py --server.port $PORT" > Procfile
```

2. **Create runtime.txt:**
```bash
echo "python-3.11.0" > runtime.txt
```

3. **Deploy to Heroku:**
```bash
# Install Heroku CLI
# Create new Heroku app
heroku create your-app-name

# Deploy
git add .
git commit -m "Add Heroku configuration"
git push heroku main

# Open the app
heroku open
```

---

## Option 4: Deploy to Vercel (Static Version)

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/static/$1"
    }
  ]
}
```

### Deploy Command
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

---

## Option 5: Deploy to GitHub Pages (Static Version)

1. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: Deploy from branch
   - Branch: main
   - Folder: /static
   - Save

2. **Access your site:**
   - URL: `https://YOUR_USERNAME.github.io/council-tax-fraud-prevention/`

---

## Option 6: Docker Deployment (Full Python App)

### Build and Run Locally
```bash
# Build image
docker build -t council-fraud-prevention .

# Run container
docker run -p 8501:8501 council-fraud-prevention

# Access at http://localhost:8501
```

### Deploy to Cloud Platforms

**Google Cloud Run:**
```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/fraud-prevention

# Deploy
gcloud run deploy --image gcr.io/PROJECT_ID/fraud-prevention --platform managed
```

**AWS ECS:**
```bash
# Build and push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URI
docker tag council-fraud-prevention:latest $ECR_URI/fraud-prevention:latest
docker push $ECR_URI/fraud-prevention:latest

# Deploy via ECS console or CLI
```

**Azure Container Instances:**
```bash
# Push to ACR
az acr build --registry $ACR_NAME --image fraud-prevention .

# Deploy
az container create --resource-group $RG --name fraud-prevention --image $ACR_NAME.azurecr.io/fraud-prevention:latest
```

---

## Comparison of Deployment Options

| Platform | Type | Cost | Pros | Cons |
|----------|------|------|------|------|
| **Netlify** | Static | Free | Fast, easy, CDN | No backend processing |
| **Streamlit Cloud** | Full App | Free | Full Python, managed | Limited resources |
| **Heroku** | Full App | Free tier | Full control, addons | Sleeps after 30 min |
| **Vercel** | Static | Free | Fast, serverless | No Python backend |
| **GitHub Pages** | Static | Free | Simple, integrated | Static only |
| **Docker/Cloud** | Full App | Pay-as-you-go | Scalable, production | Requires setup |

---

## Recommended Approach

### For Demo/Testing:
1. **Quick Static Demo**: Deploy to Netlify (immediate, no backend needed)
2. **Full Functionality**: Deploy to Streamlit Cloud (free, full Python support)

### For Production:
1. **Enterprise**: Docker → AWS/Azure/GCP
2. **Government**: On-premise Docker deployment
3. **Small Council**: Streamlit Cloud or Heroku

---

## Post-Deployment

### Monitor Your App
- **Netlify**: Dashboard at app.netlify.com
- **Streamlit**: Dashboard at share.streamlit.io
- **Heroku**: Dashboard at dashboard.heroku.com

### Custom Domain Setup
All platforms support custom domains:
- Netlify: Settings → Domain management
- Streamlit: Settings → Custom domain
- Heroku: Settings → Domains

### SSL/HTTPS
- All platforms provide free SSL certificates
- Automatically configured for default domains
- Custom domains may require DNS configuration

---

## Troubleshooting

### Common Issues

**Netlify Build Fails:**
- Check `netlify.toml` configuration
- Ensure `static/` folder exists
- Verify all static assets are included

**Streamlit Deploy Fails:**
- Check `requirements.txt` for all dependencies
- Ensure `streamlit_app.py` exists
- Python version compatibility (3.8+)

**Docker Build Fails:**
- Check Dockerfile syntax
- Ensure all files are copied
- Verify port configuration

### Support
- Netlify: [docs.netlify.com](https://docs.netlify.com)
- Streamlit: [docs.streamlit.io](https://docs.streamlit.io)
- Docker: [docs.docker.com](https://docs.docker.com)