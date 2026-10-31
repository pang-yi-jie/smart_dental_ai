// 登录逻辑。
const { request } = require('./request');

// 手机号登录（MVP：手动输入手机号；生产可改用「微信一键授权手机号」）
function loginByPhone(phone) {
  return request('POST', '/api/auth/wechat', { phone: phone, openid: '' })
    .then((res) => {
      wx.setStorageSync('token', res.access_token);
      return res;
    });
}

function isLoggedIn() {
  return !!wx.getStorageSync('token');
}

function logout() {
  wx.removeStorageSync('token');
}

module.exports = { loginByPhone, isLoggedIn, logout };
