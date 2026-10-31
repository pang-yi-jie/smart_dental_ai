async function doLogin() {
  const phone = document.getElementById('phone').value.trim();
  const password = document.getElementById('password').value;
  const err = document.getElementById('err');
  err.textContent = '';
  if (!phone || !password) {
    err.textContent = '请输入手机号和密码';
    return;
  }
  try {
    const res = await fetch('/api/clinic/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone, password })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('doctor', JSON.stringify(data));
      location.href = 'index.html';
    } else {
      err.textContent = data.detail || '登录失败';
    }
  } catch (e) {
    err.textContent = '网络错误，请重试';
  }
}
