import { createCase } from '~/api/index';

Page({
  data: {
    view: 'occlusal',
    tooth: '',
    img: '',
    uploading: false,
  },

  onReady() {
    this.ctx = wx.createCameraContext();
  },

  onSwitchView(e) {
    this.setData({ view: e.currentTarget.dataset.view });
  },

  onToothInput(e) {
    this.setData({ tooth: e.detail.value });
  },

  takePhoto() {
    this.ctx.takePhoto({
      quality: 'high',
      success: (res) => this.setData({ img: res.tempImagePath }),
      fail: () => wx.showToast({ title: '拍照失败', icon: 'none' }),
    });
  },

  retake() {
    this.setData({ img: '' });
  },

  upload() {
    if (!this.data.img) {
      wx.showToast({ title: '请先拍照', icon: 'none' });
      return;
    }
    this.setData({ uploading: true });
    wx.showLoading({ title: 'AI 分析中...', mask: true });

    createCase(this.data.img, this.data.view, this.data.tooth)
      .then((res) => {
        wx.hideLoading();
        this.setData({ uploading: false });
        wx.redirectTo({ url: `/pages/report/index?id=${res.id}` });
      })
      .catch((err) => {
        wx.hideLoading();
        this.setData({ uploading: false });
        wx.showToast({ title: '上传失败，请重试', icon: 'none' });
      });
  },
});
