<template>
  <div class="list_part_unit">
    <b-row>
      <b-col cols="12">
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
        <b-col xl="1" cols="2">
          <b>Ordered:</b> {{ formatDate(order.date) }}<br>
          <b>Number:</b> {{ order.order_number }}<br>
          <b>Items:</b> {{ rows }}<br>
          <b>From:</b> {{ order.vendor }}<br>
          <multiselect
            v-model="order.vendor_db" :options="choicesDistributors"
            label="text" track-by="value" placeholder="match known one"
          /><br>
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
            :items="order.items"
            :fields="fields"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            responsive="sm"
            striped
            show-empty
          >
            <template #cell(category)="data">
              <treeselect
                v-model="data.item.category" :multiple="false" :options="choicesCategory"
                search-nested :default-expand-level="Infinity" clearable
                :normalizer="categoriesNormalizer" no-children-text placeholder="Category to import in"
              />
            </template>

            <template #cell(manufacturer)="data">
              {{ data.item.manufacturer }}<br>
              <multiselect
                v-model="data.item.manufacturer_db" :options="choicesManufacturers"
                label="text" track-by="value" placeholder="match known one"
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
      choicesCategory: state => { return [state.preloads.categories] },
      choicesDistributors: (state) => {
        return state.preloads.distributors.map(x => { return { value: x.id, text: x.name } })
      },
      choicesManufacturers: (state) => {
        return state.preloads.manufacturers.map(x => { return { value: x.id, text: x.name } })
      }
    }),
    rows () {
      return this.order && this.order.items ? this.order.items.length : 0
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
          this.order = {
            id: val.data.id,
            date: val.data.date,
            order_number: val.data.order_number,
            status: val.data.status,
            vendor: val.data.vendor,
            vendor_db: val.data.vendor_db ? { value: val.data.vendor_db.id, text: val.data.vendor_db.name } : null,
            import_state: val.data.import_state,
            items: val.data.items.map(y => {
              return {
                id: y.id,
                vendor_part_number: y.vendor_part_number,
                mfr_part_number: y.mfr_part_number,
                manufacturer: y.manufacturer,
                description: y.description,
                quantity: y.quantity,
                order: y.order,
                ignore: y.ignore,
                category: y.category ? y.category.id : null,
                manufacturer_db: y.manufacturer_db ? { value: y.manufacturer_db.id, text: y.manufacturer_db.name } : null
              }
            })
          }
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('OrdersImporterDetails/Fetch/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('OrdersImporterDetails/Fetch/Toast/Error/Title', 'Fetching order'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
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
      let datas = this.order
      datas.vendor_db = datas.vendor_db ? datas.vendor_db.value : null
      datas.items = datas.items.map(x => {
        return {
          ...x,
          category: x.category ? x.category : null,
          manufacturer_db: x.manufacturer_db ? x.manufacturer_db.value : null
        }
      })
      apiService.updateOrderImporter(this.order.id, datas)
        .then(() => {
          this.$bvToast.toast(this.$pgettext('OrdersImporterDetails/Add/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('OrdersImporterDetails/Add/Toast/Success/Title', 'Updating order'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.fetchOrder(this.orderId)
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('OrdersImporterDetails/Add/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('OrdersImporterDetails/Add/Toast/Error/Title', 'Updating order'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot rematch items', error.message)
        })
    },
    rematchCategories () {
      apiService.rematchOrderItems()
        .then(() => {
          this.$bvToast.toast(this.$pgettext('CategoryMatchers/Add/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('CategoryMatchers/Add/Toast/Success/Title', 'Updating categories'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.fetchOrder(this.orderId)
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('CategoryMatchers/Add/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('CategoryMatchers/Add/Toast/Error/Title', 'Updating categories'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot rematch items', error.message)
        })
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
