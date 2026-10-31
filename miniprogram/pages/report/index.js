import { getCase, getProducts } from '~/api/index';
import { BASE_URL } from '~/api/request';

const STATUS_TEXT = {
  uploaded: '已上传',
  analyzing: 'AI 分析中',
  pending: '待医生复核',
  finalized: '已定稿',
  rejected: '需重新拍摄',
  failed: '分析失败',
};

Page({
  data: {
    caseData: null,
    annotatedUrl: '',
    detections: [],
    statusText: '',
    doctorSuggestion: '',
    // 推荐商品
    recommendTitle: '',
    recommendProducts: [],
  },

  onLoad(options) {
    this.caseId = options.id;
    this.load();
  },

  onShow() {
    if (this.loaded) this.load();
  },

  load() {
    getCase(this.caseId)
      .then((res) => {
        this.loaded = true;
        const ai = res.ai_result || {};
        const annotated = ai.annotated_image || '';
        const detections = ai.detections || [];
        const edited = res.doctor_edited || {};

        this.setData({
          caseData: res,
          detections,
          statusText: STATUS_TEXT[res.status] || res.status,
          doctorSuggestion: edited.suggestion || '',
          annotatedUrl: annotated ? `${BASE_URL}/files/${annotated}` : '',
        });

        this.loadRecommend(detections.length);
      })
      .catch(() => {
        wx.showToast({ title: '报告加载失败', icon: 'none' });
      });
  },

  /** 加载推荐商品（根据检测结果个性化） */
  loadRecommend(detCount) {
    getProducts()
      .then((list) => {
        if (!list || !list.length) return;
        // 简单推荐策略：检测到问题（有检出）→ 推荐牙膏/牙刷为主
        let picked = list;
        let title = '精选口腔护理好物';
        if (detCount > 0) {
          title = '根据您的检测结果，建议关注这些护理产品';
          picked = list.filter((p) => p.category !== 'device');
          if (!picked.length) picked = list;
        }
        this.setData({ recommendTitle: title, recommendProducts: picked.slice(0, 6) });
      })
      .catch(() => {
        // 无商品时静默
      });
  },

  /** 复制淘口令 */
  onBuy(e) {
    const { code } = e.currentTarget.dataset;
    if (!code) {
      wx.showToast({ title: '该商品暂无购买链接', icon: 'none' });
      return;
    }
    wx.setClipboardData({
      data: code,
      success: () => wx.showToast({ title: '淘口令已复制，打开淘宝即可' }),
    });
  },

  /** 预览标注大图 */
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
