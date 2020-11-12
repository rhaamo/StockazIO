
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
    },
    parts_uncategorized_count: 0
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
      axios.defaults.baseURL = state.serverUrl
    },
    settings: (state, value) => {
      logger.default.info('Merging settings with', value)
      _.merge(state.settings, value)
    },
    parts_uncategorized_count: (state, value) => {
      state.parts_uncategorized_count = value
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
      return axios.get('/api/v1/app/settings').then(response => {
        logger.default.info('Successfully fetched server settings')
        let sections = {}
        sections.partAttachmentAllowedTypes = response.data.part_attachment_allowed_types
        sections.pagination = response.data.pagination
        sections.backendVersion = response.data.version
        sections.registrationEnabled = false // TODO
        commit('settings', sections)
        commit('parts_uncategorized_count', response.data.parts_uncategorized_count)
      }, response => {
        logger.default.error('Error while fetching settings', response.data)
      })
    }
  }
}
