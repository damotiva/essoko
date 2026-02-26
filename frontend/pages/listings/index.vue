<template>
  <div class="bg-light min-vh-100 py-4">
    <div class="container">

      <!-- Page Header -->
      <div class="mb-4">
        <h2 class="display-6 fw-bold text-earth-green">Available Products</h2>
        <p class="text-muted">Fresh produce from verified godowns — ready to order.</p>
      </div>

      <!-- Filters Row -->
      <div class="card shadow-sm border-0 rounded-3 mb-4">
        <div class="card-body py-3">
          <div class="row g-2 align-items-end">
            <div class="col-md-4">
              <label class="form-label small fw-semibold mb-1">Search</label>
              <input
                v-model="filters.search"
                type="text"
                class="form-control form-control-sm"
                placeholder="Search produce…"
                @input="debouncedFetch"
              />
            </div>
            <div class="col-md-3">
              <label class="form-label small fw-semibold mb-1">Category</label>
              <select v-model="filters.category" class="form-select form-select-sm" @change="fetchListings" >
                <option value="">All Categories</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id" >{{ cat.name }}</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label small fw-semibold mb-1">Godown</label>
              <select v-model="filters.godown" class="form-select form-select-sm" @change="fetchListings" >
                <option value="">All Godowns</option>
                <option v-for="g in godowns" :key="g.id" :value="g.id" >{{ g.name }}</option>
              </select>
            </div>
            <div class="col-md-2">
              <button class="btn btn-outline-secondary btn-sm w-100" @click="clearFilters" >Clear</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="text-muted mt-2">Loading stock…</p>
      </div>

      <!-- Empty -->
      <div v-else-if="listings.length === 0" class="text-center py-5">
        <p class="text-muted fs-5">No produce available right now. Check back soon.</p>
      </div>

      <!-- Products Grid -->
      <div v-else class="row">
        <div class="col-md-4 col-lg-3 mb-4" v-for="item in listings" :key="item.id" >
          <div class="card h-100 shadow-sm border-0 rounded-3">
            <!-- Image -->
            <div style="height:180px; overflow:hidden; background:#f0ece0;" class="rounded-top-3">
              <img
                v-if="item.image_url"
                :src="item.image_url"
                :alt="item.category_name"
                class="w-100 h-100"
                style="object-fit:cover"
              />
              <div v-else class="h-100 d-flex align-items-center justify-content-center fs-1">🌾</div>
            </div>

            <div class="card-body">
              <!-- Status Badge -->
              <span :class="statusBadgeClass(item.status)" class="badge mb-2">
                {{ statusLabel(item.status) }}
              </span>

              <h5 class="card-title fw-bold mb-1">{{ item.category_name }}</h5>
              <p class="text-muted small mb-1">
                <i class="fas fa-map-marker-alt"></i>
                {{ item.godown_name }}, {{ item.godown_location }}
              </p>
              <p class="text-muted small mb-2">Grade: <strong>{{ item.grade }}</strong></p>

              <div class="d-flex justify-content-between align-items-center mt-auto">
                <span class="fw-bold text-earth-green fs-5">
                  TZS {{ Number(item.price_per_kg).toLocaleString() }}<small class="text-muted fw-normal">/kg</small>
                </span>
                <small class="text-muted">{{ item.quantity_available_kg }}kg left</small>
              </div>
            </div>

            <div class="card-footer bg-white border-0 pt-0 pb-3 px-3">
              <nuxt-link :to="`/listings/${item.id}`" class="btn btn-success w-100 btn-sm">
                View & Order →
              </nuxt-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="d-flex justify-content-center align-items-center gap-3 mt-2 pb-4">
        <button class="btn btn-outline-secondary btn-sm" 
        :disabled="page === 1" @click="changePage(page - 1)" >
          ← Prev
        </button>
        <span class="text-muted small">Page {{ page }} of {{ totalPages }}</span>
        <button class="btn btn-outline-secondary btn-sm" 
        :disabled="page === totalPages" @click="changePage(page + 1)" >
          Next →
        </button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'ListingsPage',
  layout: 'master',
  auth: false,

  async asyncData({ $axios }) {
    try {
      const [categoriesRes, godownsRes, listingsRes] = await Promise.all([
        $axios.$get('/api/categories/'),
        $axios.$get('/api/godowns/'),
        $axios.$get('/api/listings/'),
      ])
      return {
        categories:  categoriesRes.results  || categoriesRes,
        godowns:     godownsRes.results     || godownsRes,
        listings:    listingsRes.results    || listingsRes,
        totalCount:  listingsRes.count      || 0,
      }
    } catch (e) {
      return { categories: [], godowns: [], listings: [], totalCount: 0 }
    }
  },

  data() {
    return {
      categories: [],
      godowns:    [],
      listings:   [],
      totalCount: 0,
      filters: { search: '', category: '', godown: '' },
      page:     1,
      pageSize: 20,
      loading:  false,
      debounceTimer: null,
    }
  },

  computed: {
    totalPages() {
      return Math.ceil(this.totalCount / this.pageSize)
    },
  },

  methods: {
    async fetchListings() {
      this.loading = true
      try {
        const params = { page: this.page }
        if (this.filters.category) params.category = this.filters.category
        if (this.filters.godown)   params.godown   = this.filters.godown
        if (this.filters.search)   params.search   = this.filters.search
        const res = await this.$axios.$get('/api/listings/', { params })
        this.listings   = res.results || res
        this.totalCount = res.count   || this.listings.length
      } finally {
        this.loading = false
      }
    },

    debouncedFetch() {
      clearTimeout(this.debounceTimer)
      this.debounceTimer = setTimeout(this.fetchListings, 400)
    },

    clearFilters() {
      this.filters = { search: '', category: '', godown: '' }
      this.page = 1
      this.fetchListings()
    },

    changePage(p) {
      this.page = p
      this.fetchListings()
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    statusLabel(s) {
      return { available: '✅ Available', low_stock: '⚠️ Low Stock', out_of_stock: '❌ Out of Stock' }[s] || s
    },

    statusBadgeClass(s) {
      return {
        available:    'bg-success-subtle text-success',
        low_stock:    'bg-warning-subtle text-warning',
        out_of_stock: 'bg-danger-subtle text-danger',
      }[s] || 'bg-secondary-subtle text-secondary'
    },
  },
}
</script>

<style scoped>
.text-earth-green { color: #2D6A4F; }
.btn-success { background-color: #2D6A4F; border-color: #2D6A4F; }
.btn-success:hover { background-color: #235840; border-color: #235840; }
</style>