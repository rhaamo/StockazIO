<template>
  <li class="node-tree">
    <span v-if="node.children && node.children.length" class="label"><b>{{ node.name }} ({{ node.children.length }})</b></span>
    <span v-else class="label">{{ node.name }} (0)</span>

    <ul v-if="node.children && node.children.length">
      <node v-for="child in node.children" :node="child" :key="child.id"></node>
    </ul>
  </li>
</template>

<script>
export default {
  name: 'node',
  props: ['node']
}
</script>
