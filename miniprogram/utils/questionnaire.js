/** 口腔健康习惯问卷配置 */
export const QUESTIONS = [
  {
    id: 'brush_times',
    title: '您每天刷牙几次？',
    options: [
      { label: '1 次或更少', value: 1 },
      { label: '2 次', value: 2 },
      { label: '3 次及以上', value: 3 },
    ],
  },
  {
    id: 'brush_duration',
    title: '每次刷牙大约多长时间？',
    options: [
      { label: '少于 1 分钟', value: 1 },
      { label: '1~2 分钟', value: 2 },
      { label: '2 分钟以上', value: 3 },
    ],
  },
  {
    id: 'floss',
    title: '您使用牙线或冲牙器吗？',
    options: [
      { label: '从不', value: 1 },
      { label: '偶尔', value: 2 },
      { label: '经常', value: 3 },
    ],
  },
  {
    id: 'sugar',
    title: '您吃甜食或含糖饮料的频率？',
    options: [
      { label: '经常（每天）', value: 1 },
      { label: '偶尔（每周几次）', value: 2 },
      { label: '很少', value: 3 },
    ],
  },
  {
    id: 'check',
    title: '您多久做一次口腔检查？',
    options: [
      { label: '从未 / 想不起来', value: 1 },
      { label: '一年一次以上', value: 2 },
      { label: '半年一次或更频繁', value: 3 },
    ],
  },
];

/**
 * 根据问卷答案计算健康评分（满分 100）
 * 每道题 1~3 分，最低 5 分满分 15 分，映射到 0~100
 */
export function calcScore(answers) {
  const values = QUESTIONS.map((q) => Number(answers[q.id]) || 1);
  const total = values.reduce((a, b) => a + b, 0);
  const min = QUESTIONS.length * 1;
  const max = QUESTIONS.length * 3;
  return Math.round(((total - min) / (max - min)) * 100);
}

/** 根据评分给出口腔健康提示 */
export function getScoreLevel(score) {
  if (score >= 80) return { label: '习惯良好', color: '#00a870', tip: '保持得很好，继续坚持定期检查。' };
  if (score >= 55) return { label: '需要改善', color: '#ff8f1f', tip: '建议加强刷牙时长与牙线使用。' };
  return { label: '需要重视', color: '#d54941', tip: '存在较高口腔风险，建议尽快做专业检查。' };
}
