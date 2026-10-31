const { upload } = require('../../utils/request');

Page({
  data: {
    view: 'occlusal',   // occlusal 咬合面 / buccal 唇颊面
    tooth: '',          // 牙位（FDI，如 16）
    img: '',            // 拍到的临时图片
    uploading: false
  },

  onReady() {
    this.ctx = wx.createCameraContext();
  },

  onViewChange(e) {
    this.setData({ view: e.detail.value });
  },

  onToothInput(e) {
    this.setData({ tooth: e.detail.value });
  },

  takePhoto() {
    this.ctx.takePhoto({
      quality: 'high',
      success: (res) => this.setData({ img: res.tempImagePath }),
      fail: () => wx.showToast({ title: '拍照失败', icon: 'none' })
    });
  },

  upload() {
    if (!this.data.img) {
      wx.showToast({ title: '请先拍照', icon: 'none' });
      return;
    }
    this.setData({ uploading: true });
    wx.showLoading({ title: 'AI 分析中' });
    upload('/api/cases', this.data.img, {
      view: this.data.view,
      tooth_position: this.data.tooth
    }).then((res) => {
      wx.hideLoading();
      this.setData({ uploading: false });
      wx.redirectTo({ url: '/pages/report/report?id=' + res.id });
    }).catch(() => {
      wx.hideLoading();
      this.setData({ uploading: false });
      wx.showToast({ title: '上传失败', icon: 'none' });
    });
  }
});
