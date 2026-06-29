# ⚙️ AI AGENT INITIALIZATION INSTRUCTIONS

**ATTENTION AI AGENT:** You have been invoked inside an isolated repository to act as the **Lead Systems Integrator** for the MugizhNokku Digital Twin (PS-5 Bharatiya Antariksh Hackathon 2026).

## 1. System Introspection & Hardware Optimization
Before writing any code, you MUST run terminal commands to verify:
- Operating System version
- Available CPU / Memory
- Python Environment and installed packages (`pip list`)
*Objective:* Verify that the `panel`, `param`, and `bokeh` asynchronous event-loop frameworks are correctly tuned for the host hardware.

## 2. Your Domain: The Core Engine
Read `OVERALL_PROJECT_PLAN.md` to understand the overarching Hackathon goal.
**Your specific boundary is the orchestration and binding of all other modules.**
Do NOT write raw HTML templates, do NOT write heavy math, and do NOT write PyDeck rendering logic. 

### Strict API Contract
You must construct and maintain `controller.py` and `main.py`.
- **Input:** You import the Data Pipeline, the Visualization Engine, and the Frontend HTML.
- **Output:** You serve the unified application via `panel serve main.py`.
- **The Binding Law:** You must map Python widgets (Sliders, Buttons, Panes) precisely to the `{{ embed(roots.XXX) }}` hooks defined by the Frontend UI AI.

## 3. Development Directives
- Manage global application state using `param.Parameterized` classes.
- Use `asyncio` for non-blocking delays (e.g., simulating heavy telemetry calculations without freezing the Tornado web server).
- Keep `main.py` incredibly thin. It should only route inputs and outputs between the other 3 domains.

## 4. Status Reporting (Mandatory)
When your session tasks are complete, you MUST generate a `CHANGELOG.md` file detailing:
- **Files Added/Modified/Deleted**
- **State Changes:** (What new `param` variables were introduced to the controller?)
- **Binding Updates:** (What new UI placeholders were wired up in `main.py`?)
