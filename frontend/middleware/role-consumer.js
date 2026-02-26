// ═══════════════════════════════════════════════
// middleware/role-consumer.js
// ═══════════════════════════════════════════════

export default function ({ $auth, redirect }) {
  if (!$auth.loggedIn || $auth.user.role !== 'consumer') {
    redirect('/')
  }
}