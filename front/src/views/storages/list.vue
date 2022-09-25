<template>
  <div class="storages_list">
    <ModalManageCategory
      :parent="modalManageCategoryParent" :mode="modalManageCategoryMode"
      :item="modalManageCategoryItem" @modal-storages-manage-category-closed="fetchStorages" @modal-storages-manage-category-saved="fetchStorages"
    />
    <ModalManageLocation
      :parent="modalManageLocationParent" :mode="modalManageLocationMode"
      :item="modalManageLocationItem" @modal-storages-manage-location-closed="fetchStorages" @modal-storages-manage-location-saved="fetchStorages"
    />
    <modalLabelGenerator
      :items="modalLabelGeneratorItems" :kind="modalLabelGeneratorKind" @modal-label-generator-closed="labelGeneratorClosed"
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
            <router-link
              to="#"
              title="Add storage category on root level"
              @click.native.prevent="addCategory(null)"
            >
              <i class="fa fa-plus-square-o" aria-hidden="true" /> Add root category
            </router-link>

            &nbsp;&nbsp;&nbsp;

            <router-link
              to="#"
              title="Bulk-generate labels"
              @click.native.prevent="bulkGenerateLabels()"
            >
              <i class="fa fa-qrcode" aria-hidden="true" /> Bulk-generate labels
            </router-link>
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
import ModalManageLocation from './modal-manage-location'
import modalLabelGenerator from '@/components/labels/modal-label-generator.vue'

import { mapState } from 'vuex'

export default {
  name: 'StoragesList',
  components: {
    ListCategory,
    ListLocation,
    ModalManageCategory,
    ModalManageLocation,
    modalLabelGenerator
  },
  data: () => ({
    modalManageCategoryParent: null,
    modalManageCategoryMode: 'add',
    modalManageCategoryItem: null,
    modalManageLocationParent: null,
    modalManageLocationMode: 'add',
    modalManageLocationItem: null,
    modalLabelGeneratorItems: [],
    modalLabelGeneratorKind: "storage"
  }),
  computed: {
    ...mapState({
      stateStorages: (state) => state.preloads.storages
    })
  },
  created () {
    this.$nextTick(() => {
      this.$root.$on('changeModalManageCategoryParent', (id) => {
        this.modalManageCategoryParent = id
      })
      this.$root.$on('reloadStorageCategoriesTree', (id) => {
        this.fetchStorages()
      })
      this.$root.$on('changeModalManageCategoryMode', (mode) => {
        this.modalManageCategoryMode = mode
      })
      this.$root.$on('modalStoragesCategoryUpdateSetItem', (item) => {
        this.modalManageCategoryItem = item
      })
      //
      this.$root.$on('changeModalManageLocationParent', (id) => {
        this.modalManageLocationParent = id
      })
      this.$root.$on('changeModalManageLocationMode', (mode) => {
        this.modalManageLocationMode = mode
      })
      this.$root.$on('modalStoragesLocationUpdateSetItem', (item) => {
        this.modalManageLocationItem = item
      })
      this.$root.$on('modalLabelGeneratorSetItem', (item) => {
        this.modalLabelGeneratorItems = [item]
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
            this.$store.commit('setLastUpdate', { item: 'storages', value: new Date() })
            logger.default.info('Storages reloaded')
          })
      }
      // Reset field
      this.modalManageCategoryItem = null
      this.modalManageCategoryMode = 'add'
      this.modalManageLocationItem = null
      this.modalManageLocationMode = 'add'
    },
    addCategory (id) {
      this.modalManageCategoryParent = id
      this.modalManageCategoryMode = 'add'
      // Important to nextTick otherwise we don't get the time to emit the parent ID change
      this.$nextTick(() => {
        this.$bvModal.show('modalStoragesManageCategory')
      })
    },
    labelGeneratorClosed () {
      this.modalLabelGeneratorItems = []
    },
    bulkGenerateLabels () {
      let slocs = []
      const cb = (e) => {
        if (e.category) {
          slocs.push(e)
        } else {
          e.storage_locations.forEach(cb)
          e.children.forEach(cb)
        }
      }
      this.stateStorages.forEach(cb)
      this.modalLabelGeneratorItems = slocs
      // yet another magic tick
      this.$nextTick(() => {
        this.$bvModal.show('modalLabelGenerator')
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
