(() => {
  const embedded = new URLSearchParams(location.search).get('embedded') === '1';
  if (embedded) {
    document.documentElement.classList.add('course-embedded');
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') parent.postMessage({type:'course-close'}, location.origin === 'null' ? '*' : location.origin);
    });
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href]');
      if (!a || !new URL(a.href).pathname.endsWith('/assignment.html') || e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      parent.postMessage({type:'course-exercise', href:a.href}, location.origin === 'null' ? '*' : location.origin);
    });
    return;
  }
  let dialog, frame, trigger;
  function prepare() {
    dialog = document.createElement('dialog');
    dialog.className = 'course-overlay';
    dialog.setAttribute('aria-labelledby','course-overlay-title');
    dialog.innerHTML = '<header class="overlay-bar"><strong id="course-overlay-title">학습자료</strong><a class="overlay-full">전체 페이지 ↗</a><button type="button" class="overlay-close" aria-label="학습자료 닫기">닫기 ×</button></header><div class="overlay-content"></div>';
    document.body.append(dialog);
    dialog.querySelector('button').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', e => {
      const r = dialog.getBoundingClientRect();
      if (e.target === dialog && (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom)) dialog.close();
    });
    dialog.addEventListener('close', () => {
      document.documentElement.classList.remove('course-dialog-open');
      dialog.querySelector('.overlay-content').replaceChildren();
      frame = null;
      trigger?.focus();
    });
    window.addEventListener('message', e => {
      if (!frame || e.source !== frame.contentWindow || e.origin !== location.origin) return;
      if (e.data?.type === 'course-close') dialog.close();
      if (e.data?.type === 'course-exercise') {
        const target = new URL(e.data.href, location.href);
        if (target.origin !== location.origin || !target.pathname.endsWith('/assignment.html')) return;
        dialog.close();
        if (target.pathname === location.pathname) document.getElementById('lab-activities')?.scrollIntoView();
        else location.href = target.href;
      }
    });
  }
  document.addEventListener('click', e => {
    const a = e.target.closest('a[data-course-overlay]');
    if (!a || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || !window.HTMLDialogElement) return;
    const url = new URL(a.href);
    if (url.origin !== location.origin) return;
    e.preventDefault();
    if (!dialog) prepare();
    trigger = a;
    dialog.querySelector('.overlay-full').href = a.href;
    dialog.querySelector('#course-overlay-title').textContent = a.dataset.courseOverlay || '학습자료';
    url.searchParams.set('embedded','1');
    frame = document.createElement('iframe');
    frame.src = url.href;
    frame.title = a.dataset.courseOverlay || '학습자료';
    dialog.querySelector('.overlay-content').replaceChildren(frame);
    dialog.showModal();
    document.documentElement.classList.add('course-dialog-open');
    dialog.querySelector('button').focus();
  });
})();
