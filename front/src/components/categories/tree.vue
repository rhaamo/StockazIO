<template>
  <ul class="cat-list">
    <li>
      <i class="fa fa-folder-o" /> <router-link :to="{ name: 'parts-category-list', params: { categoryId: 0, category: {} } }" title="Uncategorized parts">
        Uncategorized parts
      </router-link>
    </li>

    <node :node="treeData" />
  </ul>
</template>

<script>
import node from './node'

export default {
  components: {
    node
  },
  props: ['treeData']
}
</script>
