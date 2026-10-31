import { isLoggedIn, logout, getMyCases } from '~/api/index';
import { calcScore, getScoreLevel } from '~/utils/questionnaire';

const STATUS_TEXT = {
  uploaded: '已上传',
  analyzing: '分析中',
  pending: '待复核',
  finalized: '已定稿',
  rejected: '需重拍',
  failed: '失败',
};

Page({
  data: {
    loggedIn: false,
    phone: '',
    healthScore: null,
    scoreLevel: null,
    records: [],
    loading: false,
    stats: { total: 0, finalized: 0, pending: 0 },
  },

  onShow() {
    const loggedIn = isLoggedIn();
    this.setData({ loggedIn, phone: wx.getStorageSync('phone') || '' });
    if (loggedIn) {
      this.loadHealth();
      this.loadRecords();
    }
  },

  loadHealth() {
    const saved = wx.getStorageSync('questionnaire');
    if (saved && saved.answers) {
      const score = calcScore(saved.answers);
      this.setData({ healthScore: score, scoreLevel: getScoreLevel(score) });
    }
  },

  loadRecords() {
    this.setData({ loading: true });
    getMyCases()
      .then((list) => {
        const records = (list || []).map((c) => ({
          ...c,
          statusText: STATUS_TEXT[c.status] || c.status,
          detCount: ((c.ai_result || {}).detections || []).length,
          dateText: this.formatDate(c.created_at),
        }));
        const stats = {
          total: records.length,
          finalized: records.filter((r) => r.status === 'finalized').length,
          pending: records.filter((r) => r.status === 'pending').length,
        };
        this.setData({ records, stats, loading: false });
      })
      .catch(() => {
        this.setData({ loading: false });
        wx.showToast({ title: '记录加载失败', icon: 'none' });
      });
  },

  formatDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    const p = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
  },

  onOpenRecord(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({ url: `/pages/report/index?id=${id}` });
  },

  onStartDetect() {
    wx.navigateTo({ url: '/pages/camera/index' });
  },

  onGoHome() {
    wx.switchTab({ url: '/pages/home/index' });
  },

  onLogout() {
    wx.showModal({
      title: '退出登录',
      content: '确认退出当前账号？',
      success: (res) => {
        if (res.confirm) {
          logout();
          this.setData({
            loggedIn: false,
            records: [],
            stats: { total: 0, finalized: 0, pending: 0 },
            healthScore: null,
            scoreLevel: null,
          });
          wx.switchTab({ url: '/pages/home/index' });
        }
      },
    });
  },
});
