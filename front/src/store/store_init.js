import logger from '@/logging'
import { getOrCreateApp } from '../backend/oauth/oauth.js'

const checkOAuthToken = async ({ store }) => {
  return new Promise(async (resolve, reject) => {
    if (store.getters.getUserToken()) {
      try {
        await store.dispatch('user/loginUser', store.getters.getUserToken())
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

  // we have several way to guess the API server url. By order of precedence:
  // 1. use the url specified when building via VUE_APP_SERVER_URL
  // 2. use the current url
  let defaultServerUrl = process.env.VUE_APP_SERVER_URL || store.getters['server/defaultUrl']()
  logger.default.info('Detected server url:', defaultServerUrl)
  await store.commit('server/serverUrl', defaultServerUrl)
  // Fetch server settings
  await store.dispatch('server/fetchSettings').finally(() => {
    // Start oauth init
    // let store = this.$store
    // let router = this.$router
    // initializeSomeStuff({ store, router })
  })

  Promise.allSettled([
    // Check token and try to log user if found
    checkOAuthToken({ store }),
    // Try to get or create oauth2 app and token thingy
    getAppSecret({ store })
  ])
    .catch(function (error) {
      logger.default.error('Error while doing initialization', error)
    })
  logger.default.info('Initialization done.')

  if (store.state.oauth.loggedIn) {
    await store.dispatch('preloadStuff')
  } else {
    // Only preload stuff needed for unauthenticated views
    await store.dispatch('preloadSidebar')
    await store.dispatch('preloadFootprints')
    await store.dispatch('preloadStorages')
  }
}

export default initializeSomeStuff
