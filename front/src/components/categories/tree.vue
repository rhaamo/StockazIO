<template>
  <div class="tree">
      <ul class="tree-list">
          <node :node="treeData"></node>
      </ul>
  </div>
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
