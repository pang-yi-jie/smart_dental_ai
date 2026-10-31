/** 后端配置 */
export const config = {
  // 后端地址：本地开发用 127.0.0.1:8000（需勾选「不校验合法域名」）
  // 上线后改成正式 HTTPS 域名
  baseUrl: 'http://127.0.0.1:8000',
  // 是否使用 mock 数据（对接真实后端时设为 false）
  useMock: false,
};

export default config;
