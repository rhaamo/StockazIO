import jsLogger from 'js-logger'

jsLogger.useDefaults()

export default {
  get: jsLogger.get,
  default: jsLogger.get('default')
}
