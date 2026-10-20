# AGENTS.md — DM Library maintenance contract

Establish which checkout you are in before writing. The canonical DM Library
checkout is editable when the owner requests work here. A downstream project's
`decision-models-library/` is a pinned, read-only Git submodule. Never edit its
shared files from a consumer. Report corrections to the owner for the canonical
checkout. The sole downstream-local exception is the ignored `PROJECT_SPECIFIC.md`
created from [the template](PROJECT_SPECIFIC.template.md).

## Purpose and scope

This is a knowledge base and maintenance toolkit, not an installable model package.
It holds papers, generated text, substantive summaries, a cross-source synthesis,
and greppable official implementation snapshots. The conceptual domain is methods
for choosing actions; the exact corpus is the owner's live Zotero collection with
the unique stable name substring **Decision Models**. Numeric prefixes are sorting
keys and must never select the collection. The initial corpus concerns fast,
schema-conditioned decision models; do not add classical decision theory,
optimization, policy learning, or other topics merely to fill conceptual categories.

The initial owner request authorized every source already in that collection.
Future additions require a new owner request. A sync discrepancy is a report,
not permission to expand the collection, import extra papers, or delete records.
No infrastructure exception or consumer list is inherited from another library.

## Zotero is authoritative

Use the live Local API at `http://127.0.0.1:23119/api/users/0` while Zotero runs.
Paginate results. Never read SQLite as a fallback for an unavailable live API.
Use curated titles, creators, publication dates, venue, DOI, abstracts and citation
keys first. Verify missing detail from a primary source; leave unresolved fields
explicitly unknown. Preserve Zotero records, collections, notes, attachments,
citation keys and versions. This repository's scripts read Zotero and never write it.
No credential is needed for these local reads; never store credentials here.

Distinguish the publication date from the date of the PDF version actually filed.
An arXiv banner dates that PDF version, even when Zotero retains the first release.
The paper manifest preserves both dates, metadata provenance, explicit overrides
and SHA-256. Non-PDF blog posts/model cards remain explicit web-source records in
`papers/web_sources.json`, with their URL, citation key, date precision and summary.
They are not fake PDFs. A research paper missing its PDF remains a reported issue.

## Adding and maintaining knowledge

1. Run `python scripts/papers/new_paper.py --zotero ITEM_KEY --dry-run`, review
   metadata, then run without `--dry-run`. Collection membership is mandatory.
   A PDF-path fallback and explicit metadata overrides support non-arXiv sources.
   Never guess a missing month or author. Historical four-digit years are valid.
2. File as `papers/<year>/MM_Author_et_al._Title.pdf`, using the filed version's
   month, ASCII-folded names and underscore separators. Use `Author_and_Author`
   for two authors. Preserve the source PDF, particularly Zotero attachments.
3. Generate `papers/text/<year>/<same-name>.txt` with the extraction script.
   **Never manually edit generated text.** Fix extraction and regenerate instead.
4. Complete the chronological summary, overview, synthesis timeline and changelog
   scaffolds. Each summary needs venue/provenance, Zotero citation key, **Where it
   fits**, **What it contains**, **Strengths**, and **Limitations**, with substantive
   evidence from the source. Unfinished `TODO(new-paper)` markers must fail checks.
5. Integrate the source into the synthesis argument: compare assumptions, available
   information, decision interfaces, uncertainty, evaluation and computational cost.
   Distinguish observed results, provider claims and interpretation. Do not claim
   causal identification, optimal policies or regret guarantees without evidence.
6. On first mention of a paper within each section, include its title alongside
   author-year. Cross-document anchors must name their target document. Keep
   `SUMMARIES.md`, `SYNTHESIS.md` and `REPOSITORIES.md` project-neutral; local
   relevance, pipeline paths and deviations belong in `PROJECT_SPECIFIC.md`.
7. Register each official code snapshot in the normal refresh mapping. Verify its
   identity from paper/provider links, record source revision, retain useful source,
   configuration, scripts, patches and licenses, and exclude weights, large datasets
   and generated results. Cite **source paths and symbols, never dump line numbers**.
   After refresh, run the symbol checker. Files over 95 MB must be explicitly
   gitignored and documented with a regeneration command.
8. Log substantive changes in `CHANGELOG.md` (one dated section per day, newest
   first). Run appropriate offline regression tests and `maintain.py --check-only`.
   Report API/network failures separately from content defects. Check-only must
   preserve content and must not refresh, extract, replace files or change Git state.

## Git and downstream boundary

Only initialize local Git when authorized. Do not commit, push, create a hosted
repository, change remotes/history, or update real downstream projects unless the
owner explicitly asks. Display name: DM Library. Canonical public remote:
`https://github.com/andreasgoethals/DM_Library`. Mountpoint: `decision-models-library/`.

After owner publication, propagation discovers consumers through this checkout's
own remote identity, verifies a clean published exact commit, and updates only
the submodule path in each authorized consumer. Preview with `--dry-run`; downstream
pushing is optional and explicit. Never propagate a branch tip in place of the
reviewed commit or sweep unrelated consumer changes into a bump commit.

Downstream agents may read all shared files, record the pinned SHA in their local
notes, and create only `PROJECT_SPECIFIC.md` inside the submodule. An uncommitted
canonical edit is invisible downstream until the owner publishes and updates pins.

## Status

The owner authorized public publication to `andreasgoethals/DM_Library` on
20 October 2026. Publication status, remotes and consumer registrations must
still be verified live before propagation; authorization does not prove a clean,
published commit or authorize changes in an arbitrary consumer.
