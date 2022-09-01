import { createStore } from 'vuex'
import VuexPersistence from 'vuex-persist'
import server from './server'
import user from './user'
import oauth from './oauth'
import preloads from './preloads'

export default createStore({
  modules: {
    server,
    user,
    oauth,
    preloads
  },
  plugins: [
    new VuexPersistence({
      reducer: (state) => ({ oauth: state.oauth, server: state.server, preloads: state.preloads })
    }).plugin
  ]
})
