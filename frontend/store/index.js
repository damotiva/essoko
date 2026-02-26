// store/index.js
// Matches the $store.state.auth_user_data pattern your layout already uses.

export const state = () => ({
    auth_user_data: null,
  })
  
  export const mutations = {
    // Called after login or register
    setAuthUser(state, payload) {
      state.auth_user_data = {
        auth_user:  payload.auth_user,
        auth_token: payload.auth_token,
        refresh:    payload.refresh,
        user_id:    payload.user_id,
      }
    },
  
    // Called when user logs out
    logout(state) {
      state.auth_user_data = null
    },
  }
  
  export const getters = {
    isLoggedIn: (state) => !!state.auth_user_data?.auth_token,
    authUser:   (state) => state.auth_user_data?.auth_user   || null,
    authToken:  (state) => state.auth_user_data?.auth_token  || null,
    userRole:   (state) => state.auth_user_data?.auth_user?.role || null,
  }