<template>
  <div class="bg-light min-vh-100 py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-7 col-lg-6">

          <!-- Logo / Brand -->
          <div class="text-center mb-4">
            <h1 class="display-6 fw-bold">🌾 ESSOKO</h1>
            <p class="text-muted">Earth · Supply · Soko</p>
          </div>

          <div class="card shadow-sm border-0 rounded-3">
            <div class="card-body p-4">
              <h4 class="card-title text-center mb-1">Create account</h4>
              <p class="text-center text-muted small mb-4">Join the supply chain</p>

              <!-- Alerts -->
              <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>
              <div v-if="success" class="alert alert-success py-2 small">✅ Account created! Redirecting…</div>

              <!-- Role picker -->
              <div class="mb-4">
                <label class="form-label fw-semibold small">I am a…</label>
                <div class="row g-2">
                  <div class="col-6 col-md-3" v-for="r in roles" :key="r.value">
                    <button
                      type="button"
                      :class="['btn w-100 py-3', form.role === r.value ? 'btn-primary' : 'btn-outline-secondary']"
                      @click="form.role = r.value"
                    >
                      <div style="font-size:1.4rem">{{ r.icon }}</div>
                      <div class="small mt-1">{{ r.label }}</div>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Name -->
              <div class="row g-3 mb-3">
                <div class="col-6">
                  <label class="form-label fw-semibold small">First Name</label>
                  <input v-model="form.first_name" type="text" class="form-control" placeholder="John" />
                </div>
                <div class="col-6">
                  <label class="form-label fw-semibold small">Last Name</label>
                  <input v-model="form.last_name" type="text" class="form-control" placeholder="Doe" />
                </div>
              </div>

              <!-- Phone -->
              <div class="mb-3">
                <label class="form-label fw-semibold small">
                  Phone Number <span class="text-muted fw-normal">(used to log in)</span>
                </label>
                <input v-model="form.phone" type="tel" class="form-control" placeholder="+255 xxx xxx xxx" />
              </div>

              <!-- Username -->
              <div class="mb-3">
                <label class="form-label fw-semibold small">Username</label>
                <input v-model="form.username" type="text" class="form-control" placeholder="johndoe" />
              </div>

              <!-- Address -->
              <div class="mb-3">
                <label class="form-label fw-semibold small">Address / Location</label>
                <input v-model="form.address" type="text" class="form-control" placeholder="Dar es Salaam, Tanzania" />
              </div>

              <!-- Passwords -->
              <div class="row g-3 mb-4">
                <div class="col-6">
                  <label class="form-label fw-semibold small">Password</label>
                  <input v-model="form.password" type="password" class="form-control" />
                </div>
                <div class="col-6">
                  <label class="form-label fw-semibold small">Confirm Password</label>
                  <input v-model="form.password2" type="password" class="form-control" />
                </div>
              </div>

              <!-- Submit -->
              <button
                class="btn btn-primary w-100"
                :disabled="loading || !form.role"
                @click="register"
              >
                <span v-if="loading">
                  <span class="spinner-border spinner-border-sm me-2"></span>Creating account…
                </span>
                <span v-else>Create Account</span>
              </button>

              <hr class="my-3" />

              <p class="text-center small text-muted mb-0">
                Already have an account?
                <nuxt-link to="/auth/login" class="text-primary fw-semibold">Log in</nuxt-link>
              </p>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterPage',
  layout: 'master',
  auth: 'guest',

  data() {
    return {
      form: {
        role: '',
        first_name: '', last_name: '',
        phone: '', username: '', address: '',
        password: '', password2: '',
      },
      roles: [
        { value: 'consumer',    label: 'Consumer',    icon: '🍽️' },
        { value: 'farmer',      label: 'Farmer',      icon: '🌱' },
        { value: 'godown',      label: 'Godown',      icon: '🏚️' },
        { value: 'transporter', label: 'Transporter', icon: '🚚' },
      ],
      loading: false,
      error: null,
      success: false,
    }
  },

  methods: {
    async register() {
      this.error = null
      this.loading = true
      try {
        await this.$axios.$post('/auth/register/', this.form)
        this.success = true

        await this.$auth.loginWith('local', {
          data: { username: this.form.phone, password: this.form.password },
        })

        const redirects = {
          farmer:      '/farmer/dashboard',
          godown:      '/godown/dashboard',
          transporter: '/transporter/jobs',
          consumer:    '/',
        }
        this.$router.push(redirects[this.form.role] || '/')
      } catch (e) {
        const data = e.response?.data
        if (data && typeof data === 'object') {
          this.error = Object.values(data).flat().join(' ')
        } else {
          this.error = 'Registration failed. Please try again.'
        }
      } finally {
        this.loading = false
      }
    },
  },
}
</script>