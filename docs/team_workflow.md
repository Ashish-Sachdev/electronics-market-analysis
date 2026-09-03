# Team Workflow

## Eight workstreams
1. Project lead and definitions
2. Data ingestion
3. Data transformation
4. SQL and DuckDB
5. EDA and business insights
6. Power BI price/coverage page
7. Power BI availability/sale page
8. Testing and documentation

## Git workflow
Create a GitHub issue before substantial work. Use branches such as `feature/ingestion`,
`feature/transform`, `analysis/eda`, `dashboard/pricing`, `test/data-quality`, or
`docs/methodology`.

One teammate owns each shared file at a time. Open a pull request, ask a paired teammate to review it, and merge only after checks pass.

## Daily check-in
Each person answers: What did I finish? What will I finish next? What is blocking me? Does another teammate need something from me?

## Definition of done for a task
Code runs, relevant tests pass, output is checked, documentation is updated, no credentials/raw restricted data are committed, and another teammate can explain the result.
