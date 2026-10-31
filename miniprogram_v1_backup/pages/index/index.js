const auth = require('../../utils/auth');

Page({
  data: {
    phone: '',
    loggedIn: false
  },

  onShow() {
    this.setData({ loggedIn: auth.isLoggedIn() });
  },

  onPhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },

  login() {
    const phone = this.data.phone.trim();
    if (!/^1\d{10}$/.test(phone)) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' });
      return;
    }
    wx.showLoading({ title: '登录中' });
    auth.loginByPhone(phone).then(() => {
      wx.hideLoading();
      this.setData({ loggedIn: true });
      wx.showToast({ title: '登录成功' });
    }).catch(() => {
      wx.hideLoading();
      wx.showToast({ title: '登录失败', icon: 'none' });
    });
  },

  startDetect() {
    if (!auth.isLoggedIn()) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/camera/camera' });
  }
});
