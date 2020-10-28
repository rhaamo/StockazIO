<template>
  <div class="add_part">
    <div class="row">
      <div class="col-lg-9">
        <ol class="breadcrumb">
          <template v-if="category">
            <li class="breadcrumb-item">
              Parts by category
            </li>
            <li class="breadcrumb-item active">
              <router-link :to="{ name: 'parts-category-list', params: { categoryId: category.id, category: category } }">
                {{ category.name }}
              </router-link>
            </li>
          </template>
          <template v-else>
            <li class="breadcrumb-item active">
              <router-link :to="{ name: 'parts-list' }">
                All parts
              </router-link>
            </li>
          </template>
        </ol>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 mx-auto">
        <table class="table table-condensed table-stripped">
          <thead>
            <tr>
              <th width="25">
                <i class="fa fa-qrcode" />
              </th>
              <th>
                <a href="">Name</a>
                <i
                  v-if="sortBy == 'name'"
                  class="fa fa-sort-alpha-asc"
                  aria-hidden="true"
                />
                <i
                  v-else
                  class="fa fa-sort-alpha-desc"
                  aria-hidden="true"
                />
              </th>
              <th>Storage</th>
              <th>Stock</th>
              <th>Min</th>
              <th>Unit</th>
              <th>Footprint</th>
              <th>
                <i
                  class="fa fa-tasks"
                  aria-hidden="true"
                />
              </th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="part in parts"
              :key="part.id"
            >
              <td>
                <div
                  :id="qrcodeId(part.id)"
                  title="click to show bigger QrCode"
                  :data-uuid="part.uuid"
                  :data-name="part.name"
                  data-toggle="modal"
                  data-target="#modalQrCode"
                />
                <div
                  :id="qrcodeId(part.id, 'big')"
                  style="display: none; position: absolute; left: 6em; margin-top: -5em;"
                />
              </td>
              <td>
                <a
                  title="View part modal"
                  href=""
                  :data-name="part.name"
                  data-edit-url=""
                  data-delete-url=""
                  data-page-url=""
                  :data-id="part.id"
                  data-toggle="modal"
                  data-target="#modalPart"
                >{{ part.name }}</a>
                <template v-if="part.description">
                  <br>{{ part.description }}
                </template>
              </td>
              <td>{{ part.storage || '-' }}</td>
              <td>{{ part.stock_qty }}</td>
              <td>{{ part.stock_qty_min }}</td>
              <td>{{ part.part_unit || '-' }}</td>
              <td>{{ part.footprint || '-' }}</td>
              <td>
                <a href=""><i
                  class="fa fa-pencil-square-o"
                  aria-hidden="true"
                /></a>
                &nbsp;
                <a href=""><i
                  class="fa fa-trash-o"
                  aria-hidden="true"
                /></a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '../../services/api/api.service'

export default {
  props: {
    category: {
      type: Object
    }
  },
  data: () => ({
    parts: [],
    page: 0, // TODO/FIXME no pagination yet
    search_query: '' // TODO/FIXME no search yet
  }),
  computed: {
    categoryId () {
      return this.$route.params.categoryId
    },
    sortBy () {
      return (this.$route.params.sort === 'name' || this.$route.params.sort === '-name') ? 'name' : null
    }
  },
  watch: {
    'categoryId': function () {
      this.fetchParts()
    }
  },
  created () {
    this.fetchParts()
  },
  methods: {
    qrcodeId (id, size) {
      return size ? `qrcode-${id}-${size}` : `qrcode-${id}`
    },
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
  }
}
</script>
