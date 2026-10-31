import { isLoggedIn, loginByPhone, getMembers, getAssessments } from '~/api/index';

const ROLE_TEXT = { father: '父亲', mother: '母亲', child: '孩子', self: '自己' };
const RISK_TEXT = { low: '低风险', mid: '中风险', high: '高风险' };

Page({
  data: {
    loggedIn: false,
    phone: '',
    members: [],
    currentMember: null,
    currentMemberId: null,
    riskLevel: null,
    riskText: '暂无检测',
    riskColor: '#999999',
  },

  onShow() {
    const loggedIn = isLoggedIn();
    this.setData({ loggedIn, phone: wx.getStorageSync('phone') || '' });
    if (loggedIn) this.loadMembers();
  },

  loadMembers() {
    getMembers().then((list) => {
      this.setData({ members: list });
      const savedId = wx.getStorageSync('current_member_id');
      const cur = list.find((m) => m.id === savedId) || list[0];
      if (cur) this.selectMember(cur);
    }).catch(() => {
      wx.showToast({ title: '成员加载失败', icon: 'none' });
    });
  },

  selectMember(m) {
    wx.setStorageSync('current_member_id', m.id);
    this.setData({ currentMember: m, currentMemberId: m.id });
    this.loadRisk(m.id);
  },

  loadRisk(memberId) {
    getAssessments(memberId).then((list) => {
      const latest = list && list[0];
      const risk = latest && latest.risk_level;
      const color = { low: '#15816C', mid: '#C17A26', high: '#C55A49' }[risk] || '#999999';
      this.setData({
        riskLevel: risk,
        riskText: risk ? RISK_TEXT[risk] : '暂无检测',
        riskColor: color,
      });
    }).catch(() => {});
  },

  roleText(r) {
    return ROLE_TEXT[r] || r;
  },

  onSwitchMember(e) {
    const id = e.currentTarget.dataset.id;
    const m = this.data.members.find((x) => x.id === id);
    if (m) this.selectMember(m);
  },

  onPhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },

  onLogin() {
    const phone = (this.data.phone || '').trim();
    if (!/^1\d{10}$/.test(phone)) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' });
      return;
    }
    wx.showLoading({ title: '登录中' });
    loginByPhone(phone).then(() => {
      wx.hideLoading();
      this.setData({ loggedIn: true });
      this.loadMembers();
    }).catch(() => {
      wx.hideLoading();
      wx.showToast({ title: '登录失败', icon: 'none' });
    });
  },

  onDetect() {
    if (!this.data.currentMember) {
      wx.showToast({ title: '请先添加孩子', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/camera/index' });
  },

  onRecords() {
    wx.switchTab({ url: '/pages/message/index' });
  },

  onManage() {
    wx.switchTab({ url: '/pages/my/index' });
  },

  onQuestionnaire() {
    if (!this.data.currentMember) return;
    wx.navigateTo({ url: `/pages/questionnaire/index?member_id=${this.data.currentMemberId}` });
  },
});
