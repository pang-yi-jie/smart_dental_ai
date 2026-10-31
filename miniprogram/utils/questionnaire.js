/** 口腔健康习惯问卷（档案级，填一次偶尔更新） */

export const QUESTIONS = [
  {
    id: 'clean',
    title: '孩子每天刷牙几次？',
    options: [
      { label: '1 次或更少', value: 1 },
      { label: '2 次', value: 2 },
      { label: '3 次及以上', value: 3 },
    ],
  },
  {
    id: 'sugar',
    title: '孩子吃甜食或含糖饮料的频率？',
    options: [
      { label: '经常（每天）', value: 1 },
      { label: '偶尔（每周几次）', value: 2 },
      { label: '很少', value: 3 },
    ],
  },
  {
    id: 'fluoride',
    title: '孩子是否使用含氟牙膏？',
    options: [
      { label: '否', value: 1 },
      { label: '不清楚', value: 2 },
      { label: '是', value: 3 },
    ],
  },
  {
    id: 'caries_history',
    title: '孩子是否有龋齿史？',
    options: [
      { label: '有', value: 1 },
      { label: '不清楚', value: 2 },
      { label: '无', value: 3 },
    ],
  },
  {
    id: 'symptom',
    title: '目前是否有牙齿不适症状？',
    options: [
      { label: '有（疼痛/肿胀等）', value: 1 },
      { label: '不清楚', value: 2 },
      { label: '无', value: 3 },
    ],
  },
];

/** 根据答案计算健康习惯评分（0~100） */
export function calcScore(answers) {
  const values = QUESTIONS.map((q) => Number(answers[q.id]) || 1);
  const total = values.reduce((a, b) => a + b, 0);
  const min = QUESTIONS.length * 1;
  const max = QUESTIONS.length * 3;
  return Math.round(((total - min) / (max - min)) * 100);
}

/** 根据评分给出口腔健康提示（语义色对齐 WeUI） */
export function getScoreLevel(score) {
  if (score >= 80) return { label: '习惯良好', color: '#07C160', tip: '保持得很好，继续坚持定期检查。' };
  if (score >= 55) return { label: '需要改善', color: '#FF9500', tip: '建议加强刷牙时长与牙线使用。' };
  return { label: '需要重视', color: '#FA5151', tip: '存在较高口腔风险，建议尽快做专业检查。' };
}
