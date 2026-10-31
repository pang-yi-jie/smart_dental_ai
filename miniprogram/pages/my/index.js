import { isLoggedIn, logout, getMembers, createMember } from '~/api/index';

const ROLE_TEXT = { father: '父亲', mother: '母亲', child: '孩子', self: '自己' };
const ROLE_OPTIONS = [
  { key: 'father', label: '父亲' },
  { key: 'mother', label: '母亲' },
  { key: 'child', label: '孩子' },
  { key: 'self', label: '自己' },
];

Page({
  data: {
    loggedIn: false,
    phone: '',
    members: [],
    showForm: false,
    form: { role: 'child', name: '', birth: '', gender: '' },
    roleOptions: ROLE_OPTIONS,
  },

  onShow() {
    const loggedIn = isLoggedIn();
    this.setData({ loggedIn, phone: wx.getStorageSync('phone') || '' });
    if (loggedIn) this.loadMembers();
  },

  loadMembers() {
    getMembers().then((list) => {
      this.setData({ members: list });
    }).catch(() => {});
  },

  roleText(r) {
    return ROLE_TEXT[r] || r;
  },

  // ---------- 添加成员 ----------
  onAddMember() {
    this.setData({ showForm: true, form: { role: 'child', name: '', birth: '', gender: '' } });
  },

  onCloseForm() {
    this.setData({ showForm: false });
  },

  onFormInput(e) {
    const field = e.currentTarget.dataset.field;
    this.setData({ [`form.${field}`]: e.detail.value });
  },

  onPickRole(e) {
    this.setData({ 'form.role': e.currentTarget.dataset.role });
  },

  onPickGender(e) {
    this.setData({ 'form.gender': e.currentTarget.dataset.gender });
  },

  submitMember() {
    const { role, name, birth, gender } = this.data.form;
    if (!name.trim()) {
      wx.showToast({ title: '请填写姓名', icon: 'none' });
      return;
    }
    createMember({ role, name: name.trim(), birth, gender }).then(() => {
      this.setData({ showForm: false });
      this.loadMembers();
      wx.showToast({ title: '已添加' });
    }).catch(() => {
      wx.showToast({ title: '添加失败', icon: 'none' });
    });
  },

  onLogout() {
    wx.showModal({
      title: '退出登录',
      content: '确认退出当前账号？',
      success: (res) => {
        if (res.confirm) {
          logout();
          this.setData({ loggedIn: false, members: [] });
          wx.switchTab({ url: '/pages/home/index' });
        }
      },
    });
  },
});
