
import axios from 'axios'
import logger from '@/logging'
import _ from '@/lodash'

function getDefaultUrl () {
  return (
    window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '') + '/'
  )
}

export default {
  namespaced: true,
  state: {
    serverUrl: process.env.VUE_APP_SERVER_URL,
    settings: {
      pagination: {},
      partAttachmentAllowedTypes: [],
      backendVersion: '',
      registrationEnabled: false
    }
  },
  mutations: {
    serverUrl: (state, value) => {
      logger.default.info('Setting serverUrl with', value)
      if (value && !value.endsWith('/')) {
        value = value + '/'
      }
      state.serverUrl = value
      if (!value) {
        axios.defaults.baseURL = null
        return
      }
      let suffix = 'api/v1/'
      axios.defaults.baseURL = state.serverUrl + suffix
      // auth.baseURL = state.serverUrl + suffix
    },
    settings: (state, value) => {
      logger.default.info('Merging settings with', value)
      _.merge(state.settings, value)
    }
  },
  getters: {
    defaultUrl: (state) => () => {
      return getDefaultUrl()
    }
  },
  actions: {
    setUrl ({ commit, dispatch }, url) {
      commit('serverUrl', url)
      let modules = ['auth']
      modules.forEach(m => {
        commit(`${m}/reset`, null, { root: true })
      })
    },
    fetchSettings ({ commit }, payload) {
      return axios.get('app/settings').then(response => {
        logger.default.info('Successfully fetched server settings')
        let sections = {}
        sections.partAttachmentAllowedTypes = response.data.part_attachment_allowed_types
        sections.pagination = response.data.pagination
        sections.backendVersion = response.data.version
        sections.registrationEnabled = false // TODO
        commit('settings', sections)
      }, response => {
        logger.default.error('Error while fetching settings', response.data)
      })
    }
  }
}
