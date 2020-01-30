import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import server from './server'
import user from './user'
import oauth from './oauth'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    server,
    user,
    oauth
  },
  plugins: [
    createPersistedState({
      key: 'oauth',
      paths: ['oauth'],
      filter: (mutation) => {
        return mutation.type.startsWith('oauth/')
      }
    }),
    createPersistedState({
      key: 'server',
      paths: ['server.serverUrl']
    })
  ]
})
