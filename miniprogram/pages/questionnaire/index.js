import { getQuestionnaire, saveQuestionnaire } from '~/api/index';
import { QUESTIONS } from '~/utils/questionnaire';

Page({
  data: {
    memberId: null,
    questions: QUESTIONS,
    answers: {},
    saved: false,
  },

  onLoad(options) {
    this.setData({ memberId: Number(options.member_id) });
    this.loadExisting();
  },

  loadExisting() {
    getQuestionnaire(this.data.memberId).then((res) => {
      if (res && res.answers) {
        this.setData({ answers: res.answers, saved: true });
      }
    }).catch(() => {});
  },

  onAnswer(e) {
    const { qid, value } = e.currentTarget.dataset;
    this.setData({ [`answers.${qid}`]: Number(value) });
  },

  submit() {
    const allAnswered = QUESTIONS.every((q) => this.data.answers[q.id]);
    if (!allAnswered) {
      wx.showToast({ title: '还有题目未作答', icon: 'none' });
      return;
    }
    saveQuestionnaire(this.data.memberId, this.data.answers).then(() => {
      this.setData({ saved: true });
      wx.showToast({ title: '已保存' });
      setTimeout(() => wx.navigateBack(), 800);
    }).catch(() => {
      wx.showToast({ title: '保存失败', icon: 'none' });
    });
  },
});
