import { getProducts, getMyCases } from '~/api/index';
import { calcScore } from '~/utils/questionnaire';

/** 按护理需求分类的推荐说明 */
const CATEGORY_META = {
  device: { label: '检测设备', icon: 'device', desc: '在家随时自检' },
  toothpaste: { label: '功效牙膏', icon: 'app', desc: '针对性护理' },
  toothbrush: { label: '牙刷 / 电动牙刷', icon: 'brush', desc: '提升清洁效率' },
  other: { label: '护理用品', icon: 'shop', desc: '日常护理' },
};

Page({
  data: {
    tabs: [
      { key: 'all', label: '全部推荐' },
      { key: 'toothpaste', label: '牙膏' },
      { key: 'toothbrush', label: '牙刷' },
      { key: 'device', label: '设备' },
    ],
    activeTab: 'all',
    products: [],
    filteredProducts: [],
    // 个性化推荐
    personalTip: '',
    healthScore: null,
    categoryMeta: CATEGORY_META,
    loading: true,
  },

  onShow() {
    this.loadData();
  },

  loadData() {
    const saved = wx.getStorageSync('questionnaire');
    const score = saved && saved.answers ? calcScore(saved.answers) : null;

    getProducts()
      .then((list) => {
        const products = (list || []).map((p) => ({
          ...p,
          meta: CATEGORY_META[p.category] || CATEGORY_META.other,
        }));
        this.setData({
          products,
          healthScore: score,
          personalTip: this.buildTip(score),
          loading: false,
        });
        this.applyFilter();
      })
      .catch(() => {
        this.setData({ loading: false, personalTip: '商品加载失败，请稍后重试' });
      });
  },

  /** 根据健康分生成个性化提示 */
  buildTip(score) {
    if (score === null) return '完成口腔习惯问卷，可获得个性化护理推荐';
    if (score >= 80) return '您的口腔习惯良好，建议继续保持并定期检查';
    if (score >= 55) return '建议加强刷牙时长、规律使用牙线，并选择含氟牙膏';
    return '存在较高口腔风险，建议尽快就医检查，并配合专业护理产品';
  },

  onSwitchTab(e) {
    const key = e.currentTarget.dataset.key;
    this.setData({ activeTab: key });
    this.applyFilter();
  },

  applyFilter() {
    const { activeTab, products } = this.data;
    const filtered = activeTab === 'all' ? products : products.filter((p) => p.category === activeTab);
    this.setData({ filteredProducts: filtered });
  },

  /** 复制淘口令去购买 */
  onBuy(e) {
    const { code, url } = e.currentTarget.dataset;
    if (code) {
      wx.setClipboardData({
        data: code,
        success: () => wx.showToast({ title: '淘口令已复制，打开淘宝即可购买' }),
      });
    } else if (url) {
      wx.setClipboardData({
        data: url,
        success: () => wx.showToast({ title: '链接已复制' }),
      });
    } else {
      wx.showToast({ title: '该商品暂未上架链接', icon: 'none' });
    }
  },
});
