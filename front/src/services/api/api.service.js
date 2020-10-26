import Axios from 'axios'

const CHECK_TOKEN_URL = '/oauth/check_token'

const CATEGORIES_URL = '/api/v1/categories'

const verifyCredentials = () => {
  return Axios.get(CHECK_TOKEN_URL)
}

const getCategories = () => {
  return Axios.get(CATEGORIES_URL)
}

const apiService = {
  verifyCredentials,
  getCategories
}

export default apiService
