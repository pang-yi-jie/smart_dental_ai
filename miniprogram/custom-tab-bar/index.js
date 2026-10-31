Component({
  data: {
    value: '',
    list: [
      { icon: 'home', value: 'home', label: '首页' },
      { icon: 'shop', value: 'message', label: '好物' },
      { icon: 'user', value: 'my', label: '我的' },
    ],
  },

  lifetimes: {
    ready() {
      const pages = getCurrentPages();
      const curPage = pages[pages.length - 1];
      if (!curPage) return;
      const nameRe = /pages\/(\w+)\/index/.exec(curPage.route);
      if (nameRe && nameRe[1]) {
        this.setData({ value: nameRe[1] });
      }
    },
  },

  methods: {
    onTap(e) {
      const { value } = e.currentTarget.dataset;
      wx.switchTab({ url: `/pages/${value}/index` });
    },
  },
});
