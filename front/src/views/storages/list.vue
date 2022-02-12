<template>
  <div class="storages_list">
    <ModalAddCategory
      :parent="modalAddCategoryParent" @modal-storages-add-category-closed="fetchStorages"
      @modal-storages-add-category-saved="fetchStorages"
    />

    <div class="row">
      <div class="col-8">
        <ol class="breadcrumb">
          <li class="breadcrumb-item active">
            <router-link :to="{ name: 'storages-list' }">
              Storage management
            </router-link>
          </li>
        </ol>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 mx-auto">
        <ul class="list_storages">
          <li>
            <b-button pill size="sm" variant="light"
            @click.prevent="addCategory(null)"
            title="Add storage category on root level">
              <i class="fa fa-plus-square-o" aria-hidden="true"></i> Add root category
            </b-button>
          </li>
        </ul>
        <template v-for="item in storages">
          <ListCategory v-if="item.children && item.storage_locations"
          :item=item :level=1></ListCategory>
          <ListLocation v-else :item=item></ListLocation>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '@/services/api/api.service'

import ListCategory from './list-category'
import ListLocation from './list-location'
import ModalAddCategory from './modal-add-category'

export default {
  name: 'StoragesList',
  components: {
    ListCategory,
    ListLocation,
    ModalAddCategory
  },
  data: () => ({
    modalAddCategoryParent: null,
    storages: []
  }),
  created () {
    this.$nextTick(() => {
      this.$root.$on('changeModalAddCategoryParent', (id) => {
        this.changeModalAddCategoryParent(id)
      })
      this.fetchStorages()
    })
  },
  methods: {
    fetchStorages () {
      apiService.getStorages()
        .then((res) => {
          this.storages = res.data
        })
    },
    changeModalAddCategoryParent (id) {
      this.modalAddCategoryParent = id
    },
    addCategory (id) {
        this.changeModalAddCategoryParent(id)
        // Important to nextTick otherwise we don't get the time to emit the parent ID change
        this.$nextTick(() => {
          this.$bvModal.show('modalStoragesAddCategory')
        })
    }
  }
}
</script>

<style>
ul.list_storages {
  list-style-type: none;
  margin: 0;
}
</style>
