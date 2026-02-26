// plugins/persistedState.js
// Saves auth_user_data to localStorage so login survives a page refresh.
// Your nuxt.config already loads this plugin: { src: '~/plugins/persistedState.js', ssr: false }

import createPersistedState from 'vuex-persistedstate'

export default ({ store }) => {
  createPersistedState({
    key: 'essoko_store',
    paths: ['auth_user_data'],   // only persist auth
  })(store)
}
