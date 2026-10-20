# Project-specific notes — template

Copy this file to `PROJECT_SPECIFIC.md` inside your project's
`dm-library/` submodule. That filename is ignored by this library;
it is the only downstream-local write allowed inside the submodule. Keep an
external backup if these untracked notes matter: Git does not preserve them when
the submodule directory is removed or force-cleaned.

```powershell
Copy-Item dm-library/PROJECT_SPECIFIC.template.md dm-library/PROJECT_SPECIFIC.md
```

Use one section per paper or code snapshot, matching its shared-document title.
Link the shared source, describe only local relevance and deviations, and identify
the exact library commit pin. State reference behavior before local changes and
give a reason. Date claims that may become stale. Cite source paths and symbols,
never dump line numbers. Report shared-document errors for correction in the
canonical checkout. Do not copy project notes into shared documents.

```markdown
# Project-specific notes — <project>

Project: <purpose>
Library pin: <full commit SHA from git -C dm-library rev-parse HEAD>
Maintainer: <name>
Reviewed: <YYYY-MM-DD>

## <Year> — <Author> — <Paper title>

**Reference.** <link to shared summary and paper>

**Relevance.** <why this source matters locally>

**How we use it.** <local application and evidence>

**Where we deviate.** <reference value/behavior → local choice → reason>

**Open questions.** <what remains unverified>
```

Template version 1 — DM Library.
