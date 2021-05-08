import logger from '@/logging'

import apiService from '../services/api/api.service'

const preloads = {
  state: {
    categories: {},
    footprints: [],
    storages: [],
    parameters_unit: [],
    part_units: [],
    manufacturers: [],
    distributors: [],
    currentCategory: {
      id: null
    },
    partParametersPresets: []
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
    setCurrentCategory (state, value) {
      state.currentCategory = value
    },
    setPartParametersPresets (state, value) {
      state.partParametersPresets = value
    },
    incrementCategoryPartsCount (state, nodeId) {
      function incrementNode (node, nodeId) {
        if (node.id === nodeId) {
          node.parts_count += 1
        } else if (node.children && node.children.length) {
          for (let i = 0; i < node.children.length; i++) {
            incrementNode(node.children[i], nodeId)
          }
        }
      }
      if (nodeId !== null) { incrementNode(state.categories, nodeId) }
    },
    decrementCategoryPartsCount (state, nodeId) {
      function decrementNode (node, nodeId) {
        if (node.id === nodeId) {
          node.parts_count -= 1
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
    getCurrentCategory: state => () => {
      return state.currentCategory || { id: null }
    },
    getPartParametersPresets: state => () => {
      return state.partParametersPresets || []
    }
  },
  actions: {
    preloadStuff ({ commit, dispatch }) {
      dispatch('preloadSidebar')
      dispatch('preloadFootprints')
      dispatch('preloadStorages')
      dispatch('preloadParametersUnits')
      dispatch('preloadPartUnits')
      dispatch('preloadManufacturers')
      dispatch('preloadDistributors')
      dispatch('preloadPartParametersPresets')
    },
    preloadSidebar ({ commit }) {
      // Preload sidebar
      apiService.getCategories()
        .then((data) => {
          commit('setCategories', data.data[0])
          logger.default.info('Categories preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload categories', error.message)
        })
    },
    preloadFootprints ({ commit }) {
      // Preload footprints
      apiService.getFootprints()
        .then((data) => {
          commit('setFootprints', data.data)
          logger.default.info('Footprints preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload footprints', error.message)
        })
    },
    preloadStorages ({ commit }) {
      // Preload storages
      apiService.getStorages()
        .then((data) => {
          commit('setStorages', data.data)
          logger.default.info('Storages preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload storages', error.message)
        })
    },
    preloadParametersUnits ({ commit }) {
      // Preload units
      apiService.getParametersUnits()
        .then((data) => {
          commit('setParametersUnits', data.data)
          logger.default.info('Parameters Units preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload parameters units', error.message)
        })
    },
    preloadPartUnits ({ commit }) {
      // Preload part-units
      apiService.getPartUnits()
        .then((data) => {
          commit('setPartUnits', data.data)
          logger.default.info('Part Units preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload part units', error.message)
        })
    },
    preloadManufacturers ({ commit }) {
      // Preload manufacturers
      apiService.getManufacturers()
        .then((data) => {
          commit('setManufacturers', data.data)
          logger.default.info('Manufacturers preloaded')
        }).catch((error) => {
          logger.default.error('Cannot preload manufacturers', error.message)
        })
    },
    preloadDistributors ({ commit }) {
      // Preload distributors
      apiService.getDistributors()
        .then((data) => {
          commit('setDistributors', data.data)
          logger.default.info('Distributors preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload distributors', error.message)
        })
    },
    preloadPartParametersPresets ({ commit }) {
      // Preload part parameters presets
      apiService.getPartParameterPresets()
        .then((data) => {
          commit('setPartParametersPresets', data.data)
          logger.default.info('Part parameters presets preloaded')
        })
        .catch((error) => {
          logger.default.error('Cannot preload part parameters presets', error.message)
        })
    }
  }
}

export default preloads
