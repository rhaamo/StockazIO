import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
import server from './server'
import user from './user'
import oauth from './oauth'
import preloads from './preloads'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    server,
    user,
    oauth,
    preloads
  },
  plugins: [
    new VuexPersistence({
      reducer: (state) => ({ oauth: state.oauth, server: state.server })
    }).plugin
  ]
})
