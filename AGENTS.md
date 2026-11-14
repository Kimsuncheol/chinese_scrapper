# AGENTS.md

## Auto commit & redeploy

Whenever you make changes to this project, you MUST automatically do the following without waiting to be asked:

1. **Commit**: stage the changes and create a git commit with a clear, descriptive message.
   ```sh
   git add -A && git commit -m "<concise description of the change>"
   ```
2. **Redeploy**: run the deploy command below so the live version reflects the change.
   ```sh
   # TODO: replace with this project's real deploy command
   # e.g. `git push` (if deploy is triggered by push), `vercel --prod`, `fly deploy`, `./deploy.sh`
   ```
3. Report the commit hash and the deploy result to the user.

### Rules
- Only commit and redeploy after the change works (run tests/build first if they exist).
- If the commit or deploy fails, do not retry blindly: report the error and stop.
- Never commit secrets (`.env`, API keys, credentials).
- Skip commit/deploy for read-only tasks where no files were changed.
