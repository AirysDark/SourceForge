import { registerRoute, initRouter } from './router/router.js';

function repo(root) {
  root.innerHTML = `
    <div class="tabbar">
      <div class="tab active">Code</div>
      <div class="tab">Pull Requests</div>
      <div class="tab">Commits</div>
      <div class="tab">Diff</div>
    </div>
    <sf-diff-viewer></sf-diff-viewer>
    <div style="margin-top:12px;"></div>
    <sf-commit-timeline></sf-commit-timeline>
  `;
}

registerRoute('repo', repo);

window.addEventListener('DOMContentLoaded', () => {
  initRouter();
});
