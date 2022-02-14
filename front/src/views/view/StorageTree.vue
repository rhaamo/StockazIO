<template>
  <div class="storages_list">
    <modalLabelGenerator
      :items="modalLabelGeneratorItems" @modal-label-generator-closed="labelGeneratorClosed"
    />

    <div class="row">
      <div class="col-8">
        <ol class="breadcrumb">
          <li class="breadcrumb-item active">
            <router-link :to="{ name: 'view-storage-tree' }">
              Storage tree
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
            :readonly="true"
          />
          <ListLocation
            v-else :key="item.uuid" :item="item"
            :readonly="true"
          />
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import ListCategory from '@/views/storages/list-category'
import ListLocation from '@/views/storages/list-location'
import modalLabelGenerator from '@/components/labels/modal-label-generator.vue'

import { mapState } from 'vuex'

export default {
  name: 'StorageTree',
  components: {
    ListCategory,
    ListLocation,
    modalLabelGenerator
  },
  data: () => ({
    modalLabelGeneratorItems: []
  }),
  computed: {
    ...mapState({
      stateStorages: (state) => state.preloads.storages
    })
  },
  created () {
    this.$nextTick(() => {
      this.$root.$on('modalLabelGeneratorSetItem', (item) => {
        this.modalLabelGeneratorItems = [item]
      })
    })
  },
  methods: {
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
      this.$bvModal.show('modalLabelGenerator')
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
