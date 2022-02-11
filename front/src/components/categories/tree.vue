<template>
  <ul class="cat-list">
    <li>
      <i class="fa fa-folder-o" /> <router-link :to="{ name: categoriesRouteName, params: { categoryId: 0, category: {} } }" title="Uncategorized parts">
        Uncategorized parts <small>({{ serverInfos.parts_uncategorized_count }})</small>
      </router-link>
    </li>

    <CategoriesNode :node="treeData" />
  </ul>
</template>

<script>
import CategoriesNode from './node'
import { mapState } from 'vuex'

export default {
  name: 'CategoriesTree',
  components: {
    CategoriesNode
  },
  props: {
    'treeData': Object
  },
  computed: {
    ...mapState({
      serverInfos: state => state.server
    }),
    currentUser () { return this.$store.state.user.currentUser && this.$store.state.oauth.loggedIn },
    categoriesRouteName () { return this.currentUser ? 'parts-category-list' : 'public-parts-category-list' }
  }
}
</script>
