<template>
  <li>
      <i class="fa fa-folder-o" aria-hidden="true"></i> {{ item.name }}<br />
      <template v-if="item.description">&raquo; {{ item.description }}</template>
  </li>
</template>

<script>
export default {
  name: 'ListLocation',
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
