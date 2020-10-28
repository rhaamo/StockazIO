<template>
  <div class="add_part">
    <div class="row">
      <div class="col-lg-9">
        <ol class="breadcrumb">
          <template v-if="category">
            <li class="breadcrumb-item">Parts by category</li>
            <li class="breadcrumb-item active"><router-link :to="{ name: 'parts-category-list', params: { categoryId: category.id, category: category } }">{{ category.name }}</router-link></li>
          </template>
          <template v-else>
            <li class="breadcrumb-item active"><router-link :to="{ name: 'parts-list' }">All parts</router-link></li>
          </template>
        </ol>
      </div>
    </div>

    <div class="row">
      <div class="col-md-11 mx-auto">
        <h3>awoo</h3>
        <ul v-if='parts && parts.length'>
          <li v-for='part in parts' :key='part.id'>{{ part.id }} - {{ part.name }}</li>
        </ul>
      </div>
    </div>

  </div>
</template>

<script>
import apiService from '../../services/api/api.service'

export default {
  props: ['category'],
  data: () => ({
    parts: []
  }),
  computed: {
    categoryId () {
      return this.$route.params.categoryId
    }
  },
  methods: {
    fetchParts () {
      if (this.categoryId) {
        apiService.getPartsByCategory(this.categoryId)
          .then((res) => {
            this.parts = res.data
            console.log('cat', res.data)
          })
      } else {
        apiService.getParts()
          .then((res) => {
            this.parts = res.data
            console.log('no cat', res.data)
          })
      }
    }
  },
  created () {
    this.fetchParts()
  },
  watch: {
    'categoryId': function () {
      this.fetchParts()
    }
  }
}
</script>
