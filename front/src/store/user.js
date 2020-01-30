
export default {
  state: {
    currentUser: false
  },
  getters: {

  },
  mutations: {
  },
  actions: {
    loginUser (store, accessToken) {
      console.log('pls loginUser')
      // implement a check credentials in backend
      // call it
      // and that's it
    },
    logout (store) {
      console.log('pls logout')
    },
    // eslint-disable-next-line camelcase
    async login ({ state, dispatch, commit }, { access_token }) {
      commit('setToken', access_token, { root: true })
      await dispatch('loginUser', access_token, { root: true })
    }
  }
}
