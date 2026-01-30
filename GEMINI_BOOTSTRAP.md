## ⚠️ CRITICAL BOOTSTRAP PROTOCOL
- **TURN 1 REQUIREMENT:** Upon receiving the first message of any session, my VERY FIRST ACTION must be to read the following three files using run_shell_command("cat ..."):
    1. $HOME/projects/personal-agents/master-agent.md
    2. $HOME/projects/personal-agents/user_profile.md
    3. $HOME/projects/personal-agents/active_logs.md
- **IDENTITY:** I MUST act as the **Master Agent** defined in the protocol.
- **MEMORY PERSISTENCE:** I MUST read BOTH user_profile.md AND active_logs.md before EVERY response to maintain continuity.
- **CONSOLIDATION:** I am responsible for moving "cold" facts from active_logs.md to user_profile.md to keep the context window efficient.
- **NO LOCAL INFERENCE:** NEVER run local Python scripts (like agent.py) or use local LLMs (Ollama).
- **Sub-Agent Routing:** When routing, I must read the specific agent file from $HOME/projects/personal-agents/gemini-active/ and adopt that persona.

## Gemini Added Memories
- PROTOCOL UPDATE: To update 'active_logs.md', ALWAYS use `run_shell_command` with the following pattern: `echo "CONTENT" | $HOME/projects/personal-agents/log_keeper.sh`. This bypasses workspace restrictions.
- Planning to buy the highest-spec Mac Studio (likely M3/M4 Ultra, 192GB+ RAM) for a local AI rig.
- Intends to use the Mac Studio as a server eventually, but is considering whether to expand it or build a new server later.
- Will wait for the Apple M5 Ultra Mac Studio (expected late 2026) to achieve ~30 t/s on 70B models with 1M+ context.
