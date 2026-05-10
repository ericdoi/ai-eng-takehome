# Session Prompts

User prompts from the working session, in order. Claude responses omitted.
Sensitive values (API key) redacted.

---

1. *(local command: `gh auth login`, authenticated as ericdoi)*

2. Please fork https://github.com/hex-inc/ai-eng-takehome and clone it here for work.

3. *(after being asked to install git-lfs manually)*
   I did it and installed:
   ```
   zsh completions have been installed to:
     /opt/homebrew/share/zsh/site-functions
   > git lfs install
   Git LFS initialized.
   > git lfs install --system
   warning: current user is not root/admin, system install is likely to fail.
   Git LFS initialized
   ```

4. Let's create a directory for our working context files, and populate it with a WORKLOG.md and a TODO.md. They should have directives: the TODO should contain only unfinished items; if an item is finished it should be moved to the worklog. When looking at the TODO, the top item should be the highest priority. We should focus on the top unfinished item; if it is not trivial, it should be broken down further until the top item is trivial.

5. *(after Claude offered to draft an initial task list from the repo)*
   No; I added PLAN.md and CONTEXT.md from external research; please read them.

6. *(after Claude asked whether to unzip the database and run `uv sync`)*
   Yes

7. *(asked for the OpenRouter API key)*
   [REDACTED]

8. It's good to know; please add that info somewhere so we know roughly how much a run costs.

9. *(baseline eval kicked off; while it ran)*
   Let's keep a new file with a markdown table of experiment results.

10. We should check how much credits are left, since we started with $20.

11. It's good to know; please add that info somewhere so we know roughly how much a run costs.

12. *(baseline results in: 0/64 easy, 0/64 hard)*
    Let's update the TODO since we reprioritized a bit.

13. We basically started on Phase 1 instead of Phase 0 so we can swap them.

14. Please also move the completed items to the worklog.

15. *(after Claude proposed building Phase 1 tools)*
    Yes

16. *(Phase 1 eval completed: 62.5% easy, 39.1% hard)*
    check the progress of the shell run

17. Let's write a short doc for each run, before we forget.

18. Once we get the results, we should git commit.

19. *(Run 2 results in: regression to 48.4% / 28.1%)*
    Let's update the TODO.

20. `  - Fix: strengthen system prompt — "the guide title names the schema; use it directly after reading"`
    This is one idea; we should be clear that it's just an idea and there may be other approaches to consider.

21. We should add context about this error somewhere, either in the run file or in a separate file about the issue.

22. Good. Let's prepare to handoff the context. Make sure the existing docs have all the info needed to start fresh on the TODO.md

23. Yes *(to committing the handoff docs)*

24. We should also save this chat's prompts as an artifact for the assignment, omitting the openrouter API key and any other sensitive info. Probably it's not needed to include your responses, only my prompts.

---

## Session 2

1. *(local command: `/clear`)*
   We're working on context/TODO.md

2. Try it. The openrouter key is [REDACTED]; let's save it in an env file and make sure it's git ignored

3. *(Run 3 completed: 32.8% hard — regression)*
   we should update the context/issues and context/runs and also the TODO and WORKLOG.

4. *(after Claude proposed Run 5 prompt and offered to fire it)*
   Let's not fire the next run yet. Update the docs though.

5. I would revert back to run1 state, and take a different approach: currently, the guides are only about rules, and not comprehensive descriptions of what data/tables are in the schema. I suspect it will be more effective to write an llm pipeline to preprocess/index each schema: (1) textualize the tables, including sample rows; (2) use an llm prompt to read the textualized tables as well as the corresponding guide, and write a new comprehensive generated guide tying together the schema and the rules, e.g. encoding tables with their common-name synonyms and the rules in sql form; (3) embed the generated guide for search and make it discoverable via a new tool.

   What do you think about this?

6. yes, write a plan doc.

7. No; we should revert to run1 state first.

8. Try reproducing run 1 to be safe.

9. *(Run 1′ completed: 65.6% easy / 26.6% hard — variance confirmed)*
   Add that note to RESULTS.md.

10. We probably also need a better debug breakdown. First, did the agent identify the right schema? The right tables? Finally, the right logic?

11. Let's update the RESULTS.md post-hoc with the analyzer results on previous logs.

12. much better. let's update the worklog

13. let's make sure the docs contain what's needed for a handoff.

14. please update SESSION_PROMPTS.md with the prompts in this session. you can add a new section

---

## Session 3

1. *(session resumed from summary)* Is the find_schema tool documentation clear on what it's returning?

2. Is it confusing that the generated guides themselves have SQL snippets which omit the schema name? E.g. /Users/ericdoi/.../ErgastF1.md

3. Let's regenerate the guides.

4. How many credits are left on the openrouter api

5. We should note how much each schema regeneration costs, roughly, in the STATUS.md and code docs.

6. Good. Let's update the TODO and WORKLOG and RESULTS so far before running the evals again

7. Note that "Run 5" was previously referring to something else so let's make sure there's no confusion there

8. Let's do an eval run, update the results/worklog/todo, and then do a git commit before further iteration.

9. We should be adding the funnel analysis results into a markdown table in RESULTS.md as well, either the existing "Hard split failure breakdown" or a separate sub-breakdown.

10. ah sorry, thanks

11. Let's re-commit

12. Let's dig in, and create a new issues file regarding the business logic

13. Are these failures of understanding the original guides, or is there actual ambiguity? We don't want to overfit to the evals data by doing custom fixes, and instead should focus on approaches that can (1) improve the overall quality of our guides, (2) provide more focused context to avoid overwhelming the agent, or (3) improve the agent prompt guidance in a general way

14. Agreed on those 3 approaches. Let's add them to a plan file for the business logic issue.
    Also:
    Financial: IIUC, our synthesizer LLM call uses haiku; we should re-run the guide generation with Sonnet or Opus on Financial (noting the cost) and see if it fixes the issue.
    Airline + Chess: left joins would be safe, right? We could add some guidance on that to the prompt.

15. Let's add all the TODOs to the TODO.md file before starting

16. Let's not re-gen all guides yet; we should test iteratively. Regen the guides for the main failure cases first.

17. Wait; make sure the docs have all the context so I can clear the session.

18. Regenerating with sonnet/opus will be much more expensive than haiku and we likely won't be able to afford it on all schemas

19. Also, please update context/SESSION_PROMPTS.md
