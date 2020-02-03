import Axios from 'axios'

const CHECK_TOKEN_URL = '/oauth/check_token'

const verifyCredentials = () => {
  return Axios.get(CHECK_TOKEN_URL)
}

const apiService = {
  verifyCredentials
}

export default apiService
