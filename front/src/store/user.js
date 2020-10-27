import logger from '@/logging'
import Axios from 'axios'
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
      return new Promise((resolve, reject) => {
        logger.default.info('verifying credentials')
        apiService.verifyCredentials()
          .then((result) => {
            logger.default.info('credentials validated')
            store.commit('setLoggedIn', true, { root: true })
            store.commit('setCurrentUser', result.data.user)
          })
          .catch((error) => {
            logger.default.error('cannot verify credentials', error.message)
            store.commit('setLoggedIn', false, { root: true })
            store.commit('setCurrentUser', {})
            reject(error)
          })
      })
    },
    logout (store) {
      const { oauth } = store.rootState

      logger.default.info('logging out')

      Axios.post('/oauth/revoke/', {
        token: oauth.userToken,
        client_id: oauth.clientId,
        client_secret: oauth.clientSecret
      }).then(() => {
        Promise.all([
          store.commit('setLoggedIn', false, { root: true }),
          store.commit('setCurrentUser', null)
        ])
      })
    },
    // eslint-disable-next-line camelcase
    async login ({ state, dispatch, commit }, { access_token }) {
      // Store token in store
      commit('setToken', access_token, { root: true })
      // Check the token validity
      apiService.verifyCredentials()
        .then((result) => {
          logger.default.info('credentials validated')
          commit('oauth/loggedIn', true)
          commit('setCurrentUser', result.data.user)
        })
    }
  }
}
