import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

import auth from './auth'
import server from './server'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    auth,
    server
  },
  plugins: [
    createPersistedState({
      key: 'auth',
      paths: ['auth'],
      filter: (mutation) => {
        return mutation.type.startsWith('auth/')
      }
    }),
    createPersistedState({
      key: 'server',
      paths: ['server.serverUrl']
    })
  ]
})
