// ═══════════════════════════════════════════════
// middleware/guest.js  — Redirect logged-in users away from auth pages
// ═══════════════════════════════════════════════

export default function ({ $auth, redirect }) {
  if ($auth.loggedIn) redirect('/')
}