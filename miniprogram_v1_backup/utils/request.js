// 封装网络请求：自动带 token，统一错误处理。
const { BASE_URL } = require('./config');

function request(method, path, data) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: BASE_URL + path,
      method: method,
      data: data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + (wx.getStorageSync('token') || '')
      },
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(res.data && res.data.detail ? res.data.detail : res);
        }
      },
      fail(err) {
        reject(err);
      }
    });
  });
}

// 上传图片：POST 表单 + 文件
function upload(path, filePath, formData) {
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: BASE_URL + path,
      filePath: filePath,
      name: 'file',
      formData: formData || {},
      header: { 'Authorization': 'Bearer ' + (wx.getStorageSync('token') || '') },
      success(res) {
        try {
          const data = JSON.parse(res.data);
          if (res.statusCode >= 200 && res.statusCode < 300) resolve(data);
          else reject(data.detail || data);
        } catch (e) {
          reject(res);
        }
      },
      fail: reject
    });
  });
}

module.exports = { request, upload, BASE_URL };
