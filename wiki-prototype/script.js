const links = [...document.querySelectorAll('.nav-link[href^="#"]')];
const sections = links
  .map((link) => document.querySelector(link.getAttribute('href')))
  .filter(Boolean);

const observer = new IntersectionObserver((entries) => {
  const visible = entries
    .filter((entry) => entry.isIntersecting)
    .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

  if (!visible) return;

  links.forEach((link) => {
    const selected = link.getAttribute('href') === `#${visible.target.id}`;
    link.classList.toggle('active', selected);
    if (selected) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}, { rootMargin: '-15% 0px -65% 0px', threshold: [0, 0.1, 0.5] });

sections.forEach((section) => observer.observe(section));

const resultNodes = [...document.querySelectorAll('[data-result]')];

const readPath = (source, path) => path
  .split('.')
  .reduce((value, key) => value?.[key], source);

const formatResult = (value, node) => {
  const digits = Number(node.dataset.digits ?? 2);
  const scaled = node.dataset.format === 'percent' ? value * 100 : value;
  return new Intl.NumberFormat('en-GB', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits
  }).format(scaled) + (node.dataset.format === 'percent' ? '%' : '');
};

if (resultNodes.length) {
  fetch('../docs/media/recovery_model/results.json')
    .then((response) => {
      if (!response.ok) throw new Error(`Recovery results unavailable (${response.status})`);
      return response.json();
    })
    .then((results) => {
      resultNodes.forEach((node) => {
        const value = readPath(results, node.dataset.result);
        if (typeof value !== 'number' || !Number.isFinite(value)) {
          node.textContent = 'Unavailable';
          return;
        }
        node.textContent = formatResult(value, node);
      });
    })
    .catch(() => {
      resultNodes.forEach((node) => {
        node.textContent = 'Result unavailable';
        node.classList.add('result-unavailable');
      });
    });
}
