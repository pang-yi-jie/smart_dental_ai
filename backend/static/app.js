const token = localStorage.getItem('token');
if (!token) location.href = 'login.html';

const STATUS_TEXT = {
  uploaded: '已上传', analyzing: '分析中', pending: '待审核',
  finalized: '已定稿', rejected: '已驳回', failed: '失败'
};

let currentTab = 'pending';
let currentCaseId = null;

function api(path, options = {}) {
  return fetch(path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token,
      ...(options.headers || {})
    }
  }).then(async (r) => {
    const data = await r.json().catch(() => ({}));
    if (r.status === 401) { location.href = 'login.html'; throw new Error('未登录'); }
    if (!r.ok) throw new Error(data.detail || '请求失败');
    return data;
  });
}

function logout() {
  localStorage.clear();
  location.href = 'login.html';
}

function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab').forEach(t =>
    t.classList.toggle('active', t.dataset.tab === tab));
  loadCases();
}

async function loadCases() {
  const q = currentTab === 'all' ? '' : '?status=' + currentTab;
  try {
    const list = await api('/api/clinic/cases' + q);
    renderList(list);
  } catch (e) {
    document.getElementById('caseList').innerHTML = '<div class="empty">加载失败</div>';
  }
}

function renderList(list) {
  const el = document.getElementById('caseList');
  if (!list.length) { el.innerHTML = '<div class="empty">暂无病例</div>'; return; }
  el.innerHTML = list.map(c => `
    <div class="case-item ${c.id === currentCaseId ? 'active' : ''}" onclick="openCase(${c.id})">
      <div class="c1">${c.patient_phone || '未知'}</div>
      <div class="c2">${c.tooth_position || '-'} · ${c.view === 'occlusal' ? '咬合面' : '唇颊面'}</div>
      <div class="c3">${STATUS_TEXT[c.status] || c.status}</div>
    </div>`).join('');
}

async function openCase(id) {
  currentCaseId = id;
  const c = await api('/api/clinic/cases/' + id);
  renderDetail(c);
  loadCases();
}

function renderDetail(c) {
  const ai = c.ai_result || {};
  const dets = ai.detections || [];
  const img = ai.annotated_image ? '/files/' + ai.annotated_image : '';
  const note = (c.doctor_edited && c.doctor_edited.suggestion) || '';

  document.getElementById('detail').innerHTML = `
    <div class="detail-head">
      <span class="badge">${STATUS_TEXT[c.status] || c.status}</span>
      <span class="meta">患者 ${c.patient_phone || '未知'} · 牙位 ${c.tooth_position || '-'} · ${c.view === 'occlusal' ? '咬合面' : '唇颊面'}</span>
    </div>
    ${img ? `<a href="${img}" target="_blank"><img class="annotated" src="${img}" alt="标注图"></a>` : '<div class="empty">无标注图</div>'}
    <div class="h">AI 检测结果（${dets.length}）</div>
    <div class="det-list">
      ${dets.map(d => `<span class="chip">${d.label} <i>${(d.confidence * 100).toFixed(0)}%</i></span>`).join('') || '<span class="empty">未检出目标</span>'}
    </div>
    <div class="h">医生诊断意见</div>
    <textarea id="note" placeholder="填写诊断意见 / 建议（定稿前必填）">${note}</textarea>
    <div class="btns">
      <button class="btn" onclick="save()">保存</button>
      <button class="btn danger" onclick="reject()">驳回重拍</button>
      <button class="btn primary" onclick="finalize()">定稿</button>
    </div>
  `;
}

async function save() {
  if (!currentCaseId) return;
  const note = document.getElementById('note').value;
  await api('/api/clinic/cases/' + currentCaseId + '/diagnosis', {
    method: 'PUT',
    body: JSON.stringify({ diagnosis: { suggestion: note } })
  });
  toast('已保存');
}

async function finalize() {
  if (!currentCaseId) return;
  const note = document.getElementById('note').value;
  if (!note.trim()) { toast('请先填写诊断意见'); return; }
  await api('/api/clinic/cases/' + currentCaseId + '/diagnosis', {
    method: 'PUT',
    body: JSON.stringify({ diagnosis: { suggestion: note } })
  });
  await api('/api/clinic/cases/' + currentCaseId + '/finalize', { method: 'POST' });
  toast('已定稿');
  loadCases();
  openCase(currentCaseId);
}

async function reject() {
  if (!currentCaseId) return;
  if (!confirm('确认驳回，让患者重新拍摄？')) return;
  await api('/api/clinic/cases/' + currentCaseId + '/reject', { method: 'POST' });
  toast('已驳回');
  loadCases();
  openCase(currentCaseId);
}

function toast(msg) {
  let el = document.getElementById('toast');
  if (!el) {
    el = document.createElement('div');
    el.id = 'toast';
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 1500);
}

document.addEventListener('DOMContentLoaded', () => {
  const doc = JSON.parse(localStorage.getItem('doctor') || '{}');
  document.getElementById('doctorName').textContent = doc.name || '';
  loadCases();
});
