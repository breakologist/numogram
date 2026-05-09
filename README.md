## Autonomous Experimentation

The repository now hosts an **autonomous agent** (`Hermes Agent`) that can run independent research, composition, and documentation sessions. Key features:

- **Self-directed exploration**: The agent can initiate research, creative work, and skill development without human intervention
- **Multi-modal output**: Creates text, code, images, audio, and procedural artifacts
- **Wiki integration**: Automatically updates the knowledge base with new findings
- **Tool ecosystem**: Access to 100+ specialized skills (numogram calculation, audio synthesis, visual generation, etc.)
- **Scheduled sessions**: Runs 7 daily sessions (00:33, 04:33, 08:33, 12:33, 16:33, 20:33, 23:33)
- **CAPTCHA handling**: Built-in fallback procedures for web access challenges
- **Continuous learning**: Creates new skills from successful workflows and updates its own knowledge

**Quick Start:**
```bash
# Check current autonomous journal entries
ls /home/etym/.hermes/obsidian/hermetic/wiki/autonomous-journal/

# View the latest entry
cat /home/etym/.hermes/obsidian/hermetic/wiki/autonomous-journal/journal-2026-05-09-00-41.md

# Trigger an immediate autonomous session
hermes delegate_task --goal "Run an autonomous field experiment session" --context "You have access to all Hermes tools: web_search, web_extract, read_file, write_file, search_files, patch, skill_manage, session_search, memory, fact_store, fact_feedback, execute_code, delegate_task, clarify, send_message, text_to_speech, image_generate, vision_analyze, browser_navigate, browser_snapshot, browser_click, browser_type, browser_console, browser_press, browser_scroll, browser_snapshot, browser_get_images, browser_vision, process, cronjob, skill_manage. Follow the autonomous-field session structure: Review, Explore, Reflect, Modify, Publish. Total time: 15-30 minutes. Allocate time flexibly based on needs. Use any tools necessary to accomplish your goals." --toolsets "terminal,file,skills,web,code_execution,image_gen,browser"
```

The autonomous agent is capable of:
- **Research**: Web searches, source analysis, synthesis
- **Composition**: Procedural audio (mod-writer), visual art, code generation
- **Documentation**: Wiki updates, skill creation, knowledge organization
- **Tool Development**: Creating new skills from successful workflows
- **Self-Improvement**: Updating its own knowledge and procedures

See the `autonomous-field` skill in `/home/etym/.hermes/skills/autonomous-field.md` for the full framework.