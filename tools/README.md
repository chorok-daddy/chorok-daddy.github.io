# Website maintenance

| Content | Source |
|---|---|
| People, research, publications and photos | `niil/content/` |
| Logical member/project routes | `niil/content/routes.json` |
| Course publication | Pinned `tools/course-source.json`; edit in `../courses` |
| Locale/shared paths | Imported `publication-layout.json` and `publication_layout.py` |
| Lab output ownership | `tools/site-output.json` |

`niil/ko/` and `niil/en/` contain matching language publications. Shared media,
styles, scripts and course datasets live under `niil/assets/`. The default
`/niil/` entry opens Korean. Retired top-level course routes are no longer built.
The repository root, tools and templates retain their hosting/build roles.

Build: `python3 tools/build_niil.py`. It reproduces the pinned course import,
builds both language branches, prunes obsolete owned HTML, writes the two default
entries and refreshes search metadata. `--prepared-courses` verifies the fresh
import's hashes before framing. Imports prune files from the previous pin.

Run `check_site.py`, `check_migration.py`, `check_course_source.py`,
`check_research.py`, `check_presentation.py`, `check_seo.py` and
`check_repository.py` before publishing. Keep checks local and batch publication.
Do not execute student code during document checks.

Keep `AGENTS.md` local and ignored. Keep private reviews and temporary deployments
outside Git. Compile the source-only Easter egg once into the common stylesheet.
Removed files remain recoverable in Git history; never rewrite history.
