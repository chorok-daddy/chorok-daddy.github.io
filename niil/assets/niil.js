document.documentElement.classList.add("js");
const menu = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#site-nav");
menu?.addEventListener("click", () => {
  const open = menu.getAttribute("aria-expanded") !== "true";
  menu.setAttribute("aria-expanded", String(open));
  navigation.classList.toggle("open", open);
});
const query = document.querySelector('#project-search');
const status = document.querySelector('#project-status');
const topic = document.querySelector('#project-topic');
if (query && status) {
  const initialTopic = new URLSearchParams(location.search).get('topic');
  if (topic && [...topic.options].some(option => option.value === initialTopic)) topic.value = initialTopic;
  const projects = [...document.querySelectorAll('[data-project]')];
  const filter = () => {
    let count = 0;
    projects.forEach(project => {
      const matches = project.textContent.toLowerCase().includes(query.value.trim().toLowerCase()) && (!status.value || project.dataset.status === status.value) && (!topic?.value || project.dataset.topic === topic.value);
      project.hidden = !matches;
      if (matches) count++;
    });
    document.querySelector('#project-count').textContent = `${count} project${count === 1 ? '' : 's'}`;
    document.querySelector('#no-projects').hidden = count > 0;
  };
  query.addEventListener('input', filter);
  status.addEventListener('change', filter);
  topic?.addEventListener('change', filter);
  filter();
}
const toc = document.querySelector('.toc');
if (toc) document.querySelectorAll('.prose h2, .prose h3').forEach((heading, index) => {
  if (!heading.id) heading.id = `section-${index + 1}`;
  const anchor = document.createElement('a');
  anchor.href = `#${heading.id}`;
  anchor.textContent = heading.textContent;
  toc.append(anchor);
});

const publicationSearch = document.querySelector('#publication-search');
if (publicationSearch) {
  const year = document.querySelector('#publication-year');
  const type = document.querySelector('#publication-type');
  const publications = [...document.querySelectorAll('[data-publication]')];
  const filterPublications = () => {
    let count = 0;
    const term = publicationSearch.value.trim().toLocaleLowerCase();
    publications.forEach(item => {
      const matches = item.textContent.toLocaleLowerCase().includes(term) && (!year.value || item.dataset.year === year.value) && (!type.value || item.dataset.type === type.value);
      item.hidden = !matches;
      if (matches) count++;
    });
    document.querySelector('#publication-count').textContent = `${count} publication${count === 1 ? '' : 's'}`;
    document.querySelector('#publication-empty').hidden = count !== 0;
  };
  publicationSearch.addEventListener('input', filterPublications);
  year.addEventListener('change', filterPublications);
  type.addEventListener('change', filterPublications);
}
