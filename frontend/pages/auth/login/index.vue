<template>
  <div class="bg-light min-vh-100 d-flex align-items-center py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-5 col-lg-4">

          <!-- Logo / Brand -->
          <div class="text-center mb-4">
            <h1 class="display-6 fw-bold">🌾 ESSOKO</h1>
            <p class="text-muted">Earth · Supply · Soko</p>
          </div>

          <div class="card shadow-sm border-0 rounded-3">
            <div class="card-body p-4">
              <h4 class="card-title text-center mb-1">Welcome back</h4>
              <p class="text-center text-muted small mb-4">Log in to your account</p>

              <!-- Error -->
              <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>

              <!-- Phone -->
              <div class="mb-3">
                <label class="form-label fw-semibold small">Phone Number</label>
                <input
                  v-model="form.phone"
                  type="tel"
                  class="form-control"
                  placeholder="+255 xxx xxx xxx"
                />
              </div>

              <!-- Password -->
              <div class="mb-4">
                <label class="form-label fw-semibold small">Password</label>
                <input
                  v-model="form.password"
                  type="password"
                  class="form-control"
                  placeholder="Your password"
                />
              </div>

              <!-- Submit -->
              <button
                class="btn btn-primary w-100"
                :disabled="loading"
                @click="login"
              >
                <span v-if="loading">
                  <span class="spinner-border spinner-border-sm me-2"></span>Logging in…
                </span>
                <span v-else>Log In</span>
              </button>

              <hr class="my-3" />

              <p class="text-center small text-muted mb-0">
                Don't have an account?
                <nuxt-link to="/auth/register" class="text-primary fw-semibold">Register here</nuxt-link>
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
  name: 'LoginPage',
  layout: 'master',
  auth: 'guest',

  data() {
    return {
      form: {
        phone: '',
        password: '',
      },
      loading: false,
      error: null,
    }
  },

  methods: {
    async login() {
      this.error = null
      this.loading = true
      try {
        await this.$auth.loginWith('local', {
          data: { phone: this.form.phone, password: this.form.password },
        })

        const role = this.$auth.user.role
        const redirects = {
          farmer:      '/farmer/dashboard',
          godown:      '/godown/dashboard',
          transporter: '/transporter/jobs',
          consumer:    '/',
          admin:       '/admin/dashboard',
        }
        this.$router.push(redirects[role] || '/')
      } catch (e) {
        this.error = 'Invalid phone number or password. Please try again.'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>