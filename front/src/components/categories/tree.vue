<template>
  <ul class="cat-list">
    <li>
      <i class="fa fa-folder-o" /> <router-link :to="{ name: 'parts-category-list', params: { categoryId: 0, category: {} } }" title="Uncategorized parts">
        Uncategorized parts <small>({{ serverInfos.parts_uncategorized_count }})</small>
      </router-link>
    </li>

    <node :node="treeData" />
  </ul>
</template>

<script>
import node from './node'
import { mapState } from 'vuex'

export default {
  components: {
    node
  },
  props: ['treeData'],
  computed: {
    ...mapState({
      serverInfos: state => state.server
    })
  }
}
</script>
