// ═══════════════════════════════════════════════
// middleware/role-transporter.js
// ═══════════════════════════════════════════════

export default function ({ $auth, redirect }) {
  if (!$auth.loggedIn || $auth.user.role !== 'transporter') {
    redirect('/')
  }
}