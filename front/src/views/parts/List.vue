<template>
  <div class="add_part">
    <div class="row">
      <div class="col-lg-9">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><router-link :to="{}">category</router-link></li>
          <li class="breadcrumb-item active">awoo</li>
        </ol>
      </div>
    </div>

    <div class="row">
      <div class="col-md-11 mx-auto">
        <h3>awoo</h3>
      </div>
    </div>

  </div>
</template>

<script>

export default {
  data: () => ({
  }),
  computed: {
    categoryId () {
      return this.$route.params.categoryId
    }
  },
  methods: {
  },
  created () {
  }
}
</script>
