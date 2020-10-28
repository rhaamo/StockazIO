<template>
  <li>
    <template v-if="node.parts_count >0">
      <i class="fa fa-folder" /> <router-link :to="{ name: 'parts-category-list', params: { categoryId: node.id, category: node } }" :title="node.name">
        <b>{{ node.name }} <small>({{ node.parts_count }})</small></b>
      </router-link>
    </template>
    <template v-else>
      <i class="fa fa-folder" /> <router-link :to="{ name: 'parts-category-list', params: { categoryId: node.id, category: node } }" :title="node.name">
        {{ node.name }} <small>({{ node.parts_count }})</small>
      </router-link>
    </template>

    <ul v-if="node.children && node.children.length" class="children">
      <node v-for="child in node.children" :key="child.id" :node="child" />
    </ul>
  </li>
</template>

<script>
export default {
  name: 'Node',
  props: ['node']
}
</script>
