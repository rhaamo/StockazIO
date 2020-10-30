import Axios from 'axios'

const CHECK_TOKEN_URL = '/oauth/check_token'

const CATEGORIES_URL = '/api/v1/categories'

const APP_INFORMATIONS_URL = '/api/v1/app/informations'

const FOOTPRINTS_URL = '/api/v1/footprints'

const STORAGES_URL = '/api/v1/storages'

const PARAMETERS_UNITS_URL = '/api/v1/parts/parameters/units'

const PART_UNITS_URL = '/api/v1/parts/units'
const PART_UNITS_CREATE = '/api/v1/parts/units/'
const PART_UNITS_DELETE = (partUnitId) => `/api/v1/parts/units/${partUnitId}`
const PART_UNITS_UPDATE = (partUnitId) => `/api/v1/parts/units/${partUnitId}/`

const PARTS_CREATE = '/api/v1/parts/'
const PARTS_BY_CATEGORY = (categoryId) => `/api/v1/parts/?category_id=${categoryId}`
const PARTS_LIST = '/api/v1/parts/'
const PARTS_ITEM = (partId) => `/api/v1/parts/${partId}`

const MANUFACTURERS_URL = '/api/v1/manufacturers'

const DISTRIBUTORS_URL = '/api/v1/distributors'

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

const getPartsByCategory = (categoryId) => {
  return Axios.get(PARTS_BY_CATEGORY(categoryId))
}

const getParts = () => {
  return Axios.get(PARTS_LIST)
}

const getPart = (partId) => {
  return Axios.get(PARTS_ITEM(partId))
}

const deletePart = (partId) => {
  return Axios.delete(PARTS_ITEM(partId))
}

const apiService = {
  verifyCredentials,
  getCategories,
  getInformations,
  getFootprints,
  getStorages,
  getParametersUnits,
  getPartUnits,
  createPartUnit,
  deletePartUnit,
  updatePartUnit,
  getManufacturers,
  getDistributors,
  createPart,
  getPartsByCategory,
  getParts,
  getPart,
  deletePart
}

export default apiService
