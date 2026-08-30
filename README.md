# 🌧️ Tone: AI Water Harvesting Intelligence

> **SU Ideas Festival 2026 Submission** | Reimagining Water Futures: Solutions for Clean Water and Sanitation

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-AI-blue?style=flat)](https://deepmind.google/technologies/gemini/)

Tone transforms raw satellite imagery and geospatial rainfall data into an actionable, bankable rainwater harvesting investment brief in under 60 seconds. We help commercial facilities in Kenya turn uncaptured rooftop runoff into automated, confidence-adjusted ROI models.

---

## 📸 See it in Action
*(Add a high-quality GIF or YouTube link of the 60-second workflow here: Map discovery → ROI calculation → AI Brief generation)*


---

## 🧠 Core Technical Innovations
Pluvial isn't just a UI wrapper; it features two distinct backend engines designed for the built environment:

1. **The CV-to-ROI Confidence Chain:** 
   Our financial engine (`roi_engine.py`) doesn't just output static numbers. It discounts projected ROI based on the computer vision (CV) detection certainty of physical roof traits. We give CFOs a risk-weighted model they can trust.
2. **Grounded RAG Legal Pipeline:** 
   The AI Investment Brief is powered by Gemini 2.5 Flash, but grounded locally. Our `rag_retrieval.py` fetches context from Kenyan Water Resources Authority (WRA) guidelines and NEMA regulations to generate legally sound, hallucination-free proposals.

---

## 🏗️ Architecture & Tech Stack
- **Frontend:** Next.js (App Router), React 19, Tailwind CSS 4, shadcn/ui.
- **Mapping:** MapLibre GL with Carto Positron basemap & Esri World Imagery. Filtering of 10K+ records happens entirely client-side.
- **Backend:** FastAPI handling pure Python calculation layers for instant, three-scenario financial modeling.
- **AI / LLM:** Google Gemini 2.5 Flash with strict JSON schema enforcement via Pydantic.

---

## 🚀 How to Run Locally

### Prerequisites
- Node.js (v18+)
- Python 3.10+
- Google Gemini API Key

### Backend Setup (FastAPI)
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the server
uvicorn main:app --reload --port 8000
\`\`\`

### Frontend Setup (Next.js)
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`
The app will be running at `http://localhost:3000`.

---

## 👥 The Team
- Lionel Okinyi - Full-Stack & AI Engineering
- Marylynn Wanjiru - 
- **[]** 
*Built with ❤️ for the SU Ideas Festival 2026.*
