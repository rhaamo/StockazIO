import logger from '@/logging'

import apiService from '../services/api/api.service'
import { differenceInMinutes, parseISO } from 'date-fns'

// one day
const REFRESH_TIME = 1440

const preloads = {
  state: {
    categories: {},
    footprints: [],
    storages: [],
    parameters_unit: [],
    part_units: [],
    manufacturers: [],
    distributors: [],
    label_templates: [],
    currentCategory: {
      id: null
    },
    partParametersPresets: [],
    // Contain last (initial=null) date of fetch for each set of preload
    lastUpdate: {
      categories: null,
      footprints: null,
      storages: null,
      parameters_units: null,
      part_units: null,
      manufacturers: null,
      distributors: null,
      label_templates: null
    }
  },
  mutations: {
    setCategories (state, value) {
      state.categories = value
    },
    setFootprints (state, value) {
      state.footprints = value
    },
    setStorages (state, value) {
      state.storages = value
    },
    setParametersUnits (state, value) {
      state.parameters_unit = value
    },
    setPartUnits (state, value) {
      state.part_units = value
    },
    setManufacturers (state, value) {
      state.manufacturers = value
    },
    setDistributors (state, value) {
      state.distributors = value
    },
    setLabelTemplates (state, value) {
      state.label_templates = value
    },
    setCurrentCategory (state, value) {
      state.currentCategory = value
    },
    setPartParametersPresets (state, value) {
      state.partParametersPresets = value
    },
    // setLastUpdate take a dict as value {item: 'xxx', value: 'date 42'}
    setLastUpdate (state, value) {
      if (value && value.value) {
        // Cannot save a Date() object in LocalStorage, so convert it to ISO String
        state.lastUpdate[value.item] = value.value.toISOString()
      } else {
        // When nulled to force reload
        state.lastUpdate[value.item] = value.value
      }
    },
    incrementCategoryPartsCount (state, { nodeId, by = 1 }) {
      function incrementNode (node, nodeId) {
        if (node.id === nodeId) {
          node.parts_count += by
        } else if (node.children && node.children.length) {
          for (let i = 0; i < node.children.length; i++) {
            incrementNode(node.children[i], nodeId)
          }
        }
      }
      if (nodeId !== null) { incrementNode(state.categories, nodeId) }
    },
    decrementCategoryPartsCount (state, { nodeId, by = 1 }) {
      function decrementNode (node, nodeId) {
        if (node.id === nodeId) {
          node.parts_count -= by
        } else if (node.children && node.children.length) {
          for (let i = 0; i < node.children.length; i++) {
            decrementNode(node.children[i], nodeId)
          }
        }
      }
      if (nodeId !== null) { decrementNode(state.categories, nodeId) }
    }
  },
  getters: {
    getCategories: state => () => {
      return state.categories || {}
    },
    getFootprints: state => () => {
      return state.footprints || []
    },
    getStorages: state => () => {
      return state.storages || []
    },
    getParametersUnits: state => () => {
      return state.parameters_unit || []
    },
    getPartUnits: state => () => {
      return state.part_units || []
    },
    getManufacturers: state => () => {
      return state.manufacturers || []
    },
    getDistributors: state => () => {
      return state.distributors || []
    },
    getLabelTemplates: state => () => {
      return state.label_templates || []
    },
    getCurrentCategory: state => () => {
      return state.currentCategory || { id: null }
    },
    getPartParametersPresets: state => () => {
      return state.partParametersPresets || []
    },
    getLastUpdate: state => (item) => {
      if (item) {
        return state.lastUpdate[item]
      } else {
        return state.lastUpdate
      }
    }
  },
  actions: {
    async preloadStuff ({ commit, dispatch }) {
      await dispatch('preloadSidebar')
      await dispatch('preloadFootprints')
      await dispatch('preloadStorages')
      await dispatch('preloadParametersUnits')
      await dispatch('preloadPartUnits')
      await dispatch('preloadManufacturers')
      await dispatch('preloadDistributors')
      await dispatch('preloadLabelTemplates')
      await dispatch('preloadPartParametersPresets')
    },
    preloadSidebar ({ commit, state }) {
      // Preload sidebar
      let dateRefreshed = state.lastUpdate.categories
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        console.log('Categories do not need reload')
        return
      }
      return apiService.getCategories()
        .then((data) => {
          commit('setCategories', data.data[0])
          commit('setLastUpdate', { item: 'categories', value: new Date() })
          logger.default.info('Categories preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload categories', error.message)
        })
    },
    preloadFootprints ({ commit, state }) {
      // Preload footprints
      let dateRefreshed = state.lastUpdate.footprints
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        console.log('Footprints do not need reload')
        return
      }
      return apiService.getFootprints()
        .then((data) => {
          commit('setFootprints', data.data)
          commit('setLastUpdate', { item: 'footprints', value: new Date() })
          logger.default.info('Footprints preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload footprints', error.message)
        })
    },
    preloadStorages ({ commit, state }) {
      // Preload storages
      let dateRefreshed = state.lastUpdate.storages
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        console.log('Storages do not need reload')
        return
      }
      return apiService.getStorages()
        .then((data) => {
          commit('setStorages', data.data)
          commit('setLastUpdate', { item: 'storages', value: new Date() })
          logger.default.info('Storages preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload storages', error.message)
        })
    },
    preloadParametersUnits ({ commit, state }) {
      // Preload units
      let dateRefreshed = state.lastUpdate.parameters_units
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        console.log('Parameters Units do not need reload')
        return
      }
      return apiService.getParametersUnits()
        .then((data) => {
          commit('setParametersUnits', data.data)
          commit('setLastUpdate', { item: 'parameters_units', value: new Date() })
          logger.default.info('Parameters Units preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload parameters units', error.message)
        })
    },
    preloadPartUnits ({ commit, state }) {
      // Preload part-units
      let dateRefreshed = state.lastUpdate.part_units
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        console.log('Part Units do not need reload')
        return
      }
      return apiService.getPartUnits()
        .then((data) => {
          commit('setPartUnits', data.data)
          commit('setLastUpdate', { item: 'part_units', value: new Date() })
          logger.default.info('Part Units preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload part units', error.message)
        })
    },
    preloadManufacturers ({ commit, state }) {
      // Preload manufacturers
      let dateRefreshed = state.lastUpdate.manufacturers
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        console.log('Manufacturers do not need reload')
        return
      }
      return apiService.getManufacturers()
        .then((data) => {
          commit('setManufacturers', data.data)
          commit('setLastUpdate', { item: 'manufacturers', value: new Date() })
          logger.default.info('Manufacturers preloaded')
        }).catch((error) => {
          logger.default.error('Cannot preload manufacturers', error.message)
        })
    },
    preloadDistributors ({ commit, state }) {
      // Preload distributors
      let dateRefreshed = state.lastUpdate.distributors
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        console.log('Distributors do not need reload')
        return
      }
      return apiService.getDistributors()
        .then((data) => {
          commit('setDistributors', data.data)
          commit('setLastUpdate', { item: 'distributors', value: new Date() })
          logger.default.info('Distributors preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload distributors', error.message)
        })
    },
    preloadLabelTemplates ({ commit, state }) {
      // Preload Label Templates
      let dateRefreshed = state.lastUpdate.label_templates
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        console.log('Label Templates do not need reload')
        return
      }
      return apiService.getLabelTemplates()
        .then((data) => {
          commit('setLabelTemplates', data.data)
          commit('setLastUpdate', { item: 'label_templates', value: new Date() })
          logger.default.info('Label Templates preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload Label Templates', error.message)
        })
    },
    preloadPartParametersPresets ({ commit, state }) {
      // Preload part parameters presets
      let dateRefreshed = state.lastUpdate.parameters_presets
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        console.log('Part parameters do not need reload')
        return
      }
      return apiService.getPartParameterPresets()
        .then((data) => {
          commit('setPartParametersPresets', data.data.results)
          commit('setLastUpdate', { item: 'parameters_presets', value: new Date() })
          logger.default.info('Part parameters presets preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload part parameters presets', error.message)
        })
    }
  }
}

export default preloads
