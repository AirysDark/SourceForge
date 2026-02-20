class SfThemeCheck extends HTMLElement {
  connectedCallback() {
    const style = getComputedStyle(document.documentElement);
    const ok = style.getPropertyValue('--sf-bg') ? "OK" : "MISSING";
    this.innerHTML = `<div class="card"><strong>Theme Status:</strong> ${ok}</div>`;
  }
}
customElements.define('sf-theme-check', SfThemeCheck);
