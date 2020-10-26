import Vue from 'vue'
import App from './App.vue'
import routes from './router'
import store from './store'
import axios from 'axios'
import logger from '@/logging'
import { sync } from 'vuex-router-sync'
import BootstrapVue from 'bootstrap-vue'
import VueRouter from 'vue-router'
import GetTextPlugin from 'vue-gettext'
import locales from './locales.js'
import VueAxios from 'vue-axios'

logger.default.info('Loading environment:', process.env.NODE_ENV)
logger.default.debug('Environment variables:', process.env)

Vue.config.productionTip = false

const availableLanguages = (function () {
  const l = {}
  locales.locales.forEach(c => {
    l[c.code] = c.label
  })
  return l
})()
Vue.use(GetTextPlugin, {
  availableLanguages: availableLanguages,
  defaultLanguage: 'en_US',
  muteLanguages: ['en_US'], // Ignore 'translations not found' for en_US since it's our base language
  // cf https://github.com/Polyconseil/vue-gettext#configuration
  // not recommended but this is fixing weird bugs with translation nodes
  // not being updated when in v-if/v-else clauses
  autoAddKeyAttributes: true,
  languageVmMixin: {
    computed: {
      currentKebabCase: function () {
        return this.current.toLowerCase().replace('_', '-')
      }
    }
  },
  translations: {},
  silent: false
})

Vue.use(VueAxios, axios)
Vue.use(VueRouter)
Vue.use(BootstrapVue)

axios.interceptors.request.use(function (config) {
  // Do something before request is sent
  if (store.state.oauth.userToken) {
    config.headers['Authorization'] = `Bearer ${store.state.oauth.userToken}`
  }
  return config
}, function (error) {
  // Do something with request error
  return Promise.reject(error)
})

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: routes(store)
})

sync(store, router)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
