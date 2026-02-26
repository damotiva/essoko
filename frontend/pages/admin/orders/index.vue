<template>
  <div class="bg-light min-vh-100 py-4">
    <div class="container px-4">

      <div class="mb-4">
        <nuxt-link to="/admin/dashboard" class="text-muted small text-decoration-none">← Admin Dashboard</nuxt-link>
        <h2 class="fw-bold text-earth-green mb-0 mt-1">All Orders</h2>
      </div>

      <!-- Filters -->
      <div class="card border-0 shadow-sm rounded-3 mb-4">
        <div class="card-body py-3">
          <div class="row g-2">
            <div class="col-md-4">
              <input v-model="filters.search" type="text" class="form-control form-control-sm"
                placeholder="Search by consumer or produce…" @input="debouncedFetch" />
            </div>
            <div class="col-md-3">
              <select v-model="filters.status" class="form-select form-select-sm"
               @change="fetchOrders" >
                <option value="">All Statuses</option>
                <option value="pending">Pending</option>
                <option value="confirmed">Confirmed</option>
                <option value="ready">Ready</option>
                <option value="in_transit">In Transit</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div class="col-md-2">
              <button class="btn btn-outline-secondary btn-sm w-100" 
              @click="clearFilters" >Clear</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Table -->
      <div class="card border-0 shadow-sm rounded-3">
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-success"></div>
          </div>
          <div v-else-if="orders.length === 0" class="text-center py-5 text-muted">No orders found.</div>
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0 small align-middle">
              <thead class="table-light">
                <tr>
                  <th>Order #</th>
                  <th>Consumer</th>
                  <th>Produce</th>
                  <th>Godown</th>
                  <th>Qty</th>
                  <th>Total</th>
                  <th>Pickup</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="o in orders" :key="o.id" >
                  <td class="font-monospace">{{ o.id.substring(0,8) }}</td>
                  <td>
                    <div class="fw-semibold">{{ o.consumer_name }}</div>
                    <div class="text-muted" style="font-size:0.75rem">{{ o.consumer_phone }}</div>
                  </td>
                  <td>{{ o.listing_detail?.category_name }}</td>
                  <td>{{ o.godown_name }}</td>
                  <td>{{ o.quantity_kg }}kg</td>
                  <td class="fw-semibold text-earth-green">{{ o.total_amount | currency }}</td>
                  <td>
                    <span class="badge bg-light text-dark border">
                      {{ o.pickup_method === 'self_pickup' ? '🚶 Self' : '🚚 Delivery' }}
                    </span>
                  </td>
                  <td><span :class="statusClass(o.status)" class="badge">{{ o.status }}</span></td>
                  <td>{{ o.ordered_at | date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="d-flex justify-content-center gap-3 mt-3">
        <button class="btn btn-outline-secondary btn-sm" 
        :disabled="page === 1" @click="changePage(page - 1)" >← Prev</button>
        <span class="text-muted small">Page {{ page }} of {{ totalPages }}</span>
        <button class="btn btn-outline-secondary btn-sm" 
        :disabled="page === totalPages" @click="changePage(page + 1)" >Next →</button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminOrders',
  layout: 'master',
  auth: false,

  async asyncData({ $axios }) {
    try {
      const res = await $axios.$get('/api/admin/orders/')
      return { orders: res.results || res, totalCount: res.count || 0 }
    } catch (e) { return { orders: [], totalCount: 0 } }
  },

  data() {
    return {
      orders: [], totalCount: 0,
      filters: { search: '', status: '' },
      page: 1, pageSize: 20, loading: false, debounceTimer: null,
    }
  },

  computed: {
    totalPages() { return Math.ceil(this.totalCount / this.pageSize) },
  },

  filters: {
    currency(v) { return v ? `TZS ${Number(v).toLocaleString()}` : '—' },
    date(v) { return v ? new Date(v).toLocaleDateString('en-TZ', { day: 'numeric', month: 'short', year: 'numeric' }) : '—' },
  },

  methods: {
    async fetchOrders() {
      this.loading = true
      try {
        const params = { page: this.page }
        if (this.filters.status) params.status = this.filters.status
        if (this.filters.search) params.search = this.filters.search
        const res = await this.$axios.$get('/api/admin/orders/', { params })
        this.orders = res.results || res
        this.totalCount = res.count || this.orders.length
      } finally { this.loading = false }
    },
    debouncedFetch() {
      clearTimeout(this.debounceTimer)
      this.debounceTimer = setTimeout(this.fetchOrders, 400)
    },
    clearFilters() { this.filters = { search: '', status: '' }; this.page = 1; this.fetchOrders() },
    changePage(p) { this.page = p; this.fetchOrders() },
    statusClass(s) {
      return {
        pending: 'bg-warning text-dark', confirmed: 'bg-primary',
        ready: 'bg-info text-dark', in_transit: 'bg-secondary',
        completed: 'bg-success', cancelled: 'bg-danger',
      }[s] || 'bg-light text-dark'
    },
  },
}
</script>

<style scoped>
.text-earth-green { color: #2D6A4F; }
</style>