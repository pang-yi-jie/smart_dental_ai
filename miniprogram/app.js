// app.js
import { isLoggedIn } from './api/index';

App({
  onLaunch() {
    // 检查登录状态
    this.globalData.loggedIn = isLoggedIn();
  },

  globalData: {
    loggedIn: false,
  },
});
