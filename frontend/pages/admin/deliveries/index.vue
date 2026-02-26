<template>
  <div class="bg-light min-vh-100 py-4">
    <div class="container px-4">

      <div class="mb-4">
        <nuxt-link to="/admin/dashboard" class="text-muted small text-decoration-none">← Admin Dashboard</nuxt-link>
        <h2 class="fw-bold text-earth-green mb-0 mt-1">All Farmer Deliveries</h2>
      </div>

      <!-- Filter -->
      <div class="card border-0 shadow-sm rounded-3 mb-4">
        <div class="card-body py-3">
          <div class="row g-2">
            <div class="col-md-3">
              <select v-model="filters.status" class="form-select form-select-sm" @change="fetchDeliveries">
                <option value="">All Statuses</option>
                <option value="pending">Pending</option>
                <option value="accepted">Accepted</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
            <div class="col-md-2">
              <button class="btn btn-outline-secondary btn-sm w-100" @click="clearFilters">Clear</button>
            </div>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-3">
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5"><div class="spinner-border text-success"></div></div>
          <div v-else-if="deliveries.length === 0" class="text-center py-5 text-muted">No deliveries found.</div>
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0 small align-middle">
              <thead class="table-light">
                <tr>
                  <th>Farmer</th><th>Godown</th><th>Produce</th>
                  <th>Qty (kg)</th><th>Price/kg</th><th>Total</th>
                  <th>Grade</th><th>Status</th><th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="d in deliveries" :key="d.id">
                  <td class="fw-semibold">{{ d.farmer_name }}</td>
                  <td>{{ d.godown_name }}</td>
                  <td>{{ d.category_name }}</td>
                  <td>{{ d.quantity_kg }}</td>
                  <td>{{ d.price_per_kg_paid | currency }}</td>
                  <td class="fw-semibold text-earth-green">{{ d.total_amount | currency }}</td>
                  <td><span class="badge bg-success-subtle text-success border">{{ d.grade }}</span></td>
                  <td>
                    <span :class="{
                      'badge bg-warning text-dark': d.status === 'pending',
                      'badge bg-success': d.status === 'accepted',
                      'badge bg-danger': d.status === 'rejected',
                    }">{{ d.status }}</span>
                  </td>
                  <td>{{ d.delivered_at | date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div v-if="totalPages > 1" class="d-flex justify-content-center gap-3 mt-3">
        <button class="btn btn-outline-secondary btn-sm" :disabled="page === 1" @click="changePage(page - 1)">← Prev</button>
        <span class="text-muted small">Page {{ page }} of {{ totalPages }}</span>
        <button class="btn btn-outline-secondary btn-sm" :disabled="page === totalPages" @click="changePage(page + 1)">Next →</button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminDeliveries',
  layout: 'master',
  auth: false,
  async asyncData({ $axios }) {
    try {
      const res = await $axios.$get('/api/admin/deliveries/')
      return { deliveries: res.results || res, totalCount: res.count || 0 }
    } catch (e) { return { deliveries: [], totalCount: 0 } }
  },
  data() {
    return { deliveries: [], totalCount: 0, filters: { status: '' }, page: 1, pageSize: 20, loading: false }
  },
  computed: { totalPages() { return Math.ceil(this.totalCount / this.pageSize) } },
  filters: {
    currency(v) { return v ? `TZS ${Number(v).toLocaleString()}` : '—' },
    date(v) { return v ? new Date(v).toLocaleDateString('en-TZ', { day: 'numeric', month: 'short', year: 'numeric' }) : '—' },
  },
  methods: {
    async fetchDeliveries() {
      this.loading = true
      try {
        const params = { page: this.page }
        if (this.filters.status) params.status = this.filters.status
        const res = await this.$axios.$get('/api/admin/deliveries/', { params })
        this.deliveries = res.results || res
        this.totalCount = res.count || this.deliveries.length
      } finally { this.loading = false }
    },
    clearFilters() { this.filters = { status: '' }; this.page = 1; this.fetchDeliveries() },
    changePage(p) { this.page = p; this.fetchDeliveries() },
  },
}
</script>
<style scoped>
.text-earth-green { color: #2D6A4F; }
</style>