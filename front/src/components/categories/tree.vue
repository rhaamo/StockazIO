<template>
  <ul class="cat-list">
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
