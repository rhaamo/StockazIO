
export default {
  namespaced: true,
  state: {
    isAuthenticated: false,
    user: {
      email: '',
      username: ''
    },
    scopes: {
      read: false,
      write: false,
      admin: false
    },
    accessToken: ''
  },
  getters: {
    header: state => {
      return 'Bearer ' + state.accessToken
    },
    isAuthenticated () {
      return this.$auth.isAuthenticated()
    }
  },
  mutations: {
    reset (state) {
      state.isAuthenticated = false
      state.user.email = ''
      state.user.username = ''
      state.scopes = {
        read: false,
        write: false,
        admin: false
      }
      state.accessToken = ''
    },
    isAuthenticated: (state, value) => {
      state.isAuthenticated = value
      if (value === false) {
        state.user.email = ''
        state.user.username = ''
        state.accessToken = ''
        state.scopes = {
          read: false,
          write: false,
          admin: false
        }
      }
    },
    user: (state, { key, value }) => {
      state.user[key] = value
    },
    accessToken: (state, value) => {
      state.accessToken = value
    },
    scope: (state, { key, status }) => {
      state.scope[key] = status
    }
  },
  actions: {
    login ({ commit, dispatch }, { next, credentials, onError }) {
      console.log('pls login')
    },
    logout ({ commit }) {
      console.log('pls logout')
    },
    check ({ commit, dispatch, state }) {
      console.log('pls check auth')
    }
  }
}
