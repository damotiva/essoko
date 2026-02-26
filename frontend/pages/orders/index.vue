<!-- pages/orders/index.vue — Consumer: my orders -->
<template>
  <div class="page-orders">
    <div class="container">
      <div class="page-header">
        <div>
          <h1 class="page-title">My Orders</h1>
          <p class="page-sub">Track your produce orders</p>
        </div>
        <nuxt-link to="/" class="btn btn-outline">+ New Order</nuxt-link>
      </div>

      <!-- STATS -->
      <div v-if="stats" class="stats-row">
        <div class="mini-stat"><span>{{ stats.total_orders }}</span><small>Total Orders</small></div>
        <div class="mini-stat"><span>{{ stats.pending_orders }}</span><small>In Progress</small></div>
        <div class="mini-stat"><span>{{ stats.completed_orders }}</span><small>Completed</small></div>
        <div class="mini-stat orange"><span>{{ stats.total_spent | currency }}</span><small>Total Spent</small></div>
      </div>

      <div v-if="loading" class="loading-state"><span class="spinner"></span></div>
      <div v-else-if="orders.length === 0" class="empty-state">
        <p>No orders yet.</p>
        <nuxt-link to="/" class="btn btn-primary" style="margin-top:1rem">Browse Produce →</nuxt-link>
      </div>
      <div v-else>
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-card-header">
            <div>
              <span class="order-num">Order #{{ order.id.substring(0,8) }}</span>
              <span :class="`status-badge status-${order.status}`" >{{ order.status }}</span>
            </div>
            <span class="order-date">{{ order.ordered_at | date }}</span>
          </div>
          <div class="order-card-body">
            <div class="order-produce">
              <strong>{{ order.listing_detail.category_name }}</strong>
              <span class="text-muted">{{ order.quantity_kg }}kg · Grade {{ order.listing_detail.grade }}</span>
            </div>
            <div class="order-godown">
              <span class="label">📍 Pickup from</span>
              <strong>{{ order.godown_name }}</strong>
              <span class="text-muted">{{ order.godown_address }}</span>
            </div>
            <div class="order-pickup">
              <span class="label">Pickup Method</span>
              <span>{{ order.pickup_method === 'self_pickup' ? '🚶 Self Pickup' : '🚚 Transporter' }}</span>
            </div>
          </div>
          <div class="order-card-footer">
            <span class="order-total">{{ order.total_amount | currency }}</span>
            <button v-if="order.status === 'pending'" class="action-btn cancel" 
            @click="cancelOrder(order.id)" >
              Cancel
            </button>
            <nuxt-link :to="`/orders/${order.id}`" class="action-btn view">View Details →</nuxt-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MyOrdersPage',
  middleware: ['auth', 'role-consumer'],

  async asyncData({ $axios }) {
    const [ordersRes, statsRes] = await Promise.all([
      $axios.$get('/api/orders/mine/'),
      $axios.$get('/api/dashboard/stats/'),
    ])
    return {
      orders: ordersRes.results || ordersRes,
      stats: statsRes,
    }
  },

  data() {
    return { orders: [], stats: null, loading: false }
  },

  filters: {
    currency(v) { return v ? `TZS ${Number(v).toLocaleString()}` : '—' },
    date(v) { return v ? new Date(v).toLocaleDateString('en-TZ', { day: 'numeric', month: 'short', year: 'numeric' }) : '' },
  },

  methods: {
    async cancelOrder(id) {
      if (!confirm('Cancel this order?')) return
      try {
        const updated = await this.$axios.$post(`/api/orders/${id}/cancel/`)
        const idx = this.orders.findIndex(o => o.id === id)
        if (idx !== -1) this.$set(this.orders, idx, updated)
      } catch (e) {
        alert(e.response?.data?.error || 'Cannot cancel this order.')
      }
    },
  },
}
</script>

<style scoped>
.page-orders { padding: 2rem 1.5rem; background: #f7f6f3; min-height: 100vh; }
.container { max-width: 800px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; }
.page-title { font-size: 1.75rem; font-weight: 800; color: #1a2e10; margin-bottom: 0.2rem; }
.page-sub { color: #666; font-size: 0.9rem; }
.btn { padding: 0.6rem 1.25rem; border-radius: 4px; font-weight: 700; font-size: 0.88rem; text-decoration: none; cursor: pointer; border: 2px solid #ccc; background: transparent; color: #333; }
.btn-primary { background: #c8842a; color: #fff; border-color: #c8842a; }

.stats-row { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
.mini-stat { flex: 1; min-width: 100px; background: #fff; border-radius: 8px; padding: 1rem; text-align: center; border: 1px solid #e5e5e5; }
.mini-stat span { display: block; font-size: 1.6rem; font-weight: 800; color: #1a2e10; }
.mini-stat.orange span { color: #c8842a; }
.mini-stat small { font-size: 0.72rem; color: #888; text-transform: uppercase; letter-spacing: 0.08em; }

.order-card { background: #fff; border: 1px solid #e5e5e5; border-radius: 8px; overflow: hidden; margin-bottom: 1rem; }
.order-card-header { display: flex; justify-content: space-between; align-items: center; padding: 0.9rem 1.25rem; background: #fafaf8; border-bottom: 1px solid #eee; flex-wrap: wrap; gap: 0.5rem; }
.order-num { font-weight: 700; font-size: 0.9rem; color: #1a2e10; margin-right: 0.5rem; font-family: monospace; }
.order-date { font-size: 0.8rem; color: #888; }
.order-card-body { padding: 1rem 1.25rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; }
.order-produce strong { display: block; font-size: 1rem; color: #1a2e10; margin-bottom: 0.15rem; }
.order-godown strong { display: block; }
.label { display: block; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; color: #888; margin-bottom: 0.2rem; }
.text-muted { color: #888; font-size: 0.82rem; display: block; }
.order-card-footer { display: flex; align-items: center; justify-content: space-between; padding: 0.9rem 1.25rem; border-top: 1px solid #eee; gap: 0.5rem; flex-wrap: wrap; }
.order-total { font-size: 1.1rem; font-weight: 800; color: #c8842a; }
.action-btn { padding: 0.35rem 0.75rem; border-radius: 3px; font-size: 0.8rem; font-weight: 600; cursor: pointer; border: 1px solid #ccc; background: #fff; text-decoration: none; display: inline-block; }
.action-btn.cancel { background: #fee2e2; color: #991b1b; border-color: #fca5a5; }
.action-btn.view { background: #f3f4f6; color: #333; }
.status-badge { display: inline-block; padding: 0.18rem 0.5rem; border-radius: 3px; font-size: 0.7rem; font-weight: 700; text-transform: capitalize; }
.status-pending { background: #fef9c3; color: #854d0e; }
.status-confirmed { background: #dbeafe; color: #1e40af; }
.status-ready { background: #dcfce7; color: #166534; }
.status-in_transit { background: #ede9fe; color: #5b21b6; }
.status-completed { background: #d1fae5; color: #065f46; }
.status-cancelled { background: #fee2e2; color: #991b1b; }
.loading-state { text-align: center; padding: 3rem; }
.empty-state { text-align: center; padding: 3rem; background: #fff; border-radius: 8px; }
</style>