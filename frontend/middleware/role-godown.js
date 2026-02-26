// ═══════════════════════════════════════════════
// middleware/role-godown.js
// ═══════════════════════════════════════════════

export default function ({ $auth, redirect }) {
  if (!$auth.loggedIn || $auth.user.role !== 'godown') {
    redirect('/')
  }
}