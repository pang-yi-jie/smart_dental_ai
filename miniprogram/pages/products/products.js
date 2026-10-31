const { request } = require('../../utils/request');

const CATEGORY = {
  device: '检测设备', toothpaste: '牙膏', toothbrush: '牙刷', other: '其他'
};

Page({
  data: { list: [] },

  onLoad() {
    this.load();
  },

  load() {
    request('GET', '/api/products').then((res) => {
      this.setData({ list: res });
    }).catch(() => {
      wx.showToast({ title: '加载失败', icon: 'none' });
    });
  },

  catText(c) {
    return CATEGORY[c] || c;
  },

  buy(e) {
    const code = e.currentTarget.dataset.code;
    if (!code) {
      wx.showToast({ title: '该商品暂无淘口令', icon: 'none' });
      return;
    }
    wx.setClipboardData({
      data: code,
      success: () => wx.showToast({ title: '淘口令已复制，去淘宝打开' })
    });
  }
});
