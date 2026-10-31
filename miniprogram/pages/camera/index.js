import { createAssessment } from '~/api/index';

Page({
  data: {
    view: 'occlusal',
    img: '',
    uploading: false,
  },

  onReady() {
    this.ctx = wx.createCameraContext();
  },

  onSwitchView(e) {
    this.setData({ view: e.currentTarget.dataset.view });
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
    const memberId = wx.getStorageSync('current_member_id');
    if (!memberId) {
      wx.showToast({ title: '请先选择孩子', icon: 'none' });
      return;
    }
    this.setData({ uploading: true });
    wx.showLoading({ title: 'AI 分析中...', mask: true });

    createAssessment(memberId, this.data.img, this.data.view)
      .then((res) => {
        wx.hideLoading();
        this.setData({ uploading: false });
        wx.redirectTo({ url: `/pages/report/index?id=${res.id}` });
      })
      .catch(() => {
        wx.hideLoading();
        this.setData({ uploading: false });
        wx.showToast({ title: '上传失败，请重试', icon: 'none' });
      });
  },
});
