<template>
  <div class="storages_list">
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
        <template v-for="item in storages">
          <ListCategory v-if="item.children && item.storage_locations" :item=item :level=1></ListCategory>
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

export default {
  name: 'StoragesList',
  components: {
    ListCategory,
    ListLocation
  },
  data: () => ({
    storages: []
  }),
  created () {
    this.$nextTick(() => {
      this.fetchStorages()
    })
  },
  methods: {
    fetchStorages () {
      apiService.getStorages()
        .then((res) => {
          this.storages = res.data
        })
    }
  }
}
</script>

<style>
</style>
