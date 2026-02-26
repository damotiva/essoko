<template>
  <div class="bg-light min-vh-100 py-4">
    <div class="container px-4">

      <div class="mb-4">
        <nuxt-link to="/admin/dashboard" class="text-muted small text-decoration-none">← Admin Dashboard</nuxt-link>
        <h2 class="fw-bold text-earth-green mb-0 mt-1">All Transport Jobs</h2>
      </div>

      <!-- Filter -->
      <div class="card border-0 shadow-sm rounded-3 mb-4">
        <div class="card-body py-3">
          <div class="row g-2">
            <div class="col-md-3">
              <select v-model="filters.status" class="form-select form-select-sm" @change="fetchJobs" >
                <option value="">All Statuses</option>
                <option value="open">Open</option>
                <option value="assigned">Assigned</option>
                <option value="picked_up">Picked Up</option>
                <option value="delivered">Delivered</option>
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

      <div class="card border-0 shadow-sm rounded-3">
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5"><div class="spinner-border text-success"></div></div>
          <div v-else-if="jobs.length === 0" class="text-center py-5 text-muted">No transport jobs found.</div>
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0 small align-middle">
              <thead class="table-light">
                <tr>
                  <th>Job ID</th><th>Order #</th><th>Transporter</th>
                  <th>Pickup</th><th>Delivery</th><th>Fee</th>
                  <th>Status</th><th>Created</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="j in jobs" :key="j.id" >
                  <td class="font-monospace">{{ j.id.substring(0,8) }}</td>
                  <td class="font-monospace text-muted">{{ j.order.substring(0,8) }}</td>
                  <td>{{ j.transporter_name || <span class="text-muted">Unassigned</span> }}</td>
                  <td>{{ j.pickup_location }}</td>
                  <td>{{ j.delivery_location }}</td>
                  <td>{{ j.transport_fee | currency }}</td>
                  <td>
                    <span :class="{
                      'badge bg-secondary': j.status === 'open',
                      'badge bg-primary':   j.status === 'assigned',
                      'badge bg-info text-dark': j.status === 'picked_up',
                      'badge bg-success':   j.status === 'delivered',
                      'badge bg-danger':    j.status === 'cancelled',
                    }" >{{ j.status }}</span>
                  </td>
                  <td>{{ j.created_at | date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

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
  name: 'AdminTransport',
  layout: 'master',
  auth: false,
  async asyncData({ $axios }) {
    try {
      const res = await $axios.$get('/admin/transport/')
      return { jobs: res.results || res, totalCount: res.count || 0 }
    } catch (e) { return { jobs: [], totalCount: 0 } }
  },
  data() {
    return { jobs: [], totalCount: 0, filters: { status: '' }, page: 1, pageSize: 20, loading: false }
  },
  computed: { totalPages() { return Math.ceil(this.totalCount / this.pageSize) } },
  filters: {
    currency(v) { return v ? `TZS ${Number(v).toLocaleString()}` : '—' },
    date(v) { return v ? new Date(v).toLocaleDateString('en-TZ', { day: 'numeric', month: 'short', year: 'numeric' }) : '—' },
  },
  methods: {
    async fetchJobs() {
      this.loading = true
      try {
        const params = { page: this.page }
        if (this.filters.status) params.status = this.filters.status
        const res = await this.$axios.$get('/admin/transport/', { params })
        this.jobs = res.results || res
        this.totalCount = res.count || this.jobs.length
      } finally { this.loading = false }
    },
    clearFilters() { this.filters = { status: '' }; this.page = 1; this.fetchJobs() },
    changePage(p) { this.page = p; this.fetchJobs() },
  },
}
</script>
<style scoped>
.text-earth-green { color: #2D6A4F; }
</style>