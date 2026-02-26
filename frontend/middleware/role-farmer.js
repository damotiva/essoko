// ═══════════════════════════════════════════════
// middleware/role-farmer.js
// ═══════════════════════════════════════════════

export default function ({ $auth, redirect }) {
  if (!$auth.loggedIn || $auth.user.role !== 'farmer') {
    redirect('/')
  }
}