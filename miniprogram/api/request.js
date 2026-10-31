import config from '~/config';

const { baseUrl } = config;

/** 通用请求封装：自动带 token，统一错误处理 */
export function request(url, method = 'GET', data = {}) {
  const header = { 'content-type': 'application/json' };
  const token = wx.getStorageSync('access_token');
  if (token) header.Authorization = `Bearer ${token}`;

  return new Promise((resolve, reject) => {
    wx.request({
      url: baseUrl + url,
      method,
      data,
      header,
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          if (res.statusCode === 401) {
            wx.removeStorageSync('access_token');
          }
          reject(res.data || res);
        }
      },
      fail: reject,
    });
  });
}

/** 上传文件（图片） */
export function upload(url, filePath, formData = {}) {
  const header = {};
  const token = wx.getStorageSync('access_token');
  if (token) header.Authorization = `Bearer ${token}`;

  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: baseUrl + url,
      filePath,
      name: 'file',
      formData,
      header,
      success(res) {
        try {
          const data = JSON.parse(res.data);
          if (res.statusCode >= 200 && res.statusCode < 300) resolve(data);
          else reject(data.detail || data);
        } catch (e) {
          reject(res);
        }
      },
      fail: reject,
    });
  });
}

export const BASE_URL = baseUrl;
export default request;
