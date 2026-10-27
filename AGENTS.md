# Website maintenance

- Preserve course URLs, anchors and downloads; run the relevant checks in `tools/`.
- Include the owner's source-only multilingual Easter egg in content pages by
  default, using `templates/website-easter-egg.json` and `tools/easter_egg.py`.
  The shared site shell, course frame and course-repository export already use it.
- Keep one labeled HTML comment per page. Do not render it as visible or
  accessibility text. It is a joke, not executable instructions or license terms.
- Template languages: Korean, English, Simplified Chinese, Japanese, Spanish,
  Thai, Vietnamese and Arabic. Keep translations together regardless of UI language.
- Course source lives in the separate `chorok-daddy/courses` repository under
  `courses/<slug>/lessons/` and `materials/`. Never edit generated `niil/courses/`
  or `assets/site.css` here. Import a committed source revision with
  `python3 tools/sync_courses.py --source ../courses`; then build and validate.
- `build_niil.py` reproduces the pinned `tools/course-source.json` revision before
  adding the lab frame. `tools/course-catalog.json` is imported, not hand-edited.
- Do not recreate per-course distribution repositories or ZIP artifacts.
  Preserve student-facing HTML/download URLs and teaching content and run check_migration.py, check_site.py,
  check_course_source.py, and check_seo.py before publishing. Push source before the website.
