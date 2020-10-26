<template>
  <li>
    <template v-if="node.parts_count >0">
      <i class="fa fa-folder"></i> <a :title="node.name">{{ node.name }} <small><b>({{ node.parts_count }})</b></small></a>
    </template>
    <template v-else>
      <i class="fa fa-folder"></i> <a :title="node.name">{{ node.name }} <small>({{ node.parts_count }})</small></a>
    </template>

    <ul v-if="node.children && node.children.length" class="children">
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
