<template>
  <li>
    {{ node.name }}

    <ul v-if="node.children && node.children.length" class="children">
      <node v-for="child in node.children" :key="child.id" :node="child" />
    </ul>

    <ul v-if="node.storage_locations && node.storage_locations.length" class="storage_locations">
      <node v-for="child in node.storage_locations" :key="child.id" :node="child" />
    </ul>
  </li>
</template>

<script>
export default {
  name: 'Node',
  props: ['node']
}
</script>
