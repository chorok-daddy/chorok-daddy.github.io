/* Locale routing for complete Korean/English course documents and popup controls. */
(() => {
  if (!document.body.classList.contains('niil-course')) return;
  const current = new URL(location.href);
  const english = current.pathname.startsWith('/niil/en/courses/');
  // Preserve old shared UI-locale URLs, now opening the actual English body.
  if (!english && current.searchParams.get('lang') === 'en') {
    current.pathname = current.pathname.replace('/niil/courses/', '/niil/en/courses/');
    current.searchParams.delete('lang');
    location.replace(current.href);
    return;
  }
  document.documentElement.lang = english ? 'en' : 'ko';
  document.documentElement.dataset.uiLanguage = english ? 'en' : 'ko';
  const labels = new Map(Object.entries({
    '연구':'Research', '논문':'Publications', '구성원':'People', '강의자료':'Course',
    '문의·지원':'Contact', '자연모사 인공지능 연구실':'Nature-inspired Intelligence Lab',
    '광운대학교':'Kwangwoon University · Seoul, Korea', '저자·이용 안내':'Author & use',
    '학습자료':'Study material', '자료 받기 ↗':'Get materials ↗',
    '학습용 노트북 미리보기':'Study notebook preview', '학습용 노트북 다운로드':'Study notebook download',
    '실습용 노트북 미리보기':'Practice notebook preview', '실습용 노트북 다운로드':'Practice notebook download',
    'Colab 노트북 미리보기':'Colab notebook preview', 'Colab 노트북 다운로드':'Colab notebook download',
    '학습용 mlx 스크립트 미리보기':'Study mlx script preview', '학습용 mlx 스크립트 다운로드':'Study mlx script download',
    '실습용 mlx 스크립트 미리보기':'Practice mlx script preview', '실습용 mlx 스크립트 다운로드':'Practice mlx script download',
    'mlx 스크립트 미리보기':'mlx script preview', 'mlx 스크립트 다운로드':'mlx script download',
    'MATLAB Online 실습 시작 ↗':'Run in MATLAB Online ↗', 'Colab 실습 시작 ↗':'Run in Colab ↗',
    'MATLAB 실행 ↗':'Run in MATLAB ↗', 'Colab 실행 ↗':'Run in Colab ↗', 'MATLAB Online 실행 ↗':'Run in MATLAB Online ↗', '닫기 ×':'Close ×', '자료 닫기':'Close material', '시험 형식 예시':'Exam format examples',
    '중간시험':'Midterm exam', '기말시험':'Final exam', '실습':'Practice', '실행 조건':'Requirements', '실습 전에':'Before you start',
    '기록 항목과 확인할 점':'Records and checks', '설명':'Explanation', '선택 실습':'Optional practice'
  }));
  function translate(root) {
    if (!english) return;
    root.querySelectorAll('a,button,h2,summary,.footer-identity strong,.footer-identity span').forEach(el => {
      const replacement = labels.get(el.textContent.trim());
      if (replacement && !el.querySelector('math,pre,code')) { el.textContent = replacement; el.lang = 'en'; }
    });
    root.querySelectorAll('[aria-label]').forEach(el => {
      const replacement = labels.get(el.getAttribute('aria-label'));
      if (replacement) el.setAttribute('aria-label', replacement);
    });
    root.querySelectorAll('[data-course-overlay]').forEach(el => {
      const replacement = labels.get(el.dataset.courseOverlay);
      if (replacement) el.dataset.courseOverlay = replacement;
    });
    root.querySelectorAll('[data-course-label-en]').forEach(el => { el.textContent = el.dataset.courseLabelEn; });
  }
  function localeUrl(url) {
    if (url.origin !== location.origin) return url;
    const path = url.pathname;
    if (path === '/niil/courses/' || path === '/niil/courses/index.html' || path === '/niil/courses/reuse.html') {
      if (english) url.pathname = path.replace('/niil/', '/niil/en/');
    } else if (path.startsWith('/niil/courses/') && (path.endsWith('.html') || path.endsWith('/'))) {
      if (english) url.pathname = path.replace('/niil/courses/', '/niil/en/courses/');
      url.searchParams.delete('lang');
    } else if (english && path.startsWith('/niil/') && !path.startsWith('/niil/en/') && !path.startsWith('/niil/assets/') && !path.startsWith('/niil/courses/') && (path.endsWith('/') || path.endsWith('.html'))) {
      url.pathname = path.replace('/niil/', '/niil/en/');
    }
    return url;
  }
  function languageLinks() {
    document.querySelectorAll('[data-course-language]').forEach(link => {
      const url = new URL(location.href);
      const target = link.dataset.courseLanguage;
      const source = url.pathname.replace('/niil/en/courses/', '/niil/courses/');
      url.pathname = target === 'en' ? source.replace('/niil/courses/', '/niil/en/courses/') : source;
      url.searchParams.delete('lang');
      url.searchParams.delete('v');
      link.href = url.pathname + url.search + url.hash;
      if ((target === 'en') === english) link.setAttribute('aria-current', 'true'); else link.removeAttribute('aria-current');
    });
  }
  document.querySelectorAll('a[href]:not([data-course-language])').forEach(link => {
    const url = localeUrl(new URL(link.href));
    if (url.origin === location.origin) link.href = url.pathname + url.search + url.hash;
  });
  if (english) {
    document.querySelectorAll('.site-header,.site-footer').forEach(el => { el.lang = 'en'; });
    document.querySelector('.brand')?.setAttribute('aria-label', 'NiiL home');
    const menu = document.querySelector('.menu-toggle');
    if (menu) menu.textContent = 'Menu ☰';
    document.querySelector('#site-nav')?.setAttribute('aria-label', 'Main navigation');
    document.querySelector('.language-switch')?.setAttribute('aria-label', 'Language');
    document.querySelector('.skip')?.replaceChildren(document.createTextNode('Skip to content'));
    if (document.body.hasAttribute('data-course-home')) {
      const title = document.querySelector('main h1');
      if (title) {
        title.textContent = document.body.dataset.courseTitleEn; title.lang = 'en';
        document.title = document.body.dataset.courseTitleEn + ' · NiiL';
        const byline = document.querySelector('main > .byline');
        if (byline?.textContent.trim() === title.textContent.trim()) byline.hidden = true;
      }
      document.querySelectorAll('.schedule-number').forEach(el => {
        const week = el.textContent.trim().match(/^(\d+)주$/);
        if (week) { el.textContent = 'Week ' + week[1]; el.style.whiteSpace = 'nowrap'; }
      });
    }
    translate(document);
    // Popup controls are created on demand by the course viewer.
    new MutationObserver(records => records.forEach(record => record.addedNodes.forEach(node => {
      if (node.nodeType === 1 && (node.matches('dialog') || node.closest('dialog'))) translate(node.parentElement || node);
    }))).observe(document.body, {childList:true, subtree:true});
  }
  languageLinks();
  window.addEventListener('hashchange', languageLinks);
})();
