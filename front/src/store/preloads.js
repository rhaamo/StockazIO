const preloads = {
  state: {
    categories: {},
    footprints: [],
    storages: [],
    parameters_unit: {},
    part_units: {},
    manufacturers: {},
    distributors: {}
  },
  mutations: {
    setCategories (state, value) {
      state.categories = value
    },
    setFootprints (state, value) {
      state.footprints = value
    },
    setStorages (state, value) {
      state.strorages = value
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
      state.distributorsz = value
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
      return state.parameters_unit || {}
    },
    getPartUnits: state => () => {
      return state.part_units || {}
    },
    getManufacturers: state => () => {
      return state.manufacturers || {}
    },
    getDistributors: state => () => {
      return state.distributors || {}
    }
  }
}

export default preloads
