import Axios from 'axios'

const CHECK_TOKEN_URL = '/oauth/check_token'

const CATEGORIES_URL = '/api/v1/categories'

const APP_INFORMATIONS_URL = '/api/v1/app/informations'

const verifyCredentials = () => {
  return Axios.get(CHECK_TOKEN_URL)
}

const getCategories = () => {
  return Axios.get(CATEGORIES_URL)
}

const getInformations = () => {
  return Axios.get(APP_INFORMATIONS_URL)
}

const apiService = {
  verifyCredentials,
  getCategories,
  getInformations
}

export default apiService
