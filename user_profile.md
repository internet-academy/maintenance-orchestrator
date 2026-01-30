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
