<template>
  <ul class="cat-list">
      <node :node="treeData"></node>
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
