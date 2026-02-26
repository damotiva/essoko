<template>
  <div class="bg-light min-vh-100 py-4">
    <div class="container px-4">

      <!-- Page Header -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 class="fw-bold text-earth-green mb-0">Admin Dashboard</h2>
          <p class="text-muted small mb-0">Platform overview — all roles, all activity</p>
        </div>
        <div class="d-flex gap-2">
          <nuxt-link to="/admin/users" class="btn btn-outline-success btn-sm">
            <i class="fas fa-users me-1"></i> Manage Users
          </nuxt-link>
          <nuxt-link to="/admin/godowns" class="btn btn-success btn-sm">
            <i class="fas fa-warehouse me-1"></i> Manage Godowns
          </nuxt-link>
        </div>
      </div>

      <!-- Stats Row -->
      <div class="row g-3 mb-4">
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm rounded-3 h-100">
            <div class="card-body text-center py-4">
              <div class="fs-1 mb-2">👤</div>
              <div class="display-6 fw-bold text-earth-green">{{ stats.total_users || 0 }}</div>
              <div class="text-muted small">Total Users</div>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm rounded-3 h-100">
            <div class="card-body text-center py-4">
              <div class="fs-1 mb-2">🏚️</div>
              <div class="display-6 fw-bold text-earth-green">{{ stats.total_godowns || 0 }}</div>
              <div class="text-muted small">Godowns</div>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm rounded-3 h-100">
            <div class="card-body text-center py-4">
              <div class="fs-1 mb-2">📦</div>
              <div class="display-6 fw-bold text-earth-green">{{ stats.total_listings || 0 }}</div>
              <div class="text-muted small">Active Listings</div>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm rounded-3 h-100">
            <div class="card-body text-center py-4">
              <div class="fs-1 mb-2">🛒</div>
              <div class="display-6 fw-bold text-earth-green">{{ stats.total_orders || 0 }}</div>
              <div class="text-muted small">Total Orders</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Second Stats Row -->
      <div class="row g-3 mb-4">
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm rounded-3">
            <div class="card-body py-3 px-3">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <div class="text-muted small">Farmers</div>
                  <div class="fw-bold fs-4">{{ stats.total_farmers || 0 }}</div>
                </div>
                <span class="fs-2">🌱</span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm rounded-3">
            <div class="card-body py-3 px-3">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <div class="text-muted small">Consumers</div>
                  <div class="fw-bold fs-4">{{ stats.total_consumers || 0 }}</div>
                </div>
                <span class="fs-2">🍽️</span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm rounded-3">
            <div class="card-body py-3 px-3">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <div class="text-muted small">Transporters</div>
                  <div class="fw-bold fs-4">{{ stats.total_transporters || 0 }}</div>
                </div>
                <span class="fs-2">🚚</span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm rounded-3">
            <div class="card-body py-3 px-3">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <div class="text-muted small">Pending Orders</div>
                  <div class="fw-bold fs-4 text-warning">{{ stats.pending_orders || 0 }}</div>
                </div>
                <span class="fs-2">⏳</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Nav Cards -->
      <div class="row g-3 mb-4">
        <div class="col-6 col-md-3" v-for="nav in quickNav" :key="nav.to">
          <nuxt-link :to="nav.to" class="text-decoration-none">
            <div class="card border-0 shadow-sm rounded-3 h-100 card-hover">
              <div class="card-body text-center py-4">
                <div class="fs-2 mb-2">{{ nav.icon }}</div>
                <div class="fw-semibold text-dark small">{{ nav.label }}</div>
                <div class="text-muted" style="font-size:0.75rem">{{ nav.desc }}</div>
              </div>
            </div>
          </nuxt-link>
        </div>
      </div>

      <!-- Recent Orders Table -->
      <div class="card border-0 shadow-sm rounded-3 mb-4">
        <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center pt-3">
          <h5 class="fw-bold mb-0">Recent Orders</h5>
          <nuxt-link to="/admin/orders" class="btn btn-outline-success btn-sm">View All</nuxt-link>
        </div>
        <div class="card-body p-0">
          <div v-if="loadingOrders" class="text-center py-4">
            <div class="spinner-border spinner-border-sm text-success"></div>
          </div>
          <div v-else-if="recentOrders.length === 0" class="text-center py-4 text-muted small">
            No orders yet.
          </div>
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0 small">
              <thead class="table-light">
                <tr>
                  <th>Order #</th>
                  <th>Consumer</th>
                  <th>Produce</th>
                  <th>Godown</th>
                  <th>Qty</th>
                  <th>Total</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in recentOrders" :key="order.id">
                  <td class="font-monospace">{{ order.id.substring(0,8) }}</td>
                  <td>{{ order.consumer_name }}</td>
                  <td>{{ order.listing_detail?.category_name }}</td>
                  <td>{{ order.godown_name }}</td>
                  <td>{{ order.quantity_kg }}kg</td>
                  <td class="fw-semibold">{{ order.total_amount | currency }}</td>
                  <td><span :class="statusClass(order.status)">{{ order.status }}</span></td>
                  <td>{{ order.ordered_at | date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Recent Users Table -->
      <div class="card border-0 shadow-sm rounded-3">
        <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center pt-3">
          <h5 class="fw-bold mb-0">Recently Registered Users</h5>
          <nuxt-link to="/admin/users" class="btn btn-outline-success btn-sm">View All</nuxt-link>
        </div>
        <div class="card-body p-0">
          <div v-if="loadingUsers" class="text-center py-4">
            <div class="spinner-border spinner-border-sm text-success"></div>
          </div>
          <div v-else-if="recentUsers.length === 0" class="text-center py-4 text-muted small">
            No users yet.
          </div>
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0 small">
              <thead class="table-light">
                <tr>
                  <th>Name</th>
                  <th>Phone</th>
                  <th>Role</th>
                  <th>Verified</th>
                  <th>Joined</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="u in recentUsers" :key="u.id">
                  <td class="fw-semibold">{{ u.first_name }} {{ u.last_name }}</td>
                  <td>{{ u.phone }}</td>
                  <td>
                    <span :class="roleBadgeClass(u.role)" class="badge">{{ u.role }}</span>
                  </td>
                  <td>
                    <span v-if="u.is_verified" class="text-success"><i class="fas fa-check-circle"></i> Yes</span>
                    <span v-else class="text-warning"><i class="fas fa-clock"></i> Pending</span>
                  </td>
                  <td>{{ u.created_at | date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  layout: 'master',
  auth: false,

  async asyncData({ $axios, store }) {
    try {
      const [statsRes, ordersRes, usersRes] = await Promise.all([
        $axios.$get('/admin/stats/'),
        $axios.$get('/admin/orders/?page_size=8'),
        $axios.$get('/admin/users/?page_size=8'),
      ])
      return {
        stats:        statsRes,
        recentOrders: ordersRes.results || ordersRes,
        recentUsers:  usersRes.results  || usersRes,
      }
    } catch (e) {
      return { stats: {}, recentOrders: [], recentUsers: [] }
    }
  },

  data() {
    return {
      stats:        {},
      recentOrders: [],
      recentUsers:  [],
      loadingOrders: false,
      loadingUsers:  false,
      quickNav: [
        { to: '/admin/users',      icon: '👥', label: 'Users',      desc: 'Manage all accounts' },
        { to: '/admin/godowns',    icon: '🏚️', label: 'Godowns',    desc: 'All warehouses' },
        { to: '/admin/orders',     icon: '🛒', label: 'Orders',     desc: 'All platform orders' },
        { to: '/admin/deliveries', icon: '🌱', label: 'Deliveries', desc: 'Farmer deliveries' },
        { to: '/admin/listings',   icon: '📦', label: 'Listings',   desc: 'Stock listings' },
        { to: '/admin/transport',  icon: '🚚', label: 'Transport',  desc: 'Delivery jobs' },
        { to: '/admin/categories', icon: '🗂️', label: 'Categories', desc: 'Produce categories' },
        { to: '/customer_support', icon: '💬', label: 'Support',    desc: 'Help & FAQ' },
      ],
    }
  },

  filters: {
    currency(v) { return v ? `TZS ${Number(v).toLocaleString()}` : '—' },
    date(v) { return v ? new Date(v).toLocaleDateString('en-TZ', { day: 'numeric', month: 'short', year: 'numeric' }) : '—' },
  },

  methods: {
    statusClass(s) {
      const map = {
        pending:    'badge bg-warning text-dark',
        confirmed:  'badge bg-primary',
        ready:      'badge bg-info text-dark',
        in_transit: 'badge bg-secondary',
        completed:  'badge bg-success',
        cancelled:  'badge bg-danger',
      }
      return map[s] || 'badge bg-light text-dark'
    },
    roleBadgeClass(r) {
      const map = {
        farmer:      'bg-success',
        godown:      'bg-warning text-dark',
        transporter: 'bg-info text-dark',
        consumer:    'bg-primary',
        admin:       'bg-danger',
      }
      return map[r] || 'bg-secondary'
    },
  },
}
</script>

<style scoped>
.text-earth-green { color: #2D6A4F; }
.btn-success { background-color: #2D6A4F; border-color: #2D6A4F; }
.btn-success:hover { background-color: #235840; }
.btn-outline-success { color: #2D6A4F; border-color: #2D6A4F; }
.btn-outline-success:hover { background-color: #2D6A4F; color: #fff; }
.card-hover { transition: transform 0.15s, box-shadow 0.15s; cursor: pointer; }
.card-hover:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.1) !important; }
</style>