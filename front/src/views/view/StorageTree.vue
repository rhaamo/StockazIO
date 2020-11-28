<template>
  <div class="add_part">
    <div class="row">
      <div class="col-lg-9">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link :to="{name: 'home'}">
              StockazIO
            </router-link>
          </li>
          <li class="breadcrumb-item active">
            Storage Tree
          </li>
        </ol>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-9">
        <ul>
          <li v-for="storage in storages" :key="storage.id">
            <node :node="storage" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import node from './StorageTreeNode'

export default {
  components: {
    node
  },
  data () {
    return {
    }
  },
  computed: {
    ...mapState({
      storages: (state) => { return state.preloads.storages }
    })
  },
  mounted () {
  }
}
</script>
