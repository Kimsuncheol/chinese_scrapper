# Latest Chinese lesson schedule

GitHub Actions requests the latest Chinese lesson Monday–Friday at 23:00
Asia/Seoul (`0 14 * * 1-5` UTC). Scheduled execution can be delayed by GitHub.
The workflow discovers the publisher URL from the Chinese section feed, excludes
future Korean publication dates, and invokes the existing production `/api/scrape`
endpoint. The scraper's existing duplicate detection preserves stored lessons.
A manual workflow run catches up immediately.

The production service must have a working PostgreSQL `DATABASE_URL` and schema.
The job checks `/readyz` first and fails without scraping when persistence is
unavailable. At repair time, Cloud Run had no database configuration and returned
503. Creating or selecting a database is required before this job can succeed.
No database is provisioned or paid infrastructure created by this workflow.
These scheduler files do not change HTTP routes, payloads, or the running image.
