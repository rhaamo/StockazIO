<template>
  <ul class="list_storages">
    <li>
        <i class="fa fa-home" aria-hidden="true"></i> {{ item.name }}
        &nbsp;&nbsp;&nbsp;&nbsp;
        <b-button pill size="sm" variant="light"
        to="#"
        @click.native.prevent="addCategory(item.id)"
        :title="addCategoryTitle(item.name)">
          <i class="fa fa-home" aria-hidden="true"></i>&nbsp;
          <i class="fa fa-plus" aria-hidden="true"></i>
        </b-button>

        &nbsp;&nbsp;
        <b-button pill size="sm" variant="info"
        to="#"
        @click.native.prevent="addLocation(item.id)"
        :title="addLocationTitle(item.name)">
          <i class="fa fa-folder-o" aria-hidden="true"></i>&nbsp;
          <i class="fa fa-plus" aria-hidden="true"></i>
        </b-button>
    </li>
    <ListCategory v-for="item in item.children" :key="item.id"
    :item=item
    :level="level+1"></ListCategory>
    <ul class="list_storages"><ListLocation v-for="item in item.storage_locations" :key="item.uuid" :item=item
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
    addCategory (id) {
        this.$root.$emit('changeModalAddCategoryParent', id)
        // Important to nextTick otherwise we don't get the time to emit the parent ID change
        this.$nextTick(() => {
            this.$bvModal.show('modalStoragesAddCategory')
        })
    },
    addCategoryTitle (name) {
        return `Add category under '${name}'`
    },
    addLocationTitle (name) {
        return `Add location/box under '${name}'`
    }
  }
}
</script>
