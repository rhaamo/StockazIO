<template>
  <div class="list_part_unit">
    <b-row>
      <b-col md="9">
        <b-breadcrumb>
          <b-breadcrumb-item :to="{name: 'orders-importer'}">
            Orders Importer
          </b-breadcrumb-item>
          <b-breadcrumb-item>
            {{ order.order_number }}
          </b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
    </b-row>

    <b-form @submit.prevent="updateOrder">
      <b-row>
        <b-col md="1">
          <b>Ordered:</b> {{ formatDate(order.date) }}<br>
          <b>Number:</b> {{ order.order_number }}<br>
          <b>Items:</b> {{ rows }}<br>
          <b>From:</b> {{ order.vendor }}<br>
          <b>Import:</b> {{ importStateText(order.import_state) }}<br>
          <br>
          <b-button variant="primary" @click.prevent="rematchCategories">
            Rematch categories
          </b-button>
          <br><br>
          <b-button type="submit" variant="info">
            Save
          </b-button>
        </b-col>

        <b-col md="10">
          <b-table
            id="tableOrderItems"
            :items="order.item_set"
            :fields="fields"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            responsive="sm"
            striped
            show-empty
          >
            <template #cell(category)="data">
              <treeselect v-model="data.item.category" :multiple="false" :options="choicesCategory"
                          search-nested :default-expand-level="Infinity" clearable
                          :normalizer="categoriesNormalizer" no-children-text placeholder="Category to import in"
              />
            </template>

            <template #cell(ignore)="data">
              <b-form-checkbox
                :id="ignoreIdCbox(data.item.id)"
                v-model="data.item.ignore"
                name="ignore"
                :value="true"
                :unchecked-value="false"
                inline
              />
            </template>
          </b-table>
        </b-col>
      </b-row>
    </b-form>
  </div>
</template>

<script>
import apiService from '@/services/api/api.service'
import logger from '@/logging'
import { mapState } from 'vuex'

import moment from 'moment'

export default {
  mixins: [
  ],
  props: {
  },
  data: () => ({
    order: {},
    fields: [
      { key: 'mfr_part_number', label: 'Manufacturer PN' },
      { key: 'description', label: 'Description' },
      { key: 'manufacturer', label: 'Manufacturer' },
      { key: 'quantity', label: 'Quantity' },
      { key: 'vendor_part_number', label: 'Vendor PN' },
      { key: 'category', label: 'Category', tdClass: 'category' },
      { key: 'ignore', label: 'Ignore from import' }
    ],
    sortBy: 'name',
    sortDesc: false
  }),
  validations: {
  },
  computed: {
    ...mapState({
      serverSettings: state => state.server.settings,
      choicesCategory: state => { return [state.preloads.categories] }
    }),
    rows () {
      return this.order && this.order.item_set ? this.order.item_set.length : 0
    },
    orderId () {
      return this.$route.params.id
    }
  },
  watch: {
  },
  created () {
    this.fetchOrder(this.orderId)
  },
  methods: {
    ignoreIdCbox (id) {
      return `ignore-${id}`
    },
    formatDate (date) {
      return moment(date).format('ddd DD MMM YYYY')
    },
    fetchOrder (orderId) {
      apiService.getOrderImporter(orderId)
        .then((val) => {
          this.order = val.data
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('OrdersImporterDetails/Fetch/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('OrdersImporterDetails/Fetch/Toast/Error/Title', 'Fetching order'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Error getting order', err)
        })
    },
    importStateText (state) {
      let states = {
        0: 'Unknown',
        1: 'Fetched',
        2: 'Imported',
        99: 'Error'
      }
      return states[state]
    },
    categoriesNormalizer: function (node) {
      return { id: node.id, label: node.name, children: node.children && node.children.length ? node.children : 0 }
    },
    updateOrder () {
      console.log('nya~')
    },
    rematchCategories () {
      console.log('aaa')
    }
  }
}
</script>

<style>
table#tableOrderItems td.category {
  width: 20em;
}
</style>
<style src="@riophae/vue-treeselect/dist/vue-treeselect.css"></style>
