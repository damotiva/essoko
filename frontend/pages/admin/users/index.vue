<template>
  <div class="bg-light min-vh-100 py-4">
    <div class="container px-4">

      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <nuxt-link to="/admin/dashboard" class="text-muted small text-decoration-none">
            ← Admin Dashboard
          </nuxt-link>
          <h2 class="fw-bold text-earth-green mb-0 mt-1">All Users</h2>
        </div>
      </div>

      <!-- Filters -->
      <div class="card border-0 shadow-sm rounded-3 mb-4">
        <div class="card-body py-3">
          <div class="row g-2 align-items-end">
            <div class="col-md-4">
              <input
                v-model="filters.search"
                type="text"
                class="form-control form-control-sm"
                placeholder="Search by name or phone…"
                @input="debouncedFetch"
              />
            </div>
            <div class="col-md-3">
              <select v-model="filters.role" class="form-select form-select-sm" @change="fetchUsers" >
                <option value="">All Roles</option>
                <option value="farmer">Farmer</option>
                <option value="godown">Godown</option>
                <option value="transporter">Transporter</option>
                <option value="consumer">Consumer</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div class="col-md-2">
              <select v-model="filters.verified" class="form-select form-select-sm" @change="fetchUsers" >
                <option value="">All Status</option>
                <option value="true">Verified</option>
                <option value="false">Unverified</option>
              </select>
            </div>
            <div class="col-md-2">
              <button class="btn btn-outline-secondary btn-sm w-100" @click="clearFilters" >Clear</button>
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
          <div v-else-if="users.length === 0" class="text-center py-5 text-muted">
            No users found.
          </div>
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0 small align-middle">
              <thead class="table-light">
                <tr>
                  <th>Name</th>
                  <th>Phone</th>
                  <th>Username</th>
                  <th>Role</th>
                  <th>Address</th>
                  <th>Verified</th>
                  <th>Joined</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="u in users" :key="u.id" >
                  <td class="fw-semibold">{{ u.first_name }} {{ u.last_name }}</td>
                  <td>{{ u.phone }}</td>
                  <td class="text-muted">{{ u.username }}</td>
                  <td>
                    <span :class="['badge', roleBadgeClass(u.role)]" >{{ u.role }}</span>
                  </td>
                  <td class="text-muted">{{ u.address || '—' }}</td>
                  <td>
                    <span v-if="u.is_verified" class="badge bg-success">✓ Verified</span>
                    <span v-else class="badge bg-warning text-dark">Pending</span>
                  </td>
                  <td>{{ u.created_at | date }}</td>
                  <td>
                    <button
                      v-if="!u.is_verified"
                      class="btn btn-success btn-sm me-1"
                      @click="verifyUser(u)"
                    >Verify</button>
                    <button
                      class="btn btn-outline-danger btn-sm"
                      @click="confirmDelete(u)"
                    >Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="d-flex justify-content-center align-items-center gap-3 mt-3">
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
  name: 'AdminUsers',
  layout: 'master',
  auth: false,

  async asyncData({ $axios }) {
    try {
      const res = await $axios.$get('/admin/users/')
      return { users: res.results || res, totalCount: res.count || 0 }
    } catch (e) {
      return { users: [], totalCount: 0 }
    }
  },

  data() {
    return {
      users: [], totalCount: 0,
      filters: { search: '', role: '', verified: '' },
      page: 1, pageSize: 20,
      loading: false,
      debounceTimer: null,
    }
  },

  computed: {
    totalPages() { return Math.ceil(this.totalCount / this.pageSize) },
  },

  filters: {
    date(v) { return v ? new Date(v).toLocaleDateString('en-TZ', { day: 'numeric', month: 'short', year: 'numeric' }) : '—' },
  },

  methods: {
    async fetchUsers() {
      this.loading = true
      try {
        const params = { page: this.page }
        if (this.filters.role)     params.role     = this.filters.role
        if (this.filters.search)   params.search   = this.filters.search
        if (this.filters.verified) params.verified = this.filters.verified
        const res = await this.$axios.$get('/admin/users/', { params })
        this.users      = res.results || res
        this.totalCount = res.count   || this.users.length
      } finally { this.loading = false }
    },

    debouncedFetch() {
      clearTimeout(this.debounceTimer)
      this.debounceTimer = setTimeout(this.fetchUsers, 400)
    },

    clearFilters() {
      this.filters = { search: '', role: '', verified: '' }
      this.page = 1
      this.fetchUsers()
    },

    changePage(p) { this.page = p; this.fetchUsers() },

    async verifyUser(u) {
      try {
        await this.$axios.$post(`/admin/users/${u.id}/verify/`)
        const idx = this.users.findIndex(x => x.id === u.id)
        if (idx !== -1) this.$set(this.users[idx], 'is_verified', true)
      } catch (e) { alert('Failed to verify user.') }
    },

    async confirmDelete(u) {
      if (!confirm(`Delete user ${u.first_name} ${u.last_name}? This cannot be undone.`)) return
      try {
        await this.$axios.$delete(`/admin/users/${u.id}/`)
        this.users = this.users.filter(x => x.id !== u.id)
      } catch (e) { alert('Failed to delete user.') }
    },

    roleBadgeClass(r) {
      return { farmer: 'bg-success', godown: 'bg-warning text-dark', transporter: 'bg-info text-dark', consumer: 'bg-primary', admin: 'bg-danger' }[r] || 'bg-secondary'
    },
  },
}
</script>

<style scoped>
.text-earth-green { color: #2D6A4F; }
.btn-success { background-color: #2D6A4F; border-color: #2D6A4F; }
</style>