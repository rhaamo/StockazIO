/*
 * File imported from https://git.pleroma.social/pleroma/pleroma-fe/blob/develop/src/modules/oauth.js
 */
// import { delete as del } from 'vue'
import logger from '@/logging'

const oauth = {
  state: {
    clientId: false,
    clientSecret: false,
    /* App token is authentication for app without any user, used mostly for
     * MastoAPI's registration of new users, stored so that we can fall back to
     * it on logout
     */
    appToken: false,
    /* User token is authentication for app with user, this is for every calls
     * that need authorized user to be successful (i.e. posting, liking etc)
     */
    userToken: false,
    loggedIn: false
  },
  mutations: {
    setClientData (state, { clientId, clientSecret }) {
      state.clientId = clientId
      state.clientSecret = clientSecret
      logger.default.info('A new OAuth app has been registered')
    },
    setAppToken (state, token) {
      state.appToken = token
    },
    setToken (state, token) {
      state.userToken = token
    },
    clearToken (state) {
      state.userToken = false
      // state.token is userToken with older name, coming from persistent state
      // let's clear it as well, since it is being used as a fallback of state.userToken
      delete state.token
    },
    setLoggedIn (state, value) {
      state.loggedIn = value
    },
    clearTokens (state) {
      state.clientId = false
      state.clientSecret = false
      state.appToken = false
      state.userToken = false
    }
  },
  getters: {
    getToken: state => () => {
      // state.token is userToken with older name, coming from persistent state
      // added here for smoother transition, otherwise user will be logged out
      return state.userToken || state.token || state.appToken
    },
    getUserToken: state => () => {
      // state.token is userToken with older name, coming from persistent state
      // added here for smoother transition, otherwise user will be logged out
      return state.userToken || state.token
    },
    getClientId: state => () => {
      return state.clientId
    },
    getClientSecret: state => () => {
      return state.clientSecret
    },
    getLoggedIn: state => () => {
      return state.loggedIn
    }
  }
}

export default oauth
