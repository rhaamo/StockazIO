<template>
  <div class="storages_list">
    <ModalManageCategory
      :parent="modalManageCategoryParent" :mode="modalManageCategoryMode"
      :item="modalManageCategoryItem" @modal-storages-manage-category-closed="fetchStorages" @modal-storages-manage-category-saved="fetchStorages"
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
            <b-button
              pill size="sm" variant="light"
              title="Add storage category on root level"
              @click.prevent="addCategory(null)"
            >
              <i class="fa fa-plus-square-o" aria-hidden="true" /> Add root category
            </b-button>
          </li>
        </ul>
        <template v-for="item in stateStorages">
          <ListCategory
            v-if="item.children && item.storage_locations"
            :key="item.id" :item="item" :level="1"
          />
          <ListLocation v-else :key="item.uuid" :item="item" />
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '@/services/api/api.service'
import logger from '@/logging'

import ListCategory from './list-category'
import ListLocation from './list-location'
import ModalManageCategory from './modal-manage-category'
import { mapState } from 'vuex'

export default {
  name: 'StoragesList',
  components: {
    ListCategory,
    ListLocation,
    ModalManageCategory
  },
  data: () => ({
    modalManageCategoryParent: null,
    modalManageCategoryMode: 'add',
    modalManageCategoryItem: null
  }),
  computed: {
    ...mapState({
      stateStorages: (state) => state.preloads.storages
    })
  },
  created () {
    this.$nextTick(() => {
      this.$root.$on('changeModalManageCategoryParent', (id) => {
        this.changeModalManageCategoryParent(id)
      })
      this.$root.$on('reloadStorageCategoriesTree', (id) => {
        this.fetchStorages()
      })
      this.$root.$on('changeModalManageCategoryMode', (mode) => {
        this.changeModalManageCategoryMode(mode)
      })
      this.$root.$on('modalStoragesCategoryUpdateSetItem', (item) => {
        this.modalManageCategoryItem = item
      })
      this.fetchStorages(true)
    })
  },
  methods: {
    fetchStorages (init = false) {
      if (!init) {
        apiService.getStorages()
          .then((res) => {
            this.$store.commit('setStorages', res.data)
            logger.default.info('Storages reloaded')
          })
      }
      // Reset field
      this.modalManageCategoryItem = null
      this.modalManageCategoryMode = 'add'
    },
    changeModalManageCategoryParent (id) {
      this.modalManageCategoryParent = id
    },
    changeModalManageCategoryMode (mode) {
      this.modalManageCategoryMode = mode
    },
    addCategory (id) {
      this.changeModalManageCategoryParent(id)
      this.modalManageCategoryMode = 'add'
      // Important to nextTick otherwise we don't get the time to emit the parent ID change
      this.$nextTick(() => {
        this.$bvModal.show('modalStoragesManageCategory')
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
