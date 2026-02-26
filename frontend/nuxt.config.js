export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'ESSOKO — Earth · Supply · Soko',
    
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.png' },
      { rel: 'stylesheet', href: '/bootstrap/css/bootstrap.min.css' },
      { rel: 'stylesheet', href: '/fontawesome/css/fontawesome.min.css' },
      { rel: 'stylesheet', href: '/fontawesome/css/all.min.css' },
      { rel: 'stylesheet', href: '/style/css/demo_3/style.css' },
      { rel: 'stylesheet', href: '/style/css/custom.css' },
      { rel: 'stylesheet', href: '/style/assets/plugin/datatables/responsive.dataTables.min.css' },
      { rel: 'stylesheet', href: '/style/assets/plugin/datatables/dataTables.bootstrap5.min.css' },
    ],
    script: [
      {src: '/style/js/jquery.min.js'},
      {src: '/bootstrap/js/bootstrap.min.js'},
      {src: '/fontawesome/js/fontawesome.min.js'},
      // {src: '/style/assets/bundles/libscripts.bundle.js'},
      // {src: '/style/assets/bundles/apexcharts.bundle.js'},
      {src: '/style/assets/plugin/jqueryuicalandar/jquery-ui.min.js'},
      {src: '/style/assets/plugin/owlcarousel/owl.carousel.js'},
      {src: '/style/assets/bundles/dataTables.bundle.js'},
      // {src: '/style/assets/template.js'},
      // {src: '/style/assets/page/index.js'}
    ]
  },

  auth: {
    strategies: {
      local: {
        scheme: 'refresh',
        token: {
          property: 'access',
          maxAge: 86400,               // 24h in seconds
          type: 'Bearer',
        },
        refreshToken: {
          property: 'refresh',
          data: 'refresh',
          maxAge: 2592000,             // 30 days
        },
        user: {
          property: false,             // User returned directly
          autoFetch: true,
        },
        endpoints: {
          login:   { url: '/auth/login/',        method: 'post' },
          refresh: { url: '/auth/token/refresh/', method: 'post' },
          logout:  { url: '/auth/logout/',       method: 'post' },
          user:    { url: '/auth/me/',            method: 'get' },
        },
      },
    },
    redirect: {
      login:    '/login',
      logout:   '/',
      callback: '/login',
      home:     '/',
    },
  },

  router: {
    middleware: ['auth'],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: '~/plugins/plugin.js', ssr: false },
    { src: '~/plugins/toastification.client.js', ssr: false},
    { src: '~/plugins/persistedState.js', ssr: false },
  ],

  server: {
    host: '0.0.0.0',
    port: 80
  },

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    '@nuxtjs/vuetify', 
    '@braid/vue-formulate/nuxt',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
  ],

  axios: {
    baseURL: 'http://127.0.0.1:8000/api/v1'
    
    // baseURL: 'https://api.essoko.com/api/v1'  
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  },

  server: {
    host: '0.0.0.0',
    port: 80
  },
}
