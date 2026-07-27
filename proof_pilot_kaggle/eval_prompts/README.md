# eval_prompts/

Self-contained **grading prompts** — one per submission — of the kind used for the AI graders in this study. Each prompt can be handed to an LLM/agent so it grades one submission and returns a completed grading sheet.

Each prompt bundles three things:

1. **The problem and its markscheme** for that problem.
2. **The submission to grade**, inserted with **line numbers** so the errors log can cite them.
3. **Grading instructions** (the 0/1/6/7 scale, grading against the markscheme rather than the reference solution, mapping alternative approaches onto the markscheme milestones), plus the full grading template embedded inline for the agent to fill out.

The layout mirrors `../evals/`: one subfolder per problem, with one `.md` per submission (`model_1.md` … `model_8.md`, `team_1.md` … `team_6.md`; 84 in total). [`template.md`](template.md) is the scaffold from which all prompts were generated.

Note: the embedded markscheme excerpts are provided as context only and are not intended to compile standalone (some figures are omitted); the authoritative markschemes are in [`../problems_and_markschemes/markschemes.pdf`](../problems_and_markschemes/markschemes.pdf).
