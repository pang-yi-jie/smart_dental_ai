const { request, BASE_URL } = require('../../utils/request');

Page({
  data: {
    caseData: null,
    annotatedUrl: '',
    detections: []
  },

  onLoad(options) {
    this.id = options.id;
    this.load();
  },

  load() {
    request('GET', '/api/cases/' + this.id).then((res) => {
      const ai = res.ai_result || {};
      const annotated = ai.annotated_image || '';
      this.setData({
        caseData: res,
        detections: ai.detections || [],
        annotatedUrl: annotated ? BASE_URL + '/files/' + annotated : ''
      });
    }).catch(() => wx.showToast({ title: '加载失败', icon: 'none' }));
  },

  statusText(status) {
    const map = {
      analyzing: '分析中', pending: '待医生审核',
      finalized: '已定稿', rejected: '已驳回重拍', failed: '分析失败'
    };
    return map[status] || status;
  }
});
