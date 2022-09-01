import { createApp } from 'vue'
import axios from 'axios'
import { sync } from 'vuex-router-sync'
import BootstrapVue3 from 'bootstrap-vue-3'
import VueRouter from 'vue-router'
import GetTextPlugin from 'vue-gettext'
import Multiselect from 'vue-multiselect'
import Treeselect from '@riophae/vue-treeselect'
import VueAxios from 'vue-axios'
import VueQrcode from '@chenfengyuan/vue-qrcode'

import logger from '@/logging'
import store from './store'
import App from './App.vue'
import routes from './router'
import locales from './locales.js'
import initializeSomeStuff from './store/store_init'

import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'

logger.default.info('Loading environment:', process.env.NODE_ENV)
logger.default.debug('Environment variables:', process.env)

const app = createApp(App)

app.config.productionTip = false

const availableLanguages = (function () {
  const l = {}
  locales.locales.forEach(c => {
    l[c.code] = c.label
  })
  return l
})()
app.use(GetTextPlugin, {
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

app.use(VueAxios, axios)
app.use(VueRouter)
app.use(BootstrapVue3)
app.component(Multiselect.name, Multiselect)
app.component(Treeselect.name, Treeselect)
app.component(VueQrcode.name, VueQrcode)

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

app.mount('#app')

initializeSomeStuff({ store, router }).then(() => {
  app.use(router)
  app.use(store)
})
