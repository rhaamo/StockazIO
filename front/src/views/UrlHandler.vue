<script>
export default {
  name: 'UrlHandler',
  computed: {
    searchQuery () {
      return this.$route.query.q
    }
  },
  created () {
    if (!this.searchQuery) {
      return this.$router.replace({ name: 'home' }).catch(() => {})
    } else {
      if (this.searchQuery.startsWith('stockazio://storageLocation/')) {
        let str = this.searchQuery.split('/')
        let uuid = str[str.length - 1]
        this.$router.replace({ name: 'parts-list', query: { storage_uuid: uuid } }).catch(() => {})
      } else if (this.searchQuery.startsWith('web+stockazio:storageLocation,')) {
        let str = this.searchQuery.split(',')
        let uuid = str[str.length - 1]
        this.$router.replace({ name: 'parts-list', query: { storage_uuid: uuid } }).catch(() => {})
      } else if (this.searchQuery.startsWith('stockazio://part/')) {
        let str = this.searchQuery.split('/')
        let uuid = str[str.length - 1]
        this.$router.replace({ name: 'parts-details', params: { partId: uuid } }).catch(() => {})
      } else if (this.searchQuery.startsWith('web+stockazio:part,')) {
        let str = this.searchQuery.split(',')
        let uuid = str[str.length - 1]
        this.$router.replace({ name: 'parts-details', params: { partId: uuid } }).catch(() => {})
      } else {
        this.$router.replace({ name: 'home' }).catch(() => {})
      }
    }
  }
}
</script>
