# 30-Days-of-Agentic-AI
# 🤖 30 Days of Agentic AI: From Script to System
### Targeting 10 LPA+ Roles by March 2026

Welcome to my 30-day intensive journey into **Agentic AI Engineering**. This repository serves as my living portfolio, replacing a traditional resume with a "Proof of Work" history. 

My goal is to transition from a Data Analyst (Intern) to a full-stack **AI Developer** capable of building autonomous, resilient, and production-ready AI agents.

---

## 🛠️ Tech Stack
- **Languages:** Python 3.x
- **AI Models:** Gemini 2.0 Flash, Gemini 1.5 Pro (via Google GenAI SDK)
- **Infrastructure:** Dotenv (Security), Git/GitHub (Version Control)
- **Concepts:** Rate Limiting (429), Error Handling, SSL Resilience, RAG (Coming Soon)

---

## 📅 Roadmap Progress

### Phase 1: Foundations & API Resilience
- [x] **Day 01: The AI Strategist** - Set up a professional directory structure and `.env` security.
  - Built a script with **Exponential Backoff** to handle API Rate Limits (429).
  - Implemented model discovery logic to bypass `404 NOT_FOUND` errors.
  - Successfully generated a technical roadmap for 10 LPA+ job readiness.

### Phase 2: Knowledge Augmentation (RAG)
- [ ] **Days 02-10:** PDF/Web-Scraping Agents & Vector Databases.

### Phase 3: Autonomous Agents
- [ ] **Days 11-30:** Building multi-agent workflows and Streamlit UI.

---

## 🚀 Key Learning: Debugging the "Final Boss"
Day 1 wasn't just about code; it was about handling infrastructure. I successfully navigated:
1. **SSL Handshake Issues:** Resolved `UNEXPECTED_EOF` errors using custom `http_options`.
2. **Git Conflicts:** Manually resolved merge conflicts in `.gitignore` during the initial cloud sync.
3. **Quota Management:** Built logic to wait and retry during peak server traffic.

---

## 📁 Repository Structure
```text
.
├── Day_01/
│   ├── ai_strategist.py     # The "Brain" of Day 1
│   ├── check_my_models.py   # Discovery tool for API resources
│   └── roadmap.txt          # AI-generated strategy
├── .env                     # (Ignored) Secret keys
├── .gitignore               # Security rules
└── README.md                # You are here!
