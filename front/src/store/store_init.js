import logger from '@/logging'
import { getOrCreateApp } from '../backend/oauth/oauth.js'

const checkOAuthToken = async ({ store }) => {
  return new Promise(async (resolve, reject) => {
    if (store.getters.getUserToken()) {
      try {
        await store.dispatch('loginUser', store.getters.getUserToken())
      } catch (e) {
        logger.default.error(e)
      }
    } else {
      logger.default.info('no user token present in cache')
    }
    resolve()
  })
}

const getAppSecret = async ({ store }) => {
  const { state, commit } = store
  const { oauth } = state
  return getOrCreateApp({ ...oauth, commit })
}

const initializeSomeStuff = async ({ store }) => {
  logger.default.info('Doing preliminary app initialization...')
  Promise.all([
    // Check token and try to log user if found
    checkOAuthToken({ store }),
    // Try to get or create oauth2 app and token thingy
    getAppSecret({ store })
  ])
    .catch(function (error) {
      logger.default.error('Error while doing initialization', error)
    })
}

export default initializeSomeStuff
