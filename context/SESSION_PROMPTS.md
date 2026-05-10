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
