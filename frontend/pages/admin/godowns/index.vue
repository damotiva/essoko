<!-- ═══════════════════════════════════════════════════════════════
     pages/admin/godowns.vue
═══════════════════════════════════════════════════════════════ -->
<template>
  <div class="bg-light min-vh-100 py-4">
    <div class="container px-4">

      <div class="mb-4">
        <nuxt-link to="/admin/dashboard" class="text-muted small text-decoration-none">← Admin Dashboard</nuxt-link>
        <h2 class="fw-bold text-earth-green mb-0 mt-1">All Godowns</h2>
      </div>

      <div class="card border-0 shadow-sm rounded-3">
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-5"><div class="spinner-border text-success"></div></div>
          <div v-else-if="godowns.length === 0" class="text-center py-5 text-muted">No godowns registered.</div>
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0 small align-middle">
              <thead class="table-light">
                <tr>
                  <th>Name</th><th>Operator</th><th>Location</th>
                  <th>Capacity (tons)</th><th>Phone</th><th>Active</th><th>Registered</th><th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="g in godowns" :key="g.id" >
                  <td class="fw-semibold">{{ g.name }}</td>
                  <td>{{ g.operator_name }}</td>
                  <td>{{ g.location }}</td>
                  <td>{{ g.capacity_tons }}</td>
                  <td>{{ g.phone }}</td>
                  <td>
                    <span v-if="g.is_active" class="badge bg-success">Active</span>
                    <span v-else class="badge bg-danger">Inactive</span>
                  </td>
                  <td>{{ g.created_at | date }}</td>
                  <td>
                    <button class="btn btn-outline-danger btn-sm" @click="toggleActive(g)" >
                      {{ g.is_active ? 'Deactivate' : 'Activate' }}
                    </button>
                  </td>
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
  name: 'AdminGodowns',
  layout: 'master',
  auth: false,
  async asyncData({ $axios }) {
    try {
      const res = await $axios.$get('/api/admin/godowns/')
      return { godowns: res.results || res }
    } catch (e) { return { godowns: [] } }
  },
  data() { return { godowns: [], loading: false } },
  filters: {
    date(v) { return v ? new Date(v).toLocaleDateString('en-TZ', { day: 'numeric', month: 'short', year: 'numeric' }) : '—' },
  },
  methods: {
    async toggleActive(g) {
      try {
        await this.$axios.$patch(`/api/admin/godowns/${g.id}/`, { is_active: !g.is_active })
        const idx = this.godowns.findIndex(x => x.id === g.id)
        if (idx !== -1) this.$set(this.godowns[idx], 'is_active', !g.is_active)
      } catch (e) { alert('Failed to update godown.') }
    },
  },
}
</script>

<style scoped>
.text-earth-green { color: #2D6A4F; }
</style>