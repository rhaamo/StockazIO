<template>
  <ul>
    <li><i class="fa fa-home" aria-hidden="true"></i> {{ item.name }}</li>
    <ListCategory v-for="item in item.children" :key="item.id" :item=item
    :level="level+1"></ListCategory>
    <ul><ListLocation v-for="item in item.storage_locations" :key="item.uuid" :item=item
    :level="level+1"></ListLocation></ul>
  </ul>
</template>

<script>
import ListLocation from './list-location'

export default {
  name: 'ListCategory',
  components: {
    ListLocation
  },
  props: {
    'item': Object,
    'level': Number
  },
  computed: {
  },
  methods: {
  }
}
</script>
