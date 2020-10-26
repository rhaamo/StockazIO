import logger from '@/logging'
import apiService from '../services/api/api.service'

export default {
  namespaced: true,
  state: {
    currentUser: false
  },
  getters: {

  },
  mutations: {
    setCurrentUser (state, user) {
      state.currentUser = user
    }
  },
  actions: {
    loginUser (store, accessToken) {
      apiService.verifyCredentials()
        .then((result) => {
          // TODO FIXME
          logger.default.info('credentials validated')
          store.commit('setLoggedIn', true, { root: true })
          store.commit('setCurrentUser', result.data.user)
        })
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
          logger.default.info('credentials validated')
          commit('oauth/loggedIn', true)
          commit('setCurrentUser', result.data.user)
        })
    }
  }
}
