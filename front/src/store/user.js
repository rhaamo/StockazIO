import apiService from '../services/api/api.service'

export default {
  namespaced: true,
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
      // Store token in store
      commit('setToken', access_token, { root: true })
      // Check the token validity
      apiService.verifyCredentials()
        .then((result) => {
        // TODO FIXME
        })
    }
  }
}
