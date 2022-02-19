// cherry-pick specific lodash methods here to reduce bundle size

export default {
  clone: require('lodash/clone'),
  keys: require('lodash/keys'),
  debounce: require('lodash/debounce'),
  get: require('lodash/get'),
  merge: require('lodash/merge'),
  range: require('lodash/range'),
  shuffle: require('lodash/shuffle'),
  sortBy: require('lodash/sortBy'),
  throttle: require('lodash/throttle'),
  uniq: require('lodash/uniq'),
  remove: require('lodash/remove'),
  reverse: require('lodash/reverse'),
  isEqual: require('lodash/isEqual'),
  sum: require('lodash/sum'),
  chunk: require('lodash/chunk')
}
