// Snippets extracted from https://git.pleroma.social/pleroma/pleroma-fe/blob/develop/src/services/new_api/oauth.js
import { reduce } from 'lodash'
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
    .then((response) => ({ clientId: response.client_id, clientSecret: response.client_secret }))
    .then((response) => commit('setClientData', response) || response)
}

/*
 *
 */
const login = ({ clientId }) => {
  logger.default.debug('login called')
  const data = {
    response_type: 'code',
    client_id: clientId,
    redirect_uri: REDIRECT_URI,
    scope: 'read write'
  }

  const dataString = reduce(data, (acc, v, k) => {
    const encoded = `${k}=${encodeURIComponent(v)}`
    if (!acc) {
      return encoded
    } else {
      return `${acc}&${encoded}`
    }
  }, false)

  // Do the redirect
  window.location.href = `/oauth/authorize?${dataString}`
}

/*
 * Get a token through password grant type
 */
const getTokenWithCredentials = ({ clientId, clientSecret, username, password }) => {
  logger.default.debug('getTokenWithCredentials called')
  const url = '/oauth/token'
  const form = new window.FormData()

  form.append('client_id', clientId)
  form.append('client_secret', clientSecret)
  form.append('grant_type', 'password')
  form.append('scope', 'read write')
  form.append('username', username)
  form.append('password', password)

  return window.fetch(url, {
    method: 'POST',
    body: form
  }).then((data) => data.json())
}

/*
 * Get a token via authorization_code grant type
 */
const getToken = ({ clientId, clientSecret, code }) => {
  logger.default.debug('getToken called')
  const url = '/oauth/token'
  const form = new window.FormData()

  form.append('client_id', clientId)
  form.append('client_secret', clientSecret)
  form.append('grant_type', 'authorization_code')
  form.append('code', code)
  form.append('token_endpoint_auth_method', 'client_secret_post')
  form.append('scope', 'read write')
  form.append('redirect_uri', REDIRECT_URI)

  return window.fetch(url, {
    method: 'POST',
    body: form
  }).then((data) => data.json())
}

/*
 * Get a token via client_credentials grant type
 */
export const getClientToken = ({ clientId, clientSecret }) => {
  logger.default.debug('getClientToken called')
  return Axios.post('/oauth/token/', {
    client_id: clientId,
    client_secret: clientSecret,
    grant_type: 'client_credentials',
    scope: 'read write',
    redirect_uri: REDIRECT_URI
  })
}

/*
 * Revoke a token
 */
const revokeToken = ({ app, token }) => {
  logger.default.debug('revokeToken called')
  const url = '/oauth/revoke/'
  const form = new window.FormData()

  form.append('client_id', app.clientId)
  form.append('client_secret', app.clientSecret)
  form.append('token', token)

  const auth = window.btoa(token)

  return window.fetch(url, {
    headers: { Authorization: `Basic ${auth}` },
    method: 'POST',
    body: form
  }).then((data) => data.json())
}

const oauth = {
  login,
  getToken,
  getTokenWithCredentials,
  getClientToken,
  getOrCreateApp,
  revokeToken
}

export default oauth
