<template>
  <div class="bg-light min-vh-100 py-4">
    <div class="container px-4">

      <div class="mb-4">
        <nuxt-link to="/admin/dashboard" class="text-muted small text-decoration-none">← Admin Dashboard</nuxt-link>
        <h2 class="fw-bold text-earth-green mb-0 mt-1">Produce Categories</h2>
      </div>

      <div class="row g-4">

        <!-- Add Category Form -->
        <div class="col-md-4">
          <div class="card border-0 shadow-sm rounded-3">
            <div class="card-body p-4">
              <h5 class="fw-bold mb-4">
                {{ editing ? 'Edit Category' : 'Add New Category' }}
              </h5>

              <div v-if="formSuccess" class="alert alert-success py-2 small">✅ Saved successfully.</div>
              <div v-if="formError" class="alert alert-danger py-2 small">{{ formError }}</div>

              <div class="mb-3">
                <label class="form-label fw-semibold small">Category Name</label>
                <input v-model="form.name" type="text" class="form-control" placeholder="e.g. Maize, Tomato, Rice" />
              </div>

              <div class="mb-4">
                <label class="form-label fw-semibold small">Unit of Measure</label>
                <select v-model="form.unit" class="form-select">
                  <option value="kg">kg</option>
                  <option value="tonnes">tonnes</option>
                  <option value="bags">bags</option>
                  <option value="litres">litres</option>
                  <option value="pieces">pieces</option>
                </select>
              </div>

              <div class="d-flex gap-2">
                <button class="btn btn-success flex-fill" :disabled="saving" @click="saveCategory">
                  <span v-if="saving"><span class="spinner-border spinner-border-sm me-1"></span>Saving…</span>
                  <span v-else>{{ editing ? 'Update' : 'Add Category' }}</span>
                </button>
                <button v-if="editing" class="btn btn-outline-secondary" @click="cancelEdit">Cancel</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Categories List -->
        <div class="col-md-8">
          <div class="card border-0 shadow-sm rounded-3">
            <div class="card-body p-0">
              <div v-if="loading" class="text-center py-5"><div class="spinner-border text-success"></div></div>
              <div v-else-if="categories.length === 0" class="text-center py-5 text-muted">
                No categories yet. Add your first one.
              </div>
              <div v-else class="table-responsive">
                <table class="table table-hover mb-0 small align-middle">
                  <thead class="table-light">
                    <tr>
                      <th>#</th>
                      <th>Category Name</th>
                      <th>Unit</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(cat, idx) in categories" :key="cat.id">
                      <td class="text-muted">{{ idx + 1 }}</td>
                      <td class="fw-semibold">{{ cat.name }}</td>
                      <td><span class="badge bg-light text-dark border">{{ cat.unit }}</span></td>
                      <td>
                        <button class="btn btn-outline-success btn-sm me-1" @click="editCategory(cat)">
                          <i class="fas fa-pencil-alt"></i> Edit
                        </button>
                        <button class="btn btn-outline-danger btn-sm" @click="deleteCategory(cat)">
                          <i class="fas fa-trash"></i> Delete
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
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminCategories',
  layout: 'master',
  auth: false,

  async asyncData({ $axios }) {
    try {
      const res = await $axios.$get('/categories/')
      return { categories: res.results || res }
    } catch (e) { return { categories: [] } }
  },

  data() {
    return {
      categories: [],
      form: { name: '', unit: 'kg' },
      editing: null,   // holds the category being edited
      loading: false,
      saving: false,
      formSuccess: false,
      formError: null,
    }
  },

  methods: {
    async saveCategory() {
      this.formError = null
      this.formSuccess = false
      if (!this.form.name) return (this.formError = 'Category name is required.')
      this.saving = true
      try {
        if (this.editing) {
          // Update existing
          const updated = await this.$axios.$put(`/admin/categories/${this.editing.id}/`, this.form)
          const idx = this.categories.findIndex(c => c.id === this.editing.id)
          if (idx !== -1) this.$set(this.categories, idx, updated)
          this.editing = null
        } else {
          // Create new
          const created = await this.$axios.$post('/admin/categories/', this.form)
          this.categories.push(created)
        }
        this.form = { name: '', unit: 'kg' }
        this.formSuccess = true
        setTimeout(() => (this.formSuccess = false), 3000)
      } catch (e) {
        this.formError = 'Failed to save. Please try again.'
      } finally {
        this.saving = false
      }
    },

    editCategory(cat) {
      this.editing = cat
      this.form = { name: cat.name, unit: cat.unit }
      this.formError = null
      this.formSuccess = false
    },

    cancelEdit() {
      this.editing = null
      this.form = { name: '', unit: 'kg' }
    },

    async deleteCategory(cat) {
      if (!confirm(`Delete category "${cat.name}"? This will affect all linked listings.`)) return
      try {
        await this.$axios.$delete(`/admin/categories/${cat.id}/`)
        this.categories = this.categories.filter(c => c.id !== cat.id)
      } catch (e) { alert('Failed to delete category.') }
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
</style>