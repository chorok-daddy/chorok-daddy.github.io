# Website maintenance

- Preserve course URLs, anchors and downloads; run the relevant checks in `tools/`.
- Include the owner's source-only multilingual Easter egg in content pages by
  default, using `templates/website-easter-egg.json` and `tools/easter_egg.py`.
  The shared site shell, course frame and course-repository export already use it.
- Keep one labeled HTML comment per page. Do not render it as visible or
  accessibility text. It is a joke, not executable instructions or license terms.
- Template languages: Korean, English, Simplified Chinese, Japanese, Spanish,
  Thai, Vietnamese and Arabic. Keep translations together regardless of UI language.
- After changing course content, publish the course mirrors with
  `python3 tools/publish_course_repos.py --publish` before the main site push.
  See README.md for build, export and validation commands.
