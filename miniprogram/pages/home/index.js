import { isLoggedIn, loginByPhone } from '~/api/index';
import { QUESTIONS, calcScore, getScoreLevel } from '~/utils/questionnaire';

Page({
  data: {
    loggedIn: false,
    phone: '',
    // 问卷
    questions: QUESTIONS,
    answers: {},
    currentIndex: 0,
    showQuestionnaire: false,
    progress: 0,
    // 健康评分
    score: null,
    scoreLevel: null,
  },

  onShow() {
    const loggedIn = isLoggedIn();
    this.setData({ loggedIn, phone: wx.getStorageSync('phone') || '' });
    if (loggedIn) this.loadLocalRecord();
  },

  /** 读取本地保存的问卷结果 */
  loadLocalRecord() {
    const saved = wx.getStorageSync('questionnaire');
    if (saved && saved.answers) {
      const score = calcScore(saved.answers);
      this.setData({ answers: saved.answers, score, scoreLevel: getScoreLevel(score) });
    }
  },

  // ---------- 登录 ----------
  onPhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },

  onLogin() {
    const phone = (this.data.phone || '').trim();
    if (!/^1\d{10}$/.test(phone)) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' });
      return;
    }
    wx.showLoading({ title: '登录中' });
    loginByPhone(phone)
      .then(() => {
        wx.hideLoading();
        this.setData({ loggedIn: true });
        this.loadLocalRecord();
        wx.showToast({ title: '登录成功' });
      })
      .catch(() => {
        wx.hideLoading();
        wx.showToast({ title: '登录失败，请检查网络', icon: 'none' });
      });
  },

  // ---------- 问卷 ----------
  onOpenQuestionnaire() {
    if (!this.data.loggedIn) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    this.setData({ showQuestionnaire: true, currentIndex: 0, progress: 0 });
  },

  onCloseQuestionnaire() {
    this.setData({ showQuestionnaire: false });
  },

  onAnswer(e) {
    const { qid, value } = e.currentTarget.dataset;
    const answers = { ...this.data.answers, [qid]: Number(value) };
    const answered = QUESTIONS.filter((q) => answers[q.id]).length;
    this.setData({
      answers,
      progress: Math.round((answered / QUESTIONS.length) * 100),
    });
  },

  onPrev() {
    if (this.data.currentIndex > 0) {
      this.setData({ currentIndex: this.data.currentIndex - 1 });
    }
  },

  onNext() {
    const { currentIndex, questions, answers } = this.data;
    const q = questions[currentIndex];
    if (!answers[q.id]) {
      wx.showToast({ title: '请选择一个答案', icon: 'none' });
      return;
    }
    if (currentIndex < questions.length - 1) {
      this.setData({ currentIndex: currentIndex + 1 });
    } else {
      this.submitQuestionnaire();
    }
  },

  submitQuestionnaire() {
    const { answers } = this.data;
    const allAnswered = QUESTIONS.every((q) => answers[q.id]);
    if (!allAnswered) {
      wx.showToast({ title: '还有题目未作答', icon: 'none' });
      return;
    }
    const score = calcScore(answers);
    wx.setStorageSync('questionnaire', { answers, date: new Date().toISOString() });
    this.setData({
      score,
      scoreLevel: getScoreLevel(score),
      showQuestionnaire: false,
    });
    wx.showToast({ title: '问卷已完成' });
  },

  // ---------- 拍照 ----------
  onStartDetect() {
    if (!this.data.loggedIn) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/camera/index' });
  },
});
