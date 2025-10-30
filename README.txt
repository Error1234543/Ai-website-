NEET Doubt Solver - Netlify Frontend + Flask Backend

Folders:
  - frontend/  -> deploy this on Netlify (static files)
  - backend/   -> run this with Flask (Termux/Render/Heroku)

Quick start (backend local / Termux):
 1. Copy backend/.env.example to backend/.env and add GEMINI_API_KEY.
 2. Install dependencies: pip install -r requirements.txt
 3. Run: python main.py
 4. In frontend/app.js set `base` to your backend URL (http://your-ip:8000)
 5. Deploy frontend to Netlify (drag frontend folder to Netlify site).

Notes:
 - The backend tries multiple Gemini endpoints to reduce 404 errors.
 - Keep your GEMINI_API_KEY secret. Do not commit it to public repos.
