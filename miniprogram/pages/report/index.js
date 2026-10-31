import { getAssessment, getProducts, getVideos } from '~/api/index';
import { BASE_URL } from '~/api/request';

const RISK_TEXT = { low: '低风险', mid: '中风险', high: '高风险' };
const RISK_COLOR = { low: '#15816C', mid: '#C17A26', high: '#C55A49' };

Page({
  data: {
    assessment: null,
    annotatedUrl: '',
    detections: [],
    riskLevel: null,
    riskText: '待评估',
    riskColor: '#999999',
    classificationNote: '',
    // 定向推送
    videos: [],
    products: [],
  },

  onLoad(options) {
    this.assessmentId = options.id;
  },

  onShow() {
    this.load();
  },

  load() {
    getAssessment(this.assessmentId)
      .then((res) => {
        const annotated = res.annotated_image || '';
        const detections = res.detections || [];
        const cls = res.classification || {};
        const risk = res.risk_level;

        this.setData({
          assessment: res,
          detections,
          riskLevel: risk,
          riskText: risk ? RISK_TEXT[risk] : '待评估',
          riskColor: RISK_COLOR[risk] || '#999999',
          classificationNote: cls.note || '',
          annotatedUrl: annotated ? `${BASE_URL}/files/${annotated}` : '',
        });

        this.loadRecommend();
      })
      .catch(() => {
        wx.showToast({ title: '报告加载失败', icon: 'none' });
      });
  },

  /** 定向推送：科普视频 + 商品 */
  loadRecommend() {
    getVideos().then((list) => {
      this.setData({ videos: (list || []).slice(0, 3) });
    }).catch(() => {});
    getProducts().then((list) => {
      this.setData({ products: (list || []).slice(0, 4) });
    }).catch(() => {});
  },

  onBuy(e) {
    const code = e.currentTarget.dataset.code;
    if (!code) {
      wx.showToast({ title: '该商品暂无购买链接', icon: 'none' });
      return;
    }
    wx.setClipboardData({ data: code, success: () => wx.showToast({ title: '淘口令已复制' }) });
  },

  onPreview() {
    if (!this.data.annotatedUrl) return;
    wx.previewImage({ urls: [this.data.annotatedUrl] });
  },

  onRetake() {
    wx.redirectTo({ url: '/pages/camera/index' });
  },

  onBackHome() {
    wx.switchTab({ url: '/pages/home/index' });
  },
});
