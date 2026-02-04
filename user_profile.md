# LONG-TERM USER PROFILE
*This file contains established facts, preferences, and completed interaction summaries. It is the "Anchor" for the agent's knowledge.*

## 👤 IDENTITY & SYSTEM
- **OS:** Linux
- **Project Path:** `/home/konoh/ia`
- **Preferred Agent Mode:** Master Agent (Cloud-based orchestration).

## ✈️ TRAVEL PREFERENCES (AERO)
- **Interests:** Cultural immersion, "Leisurely pace" (no rushing).
- **History:**
    - **2026 Inquiry:** Planning a trip to **Shanghai** (Mainland China) and **Taiwan**.
    - **Advice Received:**
        - Shanghai: 4-5 days (Bund, Yu Garden, French Concession).
        - Taiwan: 10-16 days depending on scope (Taipei vs. Whole Island).
    - **Status:** Pending decision on Budget, Vibe, and Visa type.

## 🇯🇵 JAPANESE & CULTURE (KAIZEN)
- *No specific entries yet.*

## 💻 TECH & DEV (SWITCH)
- *No specific entries yet.*

## 🛒 SHOPPING (CART)
- *No specific entries yet.*

## 🛠️ HARDWARE & DEVICES
- **Kobo E-Reader:** Configured as a manga reader using NickelMenu and Ultimate Manga Reader (UMR).
- **Setup Date:** Jan 24, 2026.

## 🟢 PROJECT: MrClinic (Active)
- **Production URL:** https://mrclinic.vercel.app
- **Deployment:** Vercel (Zero Config + vercel_build.sh)
- **Database:** Prisma Postgres (Vercel Storage)
- **Startup Note:** Use `sg docker -c "docker compose up -d"` to bypass group permission issues. Port 5432 conflict with `consultiva_db` resolved.
- **Architecture:** Monolith (Django) + Islands (React) + Workers (Celery).
- **Product Model:** 3 Tiers (Package A, B, C) based on 10 functional modules.
- **Status:** Planning complete. Ready for Phase 1 (Foundation) setup.
- **Ref Doc:** `GEMINI.md` in project root.

## 🛠️ HARDWARE & AI RIG (PLAN)
- **Target Device:** Mac Studio M5 Ultra (Expected Late 2026).
- **Target Memory:** 256GB - 512GB Unified Memory.
- **Performance Goals:** 1M+ token context window; 30+ tokens/sec on 72B models.
- **Model Hierarchy:** 
    - Daily Driver: Qwen 2.5 Coder 32B/72B.
    - Architectural Consultant: Llama 3 405B.

## 🟢 PROJECT: Meeting Translator (Completed)
- **Goal:** Real-time Japanese to English HUD for meetings.
- **Architecture:** Hybrid. Local Threaded Audio Capture (Python/Tkinter) -> OpenAI Whisper API.
- **Status:** Version 1.0 packaged (Git initialized).
- **Key Config:** Uses `.env` for API key; requires `libpulse-dev` on Linux.
- **Hardware:** Verified on Laptop Mic (RDP Source) + Anker Speaker.

## 🟢 PROJECT: Bohr Individual (Active)
- **Architecture:** Monolith (Go/Fiber) + SPA (Vue 3/Vite).
- **External Dependency:** Django service for file management.
- **Status:** Investigating file upload issues and enhancing UI consistency.

## 🔄 SYSTEM CONFIGURATION
- **Multi-Device Sync:** Active (Git-based).
    - **Mechanism:** `agent-sync.sh` handles push/pull.
    - **Triggers:**
        - **Start:** `gemini` alias in `~/.bashrc` pulls latest memory.
        - **Update:** `log_keeper.sh` auto-pushes after memory writes.
        - **Exit:** `gemini` alias triggers final sync on session end.

## 🟢 PROJECT: MrClinic (Updates Jan 31, 2026)
- **Login System:** implemented custom login page with "Dev Bypass" for rapid role switching (Superuser, Doctor, Nurse, Staff, Finance).
- **Security:** Django 5.0+ requires POST requests for logout;  updated to use hidden form submission.
- **Local Dev:** Configured  fallback in  for persistence when  is missing.
- **Tools:** Added  management command to seed role-based accounts (password: ).

## 🟢 PROJECT: MrClinic (Updates Jan 31, 2026)
- **Login System:** implemented custom login page with "Dev Bypass" for rapid role switching (Superuser, Doctor, Nurse, Staff, Finance).
- **Security:** Django 5.0+ requires POST requests for logout; `base.html` updated to use hidden form submission.
- **Local Dev:** Configured `sqlite3` fallback in `settings.py` for persistence when `DATABASE_URL` is missing.
- **Tools:** Added `create_demo_users` management command to seed role-based accounts (password: `password123`).
