const { request } = require('../../utils/request');

const STATUS = {
  analyzing: '分析中', pending: '待审核', finalized: '已定稿',
  rejected: '已驳回', failed: '失败'
};

Page({
  data: { list: [] },

  onShow() {
    this.load();
  },

  load() {
    request('GET', '/api/my/cases').then((res) => {
      this.setData({ list: res });
    }).catch(() => {
      wx.showToast({ title: '加载失败', icon: 'none' });
    });
  },

  open(e) {
    wx.navigateTo({ url: '/pages/report/report?id=' + e.currentTarget.dataset.id });
  },

  statusText(s) {
    return STATUS[s] || s;
  }
});
