import Axios from 'axios'

const CHECK_TOKEN_URL = '/oauth/check_token'

const CATEGORIES_URL = '/api/v1/categories'

const APP_INFORMATIONS_URL = '/api/v1/app/informations'

const FOOTPRINTS_URL = '/api/v1/footprints'

const STORAGES_URL = '/api/v1/storages'

const PARAMETERS_UNITS_URL = '/api/v1/parts/parameters/units'
const PARAMETERS_UNITS_CREATE = '/api/v1/parts/parameters/units/'
const PARAMETERS_UNITS_DELETE = (id) => `/api/v1/parts/parameters/units/${id}`
const PARAMETERS_UNITS_UPDATE = (id) => `/api/v1/parts/parameters/units/${id}/`

const PART_UNITS_URL = '/api/v1/parts/units'
const PART_UNITS_CREATE = '/api/v1/parts/units/'
const PART_UNITS_DELETE = (partUnitId) => `/api/v1/parts/units/${partUnitId}`
const PART_UNITS_UPDATE = (partUnitId) => `/api/v1/parts/units/${partUnitId}/`

const PARTS_CREATE = '/api/v1/parts/'
const PARTS_LIST = '/api/v1/parts/'
const PARTS_UPDATE = (id) => `/api/v1/parts/${id}/`
const PARTS_ITEM = (partId) => `/api/v1/parts/${partId}`

const PARTS_AUTOCOMPLETE_QUICK = (name) => `/api/v1/parts/autocomplete/quick_by_name/${name}`

const MANUFACTURERS_URL = '/api/v1/manufacturers'

const DISTRIBUTORS_URL = '/api/v1/distributors'

const ORDERS_IMPORTER_LIST = '/api/v1/orders_importer/'
const ORDERS_IMPORTER_DETAILS = (id) => `/api/v1/orders_importer/${id}`
const ORDERS_IMPORTER_UPDATE = (id) => `/api/v1/orders_importer/${id}`

const CATEGORIES_MATCHERS_LIST = '/api/v1/orders_importer/category_matcher/'
const CATEGORIES_MATCHERS_BATCH_UPDATE = '/api/v1/orders_importer/category_matcher/batch_update'
const CATEGORIES_MATCHERS_REMATCH = '/api/v1/orders_importer/category_matcher/rematch'

const verifyCredentials = () => {
  return Axios.get(CHECK_TOKEN_URL)
}

const getCategories = () => {
  return Axios.get(CATEGORIES_URL)
}

const getInformations = () => {
  return Axios.get(APP_INFORMATIONS_URL)
}

const getFootprints = () => {
  return Axios.get(FOOTPRINTS_URL)
}

const getStorages = () => {
  return Axios.get(STORAGES_URL)
}

const getParametersUnits = () => {
  return Axios.get(PARAMETERS_UNITS_URL)
}

const createParametersUnits = (data) => {
  return Axios.post(PARAMETERS_UNITS_CREATE, data)
}

const deleteParametersUnits = (id) => {
  return Axios.delete(PARAMETERS_UNITS_DELETE(id))
}

const updateParametersUnits = (id, data) => {
  return Axios.put(PARAMETERS_UNITS_UPDATE(id), data)
}

const getPartUnits = () => {
  return Axios.get(PART_UNITS_URL)
}

const createPartUnit = (data) => {
  return Axios.post(PART_UNITS_CREATE, data)
}

const deletePartUnit = (partUnitId) => {
  return Axios.delete(PART_UNITS_DELETE(partUnitId))
}

const updatePartUnit = (partUnitId, data) => {
  return Axios.put(PART_UNITS_UPDATE(partUnitId), data)
}

const getManufacturers = () => {
  return Axios.get(MANUFACTURERS_URL)
}

const getDistributors = () => {
  return Axios.get(DISTRIBUTORS_URL)
}

const createPart = (data) => {
  return Axios.post(PARTS_CREATE, data)
}

const updatePart = (id, data) => {
  return Axios.put(PARTS_UPDATE(id), data)
}

const updatePartialPart = (id, data) => {
  return Axios.patch(PARTS_UPDATE(id), data)
}

const getParts = (params) => {
  return Axios.get(PARTS_LIST, { params: params })
}

const getPart = (partId) => {
  return Axios.get(PARTS_ITEM(partId))
}

const deletePart = (partId) => {
  return Axios.delete(PARTS_ITEM(partId))
}

const partsAutocompleteQuick = (name) => {
  return Axios.get(PARTS_AUTOCOMPLETE_QUICK(name))
}

/* Order Importer */

const getOrderImporter = (id) => {
  return Axios.get(ORDERS_IMPORTER_DETAILS(id))
}

const updateOrderImporter = (id, data) => {
  return Axios.put(ORDERS_IMPORTER_UPDATE(id), data)
}

const updatePartialOrderImporter = (id, data) => {
  return Axios.patch(ORDERS_IMPORTER_UPDATE(id), data)
}

const getOrdersImporter = () => {
  return Axios.get(ORDERS_IMPORTER_LIST)
}

const getCategoryMatchers = () => {
  return Axios.get(CATEGORIES_MATCHERS_LIST)
}

const updateCategoryMatchers = (data) => {
  return Axios.patch(CATEGORIES_MATCHERS_BATCH_UPDATE, data)
}

const rematchOrderItems = () => {
  return Axios.get(CATEGORIES_MATCHERS_REMATCH)
}

const apiService = {
  verifyCredentials,
  getCategories,
  getInformations,
  getFootprints,
  getStorages,
  getParametersUnits,
  createParametersUnits,
  deleteParametersUnits,
  updateParametersUnits,
  getPartUnits,
  createPartUnit,
  deletePartUnit,
  updatePartUnit,
  getManufacturers,
  getDistributors,
  createPart,
  updatePart,
  updatePartialPart,
  getParts,
  getPart,
  deletePart,
  partsAutocompleteQuick,
  getOrdersImporter,
  getOrderImporter,
  updateOrderImporter,
  updatePartialOrderImporter,
  getCategoryMatchers,
  updateCategoryMatchers,
  rematchOrderItems
}

export default apiService
