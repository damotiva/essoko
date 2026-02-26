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
              <NuxtLink class="nav-link text-earth-green" to="/">Home</NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink class="nav-link text-earth-green" to="/listings">Products</NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink class="nav-link text-earth-green" to="/mobile_apps">Mobile Apps</NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink class="nav-link text-earth-green" to="/customer_support">Customer Support</NuxtLink>
            </li>
          </ul>

          <!-- Right: Auth Links -->
          <ul class="navbar-nav auth-nav">
            <!-- Logged In State -->
            <template v-if="isAuthenticated">
              <li class="nav-item">
                <NuxtLink :to="dashboardRoute" class="btn btn-outline-success nav-link text-earth-green mr-2">
                  Dashboard
                </NuxtLink>
              </li>
              <li class="nav-item dropdown">
                <button class="dropdown-item text-danger" @click="logout" >Log Out</button>
              </li>
            </template>

            <!-- Logged Out State -->
            <template v-else>
              <li class="nav-item">
                <NuxtLink to="/auth/login" class="btn btn-link nav-link text-earth-green">
                  Log In
                </NuxtLink>
              </li>
              <li class="nav-item">
                <NuxtLink to="/auth/register" class="btn btn-success nav-link text-white">
                  Get Started
                </NuxtLink>
              </li>
            </template>
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
    isAuthenticated() {
      return this.$auth?.loggedIn || false
    },
    
    user() {
      return this.$auth?.user || null
    },
    
    userName() {
      return this.user?.name || this.user?.username || this.user?.phone || 'User'
    },
    
    userRole() {
      return this.user?.role || null
    },
    
    dashboardRoute() {
      const routes = {
        farmer: '/farmer/dashboard',
        godown: '/godown/dashboard',
        transporter: '/transporter/jobs',
        consumer: '/',
        admin: '/admin/dashboard',
      }
      return routes[this.userRole] || '/dashboard'
    }
  },
  
  methods: {
    async logout() {
      try {
        await this.$auth.logout()
        this.$router.push('/')
      } catch (error) {
        console.error('Logout failed:', error)
        // Force logout even if API fails
        this.$auth.reset()
        this.$router.push('/auth/login')
      }
    },
    
    scrollToTop() {
      window.scrollTo(0, 0)
      this.$router.push('/')
    }
  }
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

/* Force auth nav to the right */
.auth-nav {
  margin-left: auto !important;
  display: flex;
  align-items: center;
}

/* Button styling consistency */
.btn-outline-success {
  border-color: #2D6A4F;
  color: #2D6A4F;
}
.btn-outline-success:hover {
  background-color: #2D6A4F;
  color: white;
}

@media (max-width: 992px) {
  .navbar-nav {
    margin-top: 10px;
  }
  .auth-nav {
    margin-left: 0 !important;
    flex-direction: column;
    align-items: flex-start;
  }
  .auth-nav .nav-item {
    margin-right: 0;
    margin-bottom: 0.5rem;
    width: 100%;
  }
  .auth-nav .btn {
    width: 100%;
    text-align: left;
  }
}
</style>