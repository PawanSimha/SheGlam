/**
 * SheGlam – Auth (login, signup, token storage, redirect by role)
 */

const API_BASE = window.location.origin;
const AUTH_TOKEN_KEY = "sheglam_token";
const AUTH_ROLE_KEY = "sheglam_role";
const AUTH_EMAIL_KEY = "sheglam_email";

function getToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

function setAuth(role, email) {
  if (role) localStorage.setItem(AUTH_ROLE_KEY, role);
  if (email) localStorage.setItem(AUTH_EMAIL_KEY, email);
}

function clearAuth() {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  localStorage.removeItem(AUTH_ROLE_KEY);
  localStorage.removeItem(AUTH_EMAIL_KEY);
}

function getRole() {
  return localStorage.getItem(AUTH_ROLE_KEY);
}

function getEmail() {
  return localStorage.getItem(AUTH_EMAIL_KEY);
}

function getCsrfToken() {
  const match = document.cookie.match(/csrf_access_token=([^;]+)/);
  return match ? match[1] : "";
}

function authHeaders() {
  const csrf = getCsrfToken();
  return {
    "Content-Type": "application/json",
    ...(csrf ? { "X-CSRF-TOKEN": csrf } : {}),
  };
}

function redirectByRole() {
  const role = getRole();
  if (role === "admin") window.location.href = "/admin-dashboard";
  else if (role === "artist") window.location.href = "/artist-dashboard";
  else if (role === "user") window.location.href = "/user-dashboard";
  else window.location.href = "/login";
}

// ---------- Login form ----------
async function handleLogin(e) {
  e.preventDefault();
  const form = e.target;
  const email = (form.querySelector('input[name="email"]') || {}).value?.trim();
  const password = (form.querySelector('input[name="password"]') || {}).value;
  const errEl = form.querySelector(".alert-error") || document.getElementById("login-error");

  if (!email || !password) {
    if (errEl) { errEl.textContent = "Email and password are required."; errEl.classList.remove("hidden"); }
    return;
  }

  try {
    const res = await fetch(API_BASE + "/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      if (errEl) { errEl.textContent = data.error || "Login failed."; errEl.classList.remove("hidden"); }
      return;
    }
    setAuth(data.role, data.email);
    redirectByRole();
  } catch (err) {
    if (errEl) { errEl.textContent = "Network error. Try again."; errEl.classList.remove("hidden"); }
  }
}

// ---------- Signup (user) ----------
async function handleSignupUser(e) {
  e.preventDefault();
  const form = e.target;
  const name = (form.querySelector('input[name="name"]') || {}).value?.trim();
  const email = (form.querySelector('input[name="email"]') || {}).value?.trim().toLowerCase();
  const password = (form.querySelector('input[name="password"]') || {}).value;
  const phone = (form.querySelector('input[name="phone"]') || {}).value?.trim();
  const errEl = form.querySelector(".alert-error") || document.getElementById("signup-error");

  if (!name || !email || !password) {
    if (errEl) { errEl.textContent = "Name, email and password are required."; errEl.classList.remove("hidden"); }
    return;
  }
  if (password.length < 6) {
    if (errEl) { errEl.textContent = "Password must be at least 6 characters."; errEl.classList.remove("hidden"); }
    return;
  }

  try {
    const res = await fetch(API_BASE + "/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password, phone, role: "user" }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      if (errEl) { errEl.textContent = data.error || "Signup failed."; errEl.classList.remove("hidden"); }
      return;
    }
    if (errEl) errEl.classList.add("hidden");
    window.location.href = "/login?registered=1";
  } catch (err) {
    if (errEl) { errEl.textContent = "Network error. Try again."; errEl.classList.remove("hidden"); }
  }
}

// ---------- Signup (artist) – creates user then redirects to complete profile ----------
async function handleSignupArtist(e) {
  e.preventDefault();
  const form = e.target;
  const name = (form.querySelector('input[name="name"]') || {}).value?.trim();
  const email = (form.querySelector('input[name="email"]') || {}).value?.trim().toLowerCase();
  const password = (form.querySelector('input[name="password"]') || {}).value;
  const phone = (form.querySelector('input[name="phone"]') || {}).value?.trim();
  const errEl = form.querySelector(".alert-error") || document.getElementById("signup-artist-error");

  if (!name || !email || !password) {
    if (errEl) { errEl.textContent = "Name, email and password are required."; errEl.classList.remove("hidden"); }
    return;
  }
  if (password.length < 6) {
    if (errEl) { errEl.textContent = "Password must be at least 6 characters."; errEl.classList.remove("hidden"); }
    return;
  }

  try {
    const res = await fetch(API_BASE + "/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password, phone, role: "artist" }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      if (errEl) { errEl.textContent = data.error || "Signup failed."; errEl.classList.remove("hidden"); }
      return;
    }
    if (errEl) errEl.classList.add("hidden");
    window.location.href = "/login?registered=artist";
  } catch (err) {
    if (errEl) { errEl.textContent = "Network error. Try again."; errEl.classList.remove("hidden"); }
  }
}

// ---------- Logout ----------
async function handleLogout() {
  try {
    await fetch(API_BASE + "/auth/logout", {
      method: "POST",
      headers: authHeaders(),
    });
  } catch (err) {
    console.error("Logout request failed", err);
  }
  clearAuth();
  window.location.href = "/login";
}

// ---------- Require auth (use on dashboard pages) ----------
function requireAuth(expectedRole) {
  const role = getRole();
  const isLoggedIn = !!role;
  if (!isLoggedIn) {
    window.location.href = "/login";
    return false;
  }
  if (expectedRole && role !== expectedRole) {
    redirectByRole();
    return false;
  }
  return true;
}

// ---------- Universal Navigation ----------
function updateNavigation() {
  const nav = document.getElementById("universal-nav");
  if (!nav) return;

  const role = getRole();
  const token = getToken();
  let html = '';

  // "Artists" link is useful for everyone
  html += '<a href="/artists">Browse Artists</a>';

  if (!token) {
    // Guest
    html += '<a href="/login">Login</a>';
    html += '<a href="/register-user">Register User</a>';
    html += '<a href="/register-artist">Register Artist</a>';
  } else {
    // Logged in
    if (role === 'user') {
      html += '<a href="/user-dashboard">My Bookings</a>';
    } else if (role === 'artist') {
      html += '<a href="/artist-dashboard">My Bookings</a>';
    }
    // Admin usually stays on dashboard, but we can add a link if needed.

    html += '<button type="button" class="link-style" id="logout-btn">Logout</button>';
  }

  nav.innerHTML = html;
  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) logoutBtn.addEventListener("click", handleLogout);
}
