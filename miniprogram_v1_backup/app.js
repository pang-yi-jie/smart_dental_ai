App({
  onLaunch() {
    // 静默登录：拿到 code（生产环境配合后端换 openid；MVP 先存着备用）
    wx.login({
      success: (res) => {
        this.globalData.code = res.code;
      },
      fail: () => {}
    });
  },
  globalData: {
    code: ''
  }
});
