# DM Library

A standalone knowledge repository for **models and methods for choosing actions**.
The owner's Zotero collection matching **Decision Models** defines the exact corpus.
Its selection concerns fast, schema-conditioned decision models: thirteen
research papers and seven web-only release posts/model cards. It is maintained
here and consumed elsewhere as a pinned, read-only Git submodule.

## The commands that matter

Run from this library's root with the maintenance dependencies installed. Commands
are written separately for Windows PowerShell.

**Audit without changing library content:**

```powershell
python scripts/maintain.py --check-only
```

**Run normal maintenance**, including missing text extraction and registered code
refreshes:

```powershell
python scripts/maintain.py
```

**Import an owner-requested paper already in the selected collection:**

```powershell
python scripts/papers/new_paper.py --zotero ITEM_KEY --dry-run
```

```powershell
python scripts/papers/new_paper.py --zotero ITEM_KEY
```

Complete the generated summary, overview, synthesis and changelog scaffolds; they
deliberately fail checks until the intellectual work is finished.

**Preview downstream updates after the owner publishes this repository:**

```powershell
python scripts/propagate_to_downstream.py --dry-run
```

**When the owner authorizes downstream pin changes**, update and commit only each
consumer's submodule path; add `--push` only to publish those consumer commits:

```powershell
python scripts/propagate_to_downstream.py
```

Canonical public remote: [andreasgoethals/DM_Library](https://github.com/andreasgoethals/DM_Library).
Display name: **DM Library**. Publication and downstream updates remain separate
actions; verify the published commit and authorized consumers before propagation.

## Read the library

| File | Purpose |
|---|---|
| [SYNTHESIS.md](SYNTHESIS.md) | Cross-paper argument, timelines, assumptions, evaluation differences and open questions |
| [SUMMARIES.md](SUMMARIES.md) | One substantive summary per selected source, with provenance, strengths, limitations and Zotero citation keys |
| [REPOSITORIES.md](REPOSITORIES.md) | Official code snapshot overview, exact revisions, source paths and symbols |
| [CHANGELOG.md](CHANGELOG.md) | Substantive updates, newest first |
| [AGENTS.md](AGENTS.md) | Scope, owner authorization and canonical/downstream write boundary |
| [PROJECT_SPECIFIC.template.md](PROJECT_SPECIFIC.template.md) | Template for ignored downstream-local relevance and deviations |
| [papers/manifest.json](papers/manifest.json) | Filed PDF provenance, curated metadata, versions, overrides and hashes |
| [papers/web_sources.json](papers/web_sources.json) | Explicit records for selected sources that have no PDFs |

Shared documents are project-neutral. The conceptual subject can accommodate
decision theory, optimization under uncertainty, decision-focused learning and
policy learning, but those topics are not added unless the owner selects sources.
The collection's numeric prefix is not part of its identity.

## Setup and repository layout

Python 3.10+ and Git are required. A fresh local virtual environment is optional;
do not copy another library's environment.

```powershell
python -m venv .venv
```

```powershell
.venv\Scripts\Activate.ps1
```

```powershell
python -m pip install -r requirements.txt
```

This is a knowledge base, not an installable model package. Dependencies support
maintenance only; downstream projects need not install them.

```text
papers/<year>/MM_Author_et_al._Title.pdf
papers/text/<year>/<same-name>.txt
papers/manifest.json
papers/web_sources.json
repositories/<stable-name>.txt
scripts/maintain.py
scripts/propagate_to_downstream.py
scripts/papers/
scripts/checks/
scripts/dumps/
scripts/hooks/
scripts/lib/
```

Files use the **date of the version filed**, ASCII-folded surnames and underscore
separators. Two authors use `Author_and_Author`; three or more use `Author_et_al.`.
Historical four-digit years are supported. Publication dates are retained separately
from PDF-version dates. Unknown months are never replaced with today's month.
Generated paper text must never be edited manually.

## Zotero and source ingestion

Zotero must be running with its Local API enabled. The scripts paginate the live
API, resolve linked and stored attachments through Zotero, and use curated metadata
and citation keys. They never write Zotero or use SQLite as a stale fallback.

```powershell
python scripts/checks/check_zotero_sync.py --json
```

The checker detects missing, extra and duplicate papers; stale metadata, hash/date
differences and broken attachments; and missing/orphaned text. It distinguishes
publication dates from confirmed arXiv version dates. API unavailability is explicit
(exit 2), not a clean audit. A mismatch does not authorize adding/deleting sources.
Future additions always require an owner request.

For a non-arXiv PDF, use an explicit path and verified metadata overrides:

```powershell
python scripts/papers/new_paper.py 'C:\path\paper.pdf' --title 'Verified title' --authors 'First Author,Second Author' --year 1955 --month 07 --dry-run
```

Run `--help` for available overrides and `--no-scaffold`. A path fallback does not
replace the requirement that the canonical corpus match the selected collection;
prefer `--zotero ITEM_KEY` together with a supplied PDF path when resolving a missing
attachment. The tool records overrides and refuses to move a Zotero-owned attachment.

The seven selected blog posts/model cards are represented explicitly in the web
registry and summaries, with source URLs and review dates. No PDF or publication
month is fabricated. TypeSafe's launch is dated 15 September 2026. Intern-Decision-4B
is dated 26 September 2026: its first substantive model-card/checkpoint upload is
corroborated by a same-day public demo announcement from Hugging Face's open-source
team. Git history alone would not establish public availability.
Perplexity v1.1 uses its official public announcement
on 6 October, separately from the private checkpoint commit on 5 October.
These three date corrections were applied to the existing Zotero records on
20 October 2026; citation keys, collection memberships and attachments were preserved.
The web registry retains the primary evidence and the distinct artifact dates.
Web-only registration is limited to blog posts and model cards; it cannot excuse a
missing research-paper PDF. Future authorized web-source additions require a
reviewed registry entry, summary, overview row, synthesis entry and changelog line.

## Maintenance tools and checks

| Tool | Behavior |
|---|---|
| `scripts/papers/new_paper.py` | Membership-enforced import, metadata overrides, atomic filing, text extraction and chronological scaffolds |
| `scripts/papers/extract_paper_text.py` | Generated UTF-8 text; `--all` fills missing mirrors, `--check` audits parity and text quality |
| `scripts/checks/check_docs.py` | Identity-based PDF/web coverage, chronology, section completeness, citation keys, links/anchors, neutrality and unfinished scaffolds |
| `scripts/checks/check_symbols.py` | Validates cited source paths/symbols and rejects snapshot line-number citations |
| `scripts/checks/check_zotero_sync.py` | Read-only live collection/metadata/attachment audit |
| `scripts/checks/check_paper_versions.py` | Reports newer arXiv versions and unverifiable sources; never replaces a paper |
| `scripts/dumps/refresh_repositories.py` | Registered, revision-recorded source snapshots with targeted refresh, filtering, atomic replacement and shrink guard |
| `scripts/maintain.py` | Consolidated stages, selection/skipping and nonzero failure summary; rechecks symbols after refresh |
| `scripts/propagate_to_downstream.py` | Remote-identity consumer discovery, exact published pins and path-limited commits |

```powershell
python scripts/maintain.py --only zotero
```

```powershell
python scripts/maintain.py --skip repos
```

```powershell
python scripts/dumps/refresh_repositories.py --only SearchJev
```

```powershell
python scripts/checks/check_symbols.py --verbose
```

```powershell
python -B -m unittest discover -s scripts/checks -p 'test_*.py'
```

Check-only audits extraction rather than generating it, skips snapshot mutation,
and disables local bytecode writes. It still contacts Zotero and arXiv. Network
failures are reported separately in stage output; the consolidated command returns
nonzero if a selected check fails. Offline tests use generated PDFs, mocks and
disposable Git repositories, including published pins ahead/behind origin,
unrelated consumer changes and byte-for-byte dry-run preservation.

Install the version-controlled offline pre-commit checks:

```powershell
python scripts/hooks/install.py
```

```powershell
python scripts/hooks/install.py --status
```

The hook checks documents and relevant snapshot citations. It does not contact
Zotero or upstream services. `--uninstall` removes the hooks-path setting.

## Code snapshots

The [implementation guide](REPOSITORIES.md) documents all 13 registered sources.
Refreshes preserve stable filenames, upstream commit revisions, licenses and useful
configuration/scripts. Weights, checkpoints, large datasets and generated responses
are excluded. Failed downloads leave the old snapshot intact; a replacement below
half the old size is refused unless deliberately overridden with `--force-shrink`.
No unrelated infrastructure snapshot is inherited. Cite source symbols and paths,
never generated-dump line numbers.

Anything above 95 MB must be explicitly ignored and documented with its targeted
regeneration command. Current snapshots are below that threshold. Rechecked on
20 October 2026: Li's author repository publishes a website and manuscript, but
does not supply the experimental supplement; Microsoft-Decision-1's release links
hosted access without model implementation code. See the evidence and exclusions
under [coverage boundaries](REPOSITORIES.md#coverage-boundaries).

## Publication and downstream submodule workflow

The owner selected public publication at
[andreasgoethals/DM_Library](https://github.com/andreasgoethals/DM_Library).
Papers and code retain their original authorship and individual license terms;
this library does not relicense third-party material. As checked on 20 October
2026, the arXiv pages for
[Evaluating and Benchmarking the System One Model Jev](https://arxiv.org/abs/2609.37647),
[JevOut](https://arxiv.org/abs/2609.30243), and
[General Decision Models](https://arxiv.org/abs/2610.03935) use
[arXiv's non-exclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html).
That hosting license is distinct from a general redistribution license. Source
URLs, version identifiers and retained upstream notices document provenance.

From a consumer repository, add the published library:

```powershell
git submodule add https://github.com/andreasgoethals/DM_Library.git decision-models-library
```

For an existing consumer checkout:

```powershell
git submodule update --init --recursive decision-models-library
```

To review and pin a specific **published** library commit:

```powershell
git -C decision-models-library fetch origin
```

```powershell
git -C decision-models-library checkout --detach PUBLISHED_COMMIT_SHA
```

```powershell
git add -- decision-models-library
```

The owner can then commit the reviewed pin. Read `CHANGELOG.md` first; downstream
copies see only the pinned commit. Never edit shared material inside a consumer.
Copy the project template to the ignored `PROJECT_SPECIFIC.md` for local notes,
including that exact SHA. Those untracked notes need their own backup.

For authorized multi-consumer updates, propagation discovers `.gitmodules` entries
by this checkout's own `origin` identity, including normalized SSH/HTTPS forms. It
rejects a dirty/unpublished library and dirty or pending consumer pins, fetches the
exact published commit and commits only the submodule path. `--root` and `--depth`
bound discovery; dry-run does not fetch, write pins or create commits. Real
propagation was not run during setup.

### Automatic updates after publication

A submodule records an exact commit in its parent repository. Pushing this library
does not move that recorded commit, even if `.gitmodules` names a tracking branch.
The local propagation script is an explicit command, not a push trigger.

For updates on every published `main` commit, configure GitHub Actions for the
canonical remote and explicitly authorized consumer repositories:

1. Validate the pushed library commit with offline tests and content checks. Zotero
   reconciliation runs locally before publication because a hosted runner cannot
   reach the owner's Desktop Local API.
2. Dispatch a `dm-library-updated` event to each explicitly registered consumer,
   carrying the canonical repository identity and the exact validated commit SHA.
3. In each consumer, verify the expected source identity and commit ancestry, fetch
   that SHA, and update only `decision-models-library`. An old or duplicate event
   must not roll a newer pin back. Serialize updates per consumer.
4. Open a pin-only pull request and enable automatic merging after the consumer's
   required checks succeed. The consumer's branch rules must permit this; a failing
   check leaves an actionable pull request instead of silently adopting the update.

Use a GitHub App installed only on the selected repositories, with library read
access and consumer contents/pull-request permissions. The canonical repository's
default `GITHUB_TOKEN` does not grant access to unrelated repositories. Put any
app key in GitHub Actions secrets. Use the app token for pin pull requests so their
checks can run normally.

This is a configuration recipe, not an enabled integration. No consumer pin or
cross-repository workflow is configured by publishing this library.
Once an update is merged on GitHub, local consumer checkouts still need
`git pull --recurse-submodules`; fresh clones use `git clone --recurse-submodules`.
GitHub cannot update files in an idle local checkout.

References: [Git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules),
[repository dispatch](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event),
and [GitHub Actions token scope](https://docs.github.com/en/actions/concepts/security/github_token).

## Shared Literature workspace

This independent repository can also live under the local `0. Literature`
workspace alongside other libraries. Its Git history and remote remain separate.
The shared entry points are `scripts/maintain.py` and
`scripts/propagate_to_downstream.py`; source-specific stages and identity are
defined in `scripts/library.json`. Both commands work in an independent clone.

From the parent workspace, `python scripts/maintain.py` runs libraries in
parallel. `python scripts/propagate_to_downstream.py --dry-run` previews updates
to existing consumer registrations under Projects; `--push` explicitly publishes
pin-only updates. Libraries are independent opt-ins, never an all-or-nothing bundle.
Pending registrations and unrelated consumer work must be preserved.
