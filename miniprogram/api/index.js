import { request, upload, BASE_URL } from './request';

/** 家长登录（手机号） */
export function loginByPhone(phone) {
  return request('/api/auth/wechat', 'POST', { phone, openid: '' }).then((res) => {
    wx.setStorageSync('access_token', res.access_token);
    wx.setStorageSync('account_id', res.account_id);
    wx.setStorageSync('phone', phone);
    return res;
  });
}

export function isLoggedIn() {
  return !!wx.getStorageSync('access_token');
}

export function logout() {
  wx.removeStorageSync('access_token');
  wx.removeStorageSync('account_id');
}

/** 家庭成员 */
export function getMembers() {
  return request('/api/members');
}

export function createMember(data) {
  return request('/api/members', 'POST', data);
}

/** 档案级问卷 */
export function saveQuestionnaire(memberId, answers) {
  return request(`/api/members/${memberId}/questionnaire`, 'POST', { answers });
}

export function getQuestionnaire(memberId) {
  return request(`/api/members/${memberId}/questionnaire`);
}

/** 评估 */
export function createAssessment(memberId, filePath, view) {
  return upload('/api/assessments', filePath, { member_id: memberId, view });
}

export function getAssessments(memberId) {
  return request(`/api/members/${memberId}/assessments`);
}

export function getAssessment(id) {
  return request(`/api/assessments/${id}`);
}

/** 护牙任务 */
export function getTasks(memberId) {
  return request(`/api/members/${memberId}/tasks`);
}

/** 内容：科普视频 + 商品（定向推送） */
export function getVideos(category) {
  return request('/api/videos' + (category ? `?category=${category}` : ''));
}

export function getProducts(category) {
  return request('/api/products' + (category ? `?category=${category}` : ''));
}

export { BASE_URL };
