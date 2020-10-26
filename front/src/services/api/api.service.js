import Axios from 'axios'

const CHECK_TOKEN_URL = '/oauth/check_token'

const CATEGORIES_URL = '/api/v1/categories'

const APP_INFORMATIONS_URL = '/api/v1/app/informations'

const FOOTPRINTS_URL = '/api/v1/footprints'

const STORAGES_URL = '/api/v1/storages'

const PARAMETERS_UNITS_URL = '/api/v1/parts/parameters/units'

const PART_UNITS_URL = '/api/v1/parts/units'

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

const getManufacturers = () => {
  return Axios.get(MANUFACTURERS_URL)
}

const getDistributors = () => {
  return Axios.get(DISTRIBUTORS_URL)
}

const apiService = {
  verifyCredentials,
  getCategories,
  getInformations,
  getFootprints,
  getStorages,
  getParametersUnits,
  getPartUnits,
  getManufacturers,
  getDistributors
}

export default apiService
