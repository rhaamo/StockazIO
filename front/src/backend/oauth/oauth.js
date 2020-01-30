// Snippets extracted from https://git.pleroma.social/pleroma/pleroma-fe/blob/develop/src/services/new_api/oauth.js
import logger from '@/logging'
import Axios from 'axios'

const REDIRECT_URI = `${window.location.origin}/oauth-callback`

/*
 * Get the clientId and clientSecret if any or generate a new one
 */
export const getOrCreateApp = ({ clientId, clientSecret, commit }) => {
  logger.default.debug('getOrCreateApp called')
  if (clientId && clientSecret) {
    logger.default.info('We are using already known OAuth App infos')
    return Promise.resolve({ clientId, clientSecret })
  }

  return Axios.post('/oauth/apps/', {
    name: `stockazio_front_${(new Date()).toISOString()}`,
    redirect_uris: REDIRECT_URI,
    scopes: 'read write'
  })
    .then((app) => ({ clientId: app.data.client_id, clientSecret: app.data.client_secret }))
    .then((app) => commit('setClientData', app) || app)
}

/*
 * Get a token through password grant type
 */
const getTokenWithCredentials = ({ clientId, clientSecret, username, password }) => {
  logger.default.debug('getTokenWithCredentials called')
  return Axios.post('/oauth/token/', {
    client_id: clientId,
    client_secret: clientSecret,
    grant_type: 'password',
    scope: 'read write',
    username: username,
    password: password
  })
}

/*
 * Revoke a token
 */
const revokeToken = ({ app, token }) => {
  logger.default.debug('revokeToken called')
  return Axios.post('/oauth/revoke/', {
    client_id: app.clientId,
    client_secret: app.clientSecret,
    token: token
  })
}

const oauth = {
  getTokenWithCredentials,
  getOrCreateApp,
  revokeToken
}

export default oauth
