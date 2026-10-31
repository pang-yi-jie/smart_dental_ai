Component({
  options: {
    styleIsolation: 'shared',
  },
  properties: {
    navType: {
      type: String,
      value: 'title',
    },
    titleText: {
      type: String,
      value: '',
    },
  },
  data: {
    statusHeight: 0,
  },
  lifetimes: {
    ready() {
      const info = wx.getWindowInfo ? wx.getWindowInfo() : wx.getSystemInfoSync();
      this.setData({ statusHeight: info.statusBarHeight || 0 });
    },
  },
});
