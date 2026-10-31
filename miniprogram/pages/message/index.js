import { getMembers, getAssessments, getTasks } from '~/api/index';

const RISK_TEXT = { low: '低风险', mid: '中风险', high: '高风险' };
const RISK_COLOR = { low: '#15816C', mid: '#C17A26', high: '#C55A49' };

Page({
  data: {
    members: [],
    currentMemberId: null,
    records: [],
    tasks: [],
  },

  onShow() {
    this.loadMembers();
  },

  loadMembers() {
    getMembers().then((list) => {
      this.setData({ members: list });
      const savedId = wx.getStorageSync('current_member_id');
      const cur = list.find((m) => m.id === savedId) || list[0];
      if (cur) this.selectMember(cur.id);
    }).catch(() => {});
  },

  onSwitchMember(e) {
    this.selectMember(e.currentTarget.dataset.id);
  },

  selectMember(memberId) {
    wx.setStorageSync('current_member_id', memberId);
    this.setData({ currentMemberId: memberId });
    this.loadRecords(memberId);
    this.loadTasks(memberId);
  },

  loadRecords(memberId) {
    getAssessments(memberId).then((list) => {
      const records = (list || []).map((a) => ({
        ...a,
        riskText: a.risk_level ? RISK_TEXT[a.risk_level] : '待评估',
        riskColor: RISK_COLOR[a.risk_level] || '#999999',
        dateText: this.formatDate(a.created_at),
        detCount: (a.detections || []).length,
      }));
      this.setData({ records });
    }).catch(() => {});
  },

  loadTasks(memberId) {
    getTasks(memberId).then((list) => {
      this.setData({ tasks: list || [] });
    }).catch(() => {});
  },

  formatDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    const p = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
  },

  onOpenRecord(e) {
    wx.navigateTo({ url: `/pages/report/index?id=${e.currentTarget.dataset.id}` });
  },

  onNewDetect() {
    wx.navigateTo({ url: '/pages/camera/index' });
  },
});
