(() => {
  const params = new URLSearchParams(location.search);
  if (params.get('embedded') === '1') {
    document.documentElement.classList.add('course-embedded');
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') parent.postMessage({type:'course-overlay-close'}, '*');
    });
  }
  if (params.get('embedded') === '1') {
    document.addEventListener('click', e => {
      const link = e.target.closest('a[href]');
      if (link && new URL(link.href).pathname.endsWith('/assignment.html')) {
        e.preventDefault(); parent.postMessage({type:'course-overlay-return',href:link.href}, '*');
      }
    });
  }
  let dialog, trigger;
  function prepare() {
    if (dialog) return;
    dialog = document.createElement('dialog');
    dialog.className = 'course-overlay';
    dialog.setAttribute('aria-label', '학습자료 보기');
    dialog.innerHTML = '<div class="overlay-bar"><div class="overlay-tabs" role="tablist" aria-label="자료"></div><a class="overlay-full">전체 페이지</a><button type="button" class="overlay-close" aria-label="닫기">닫기 ×</button></div><div class="overlay-panels"></div>';
    document.body.append(dialog);
    dialog.querySelector('.overlay-close').onclick = () => dialog.close();
    dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => {
      document.documentElement.classList.remove('course-dialog-open');
      dialog.querySelector('.overlay-panels').replaceChildren();
      trigger?.focus();
    });
    window.addEventListener('message', e => {
      if (![...dialog.querySelectorAll('iframe')].some(frame => frame.contentWindow === e.source)) return;
      if (e.data?.type === 'course-overlay-close') dialog.close();
      if (e.data?.type === 'course-overlay-return') {
        const target = new URL(e.data.href, location.href);
        if (target.protocol !== location.protocol || target.host !== location.host) return;
        dialog.close();
        if (target.pathname === location.pathname) document.getElementById('lab-activities')?.scrollIntoView({behavior:'smooth'});
        else location.href = target.href;
      }
    });
  }
  document.addEventListener('click', e => {
    const link = e.target.closest('a[data-course-overlay]');
    if (!link || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button !== 0 || !window.HTMLDialogElement) return;
    e.preventDefault();
    prepare(); trigger = link;
    const links = [...document.querySelectorAll('a[data-course-overlay]')];
    const choices = new Map();
    [link, ...links].forEach(a => choices.has(a.href) || choices.set(a.href, a.dataset.courseOverlay || a.textContent.trim()));
    const tabs = dialog.querySelector('.overlay-tabs');
    const panels = dialog.querySelector('.overlay-panels');
    tabs.replaceChildren(); panels.replaceChildren();
    let count = 0;
    for (const [href, label] of choices) {
      const index = count++;
      const tab = document.createElement('button');
      const panel = document.createElement('div');
      tab.type = 'button'; tab.role = 'tab'; tab.textContent = label; tab.setAttribute('aria-selected','false'); tab.tabIndex = -1;
      tab.id = 'course-tab-' + index; panel.id = 'course-panel-' + index;
      tab.setAttribute('aria-controls', panel.id); panel.setAttribute('role','tabpanel'); panel.setAttribute('aria-labelledby', tab.id);
      const activate = () => {
        [...tabs.children].forEach(t => { t.setAttribute('aria-selected', String(t === tab)); t.tabIndex = t === tab ? 0 : -1; });
        [...panels.children].forEach(p => p.hidden = p !== panel);
        if (!panel.firstChild) {
          const frame = document.createElement('iframe');
          const url = new URL(href); url.searchParams.set('embedded','1');
          frame.src = url.href; frame.title = label; panel.append(frame);
        }
        dialog.querySelector('.overlay-full').href = href;
      };
      tab.onclick = activate;
      tab.onkeydown = e => {
        if (!['ArrowLeft','ArrowRight','Home','End'].includes(e.key)) return;
        e.preventDefault(); const items = [...tabs.children];
        const next = e.key === 'Home' ? 0 : e.key === 'End' ? items.length - 1 : (items.indexOf(tab) + (e.key === 'ArrowRight' ? 1 : -1) + items.length) % items.length;
        items[next].click(); items[next].focus();
      };
      tabs.append(tab); panels.append(panel);
      if (index === 0) activate(); else panel.hidden = true;
    }
    dialog.showModal();
    document.documentElement.classList.add('course-dialog-open');
    tabs.firstElementChild.focus();
  });
})();
