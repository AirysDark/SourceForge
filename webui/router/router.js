const routes = {};
export function registerRoute(name, fn) { routes[name] = fn; }

function render() {
  const name = location.hash.replace('#','') || 'repo';
  const root = document.getElementById("appRoot");
  if (routes[name]) routes[name](root);
}

export function initRouter() {
  window.addEventListener('hashchange', render);
  render();
}
