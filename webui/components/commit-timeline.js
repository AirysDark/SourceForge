class SfCommitTimeline extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <div class="card">
        <h3>Commit Timeline</h3>
        <div class="timeline">
          <div class="timeline-item"><strong>a1b2c3</strong> — Initial commit</div>
          <div class="timeline-item"><strong>d4e5f6</strong> — UI improvements</div>
          <div class="timeline-item"><strong>g7h8i9</strong> — Add diff viewer</div>
        </div>
      </div>
    `;
  }
}
customElements.define('sf-commit-timeline', SfCommitTimeline);
