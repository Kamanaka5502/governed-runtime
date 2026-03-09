window.onload = async function() {
  const res = await fetch('/api/status');
  const orgs = await res.json();
  const tbody = document.querySelector('#orgTable tbody');
  const sel = document.getElementById('orgSelect');
  orgs.forEach(o => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${o.org}</td>
      <td class="${o.secure ? 'secure' : 'insecure'}">${o.secure ? '✓ YES' : '✗ NO'}</td>
      <td>${(o.mean_control * 100).toFixed(1)}%</td>
      <td>${(o.stability * 100).toFixed(1)}%</td>
      <td>${o.timestamp}</td>
      <td style="font-family:monospace;font-size:11px">${o.hash}</td>`;
    tbody.appendChild(tr);
    const opt = document.createElement('option');
    opt.value = o.org; opt.textContent = o.org;
    sel.appendChild(opt);
  });
};

async function loadTimeline() {
  const org = document.getElementById('orgSelect').value;
  const res = await fetch(`/api/timeline?org=${encodeURIComponent(org)}`);
  const data = await res.json();
  document.getElementById('timeline').textContent = JSON.stringify(data, null, 2);
}
