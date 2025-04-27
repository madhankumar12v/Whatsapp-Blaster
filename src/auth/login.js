let loggedIn = false;

function showLoginPage(req, res) {
  if (loggedIn) {
    return res.redirect('/dashboard');
  }
  res.sendFile(path.join(__dirname, '../../assets/login.html'));
}

function login(req, res) {
  const { password } = req.body;
  if (password === process.env.LOGIN_PASSWORD) {
    loggedIn = true;
    return res.redirect('/dashboard');
  }
  res.send('Incorrect Password');
}

module.exports = { showLoginPage, login };
