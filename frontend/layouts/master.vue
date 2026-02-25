<template>
  <div>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-lg fixed-top">
      <div class="container">
        <!-- Logo Section -->
        <a class="navbar-brand d-flex align-items-center" @click="scrollToTop">
          <div class="w-8 h-8 bg-earth-green rounded-tr-xl rounded-bl-xl flex items-center justify-center text-white font-bold text-lg">
            E
          </div>
          <span class="font-display text-2xl font-bold text-earth-green tracking-wide ml-2">SSOKO</span>
        </a>
        <!-- Toggler for Mobile Menu -->
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <!-- Navbar Links -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <!-- Left: Main Nav Links -->
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link text-earth-green" href="/">Home</a>
            </li>

            <li class="nav-item">
              <a class="nav-link text-earth-green">Products</a>
            </li>

            <li class="nav-item">
              <a class="nav-link text-earth-green">Mobile Apps</a>
            </li>

            <li class="nav-item">
              <a class="nav-link text-earth-green">Customer Support</a>
            </li>

          </ul>

          <!-- Right: Auth Links -->
          <ul class="navbar-nav auth-nav">
            <li v-if="user" class="nav-item">
              <span class="nav-link text-earth-green">{{ user.name }}</span>
            </li>
            <li v-if="user" class="nav-item">
              <button class="btn btn-link nav-link text-red-600" @click="logout">Log Out</button>
            </li>
            <li v-if="!user" class="nav-item">
              <button class="btn btn-link nav-link text-earth-green" @click="openModal('login')">Log In</button>
            </li>
            <li v-if="!user" class="nav-item">
              <button class="btn btn-success nav-link text-white" @click="openModal('register')">Get Started</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container-fluid">
      <br /><br /><br />
      <Nuxt />
    </div>
  </div>
</template>

<script>
export default {
  name: 'LayoutMaster',
  computed: {
    user() {
      return this.$store.state.auth_user_data?.auth_user || ''
    },
    authToken() {
      return this.$store.state.auth_user_data?.auth_token || ''
    },
    userId() {
      return this.$store.state.auth_user_data?.user_id || ''
    },
  },
  methods: {
    openModal(type) {
      this.$emit('openModal', type)
    },
    logout() {
      this.$store.commit('logout')
      this.$router.push('/login')
    },
    scrollToTop() {
      window.scrollTo(0, 0)
    },
  },
}
</script>

<style scoped>
.bg-earth-green {
  background-color: #2D6A4F;
}
.text-earth-green {
  color: #2D6A4F;
}
.text-red-600 {
  color: #EF4444;
}
.font-display {
  font-family: 'Playfair Display', serif;
}
.font-body {
  font-family: 'Inter', sans-serif;
}
.navbar-nav .nav-item {
  margin-right: 1rem;
}

/* Force auth nav to the right — overrides any Tailwind conflicts */
.auth-nav {
  margin-left: auto !important;
}

@media (max-width: 992px) {
  .navbar-nav {
    margin-top: 10px;
  }
  /* On mobile, auth nav stacks naturally — remove the forced margin */
  .auth-nav {
    margin-left: 0 !important;
  }
}
</style>