<template>
  <div class="add_part">
    <div class="row">
      <div class="col-lg-9">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><router-link :to="{name: 'home'}">StockazIO</router-link></li>
          <li class="breadcrumb-item active">Informations</li>
        </ol>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-2">
        <table class="table table-striped table-condensed">
          <tr>
            <td>Parts:</td>
            <td>{{ parts_count }}</td>
          </tr>
          <tr>
            <td>Categories:</td>
            <td>{{ categories_count }}</td>
          </tr>
          <tr>
            <td>App Version:</td>
            <td>{{ version }}</td>
          </tr>
        </table>
      </div>
    </div>

  </div>
</template>

<script>
import apiService from '../../services/api/api.service'

export default {
  data () {
    return {
      parts_count: 0,
      categories_count: 0,
      version: '0.0'
    }
  },
  mounted () {
    apiService.getInformations()
      .then((data) => {
        this.parts_count = data.data.parts_count
        this.categories_count = data.data.categories_count
        this.version = data.data.version
      })
  }
}
</script>
