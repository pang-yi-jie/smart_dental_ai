import { request, upload } from './request';

/** 患者登录（手机号） */
export function loginByPhone(phone) {
  return request('/api/auth/wechat', 'POST', { phone, openid: '' }).then((res) => {
    wx.setStorageSync('access_token', res.access_token);
    wx.setStorageSync('user_id', res.user_id);
    wx.setStorageSync('phone', phone);
    return res;
  });
}

/** 当前是否已登录 */
export function isLoggedIn() {
  return !!wx.getStorageSync('access_token');
}

/** 退出登录 */
export function logout() {
  wx.removeStorageSync('access_token');
  wx.removeStorageSync('user_id');
  wx.removeStorageSync('phone');
}

/** 创建病例并上传图片（同步跑 AI 分析） */
export function createCase(filePath, view, toothPosition) {
  return upload('/api/cases', filePath, {
    view,
    tooth_position: toothPosition || '',
  });
}

/** 获取单个病例 */
export function getCase(id) {
  return request(`/api/cases/${id}`);
}

/** 我的历史病例 */
export function getMyCases() {
  return request('/api/my/cases');
}

/** 商品列表 */
export function getProducts(category) {
  return request('/api/products' + (category ? `?category=${category}` : ''));
}

/** 商品详情 */
export function getProduct(id) {
  return request(`/api/products/${id}`);
}
