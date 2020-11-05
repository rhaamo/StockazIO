<template>
  <div class="list_part_unit">
    <b-row>
      <b-col md="9">
        <b-breadcrumb>
          <b-breadcrumb-item :to="{name: 'orders-importer'}">
            Orders Importer
          </b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
    </b-row>

    <b-row>
      <b-col md="1">
        <b-button
          variant="primary"
          :to="{'name': 'orders-importer-category-matcher'}"
        >
          Edit category matchers
        </b-button>
      </b-col>

      <b-col md="6">
        <b-table
          id="tableOrders"
          :items="orders"
          :fields="fields"
          :sort-by.sync="sortBy"
          :sort-desc.sync="sortDesc"
          :per-page="perPage"
          :current-page="currentPage"
          responsive="sm"
          striped
        >
          <template #cell(date)="data">
            <router-link v-b-tooltip.hover title="Edit order details" :to="{name: 'orders-importer-details', params: {id: data.item.id}}">
              {{ data.item.date }}
            </router-link>
          </template>
          <template #cell(order_number)="data">
            <router-link v-b-tooltip.hover title="Edit order details" :to="{name: 'orders-importer-details', params: {id: data.item.id}}">
              {{ data.item.order_number }}
            </router-link>
          </template>

          <template #cell(items)="data">
            {{ data.item.items.length }}
          </template>

          <template #cell(import_state)="data">
            {{ importStateText(data.item.import_state) }}
          </template>

          <template #cell(actions)="data">
            <b-button v-if="data.item.import_state == 1"
                      variant="info"
                      @click.prevent="importOrder(data.item)"
            >
              import
            </b-button>
          </template>
        </b-table>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import apiService from '@/services/api/api.service'
import logger from '@/logging'
import { mapState } from 'vuex'

export default {
  mixins: [
  ],
  props: {
  },
  data: () => ({
    orders: [],
    currentPage: 1,
    fields: [
      { key: 'date', label: 'Date', sortable: true },
      { key: 'order_number', label: 'Order Number' },
      { key: 'items', label: 'Items qty' },
      { key: 'status', label: 'Status (vendor)', sortable: true },
      { key: 'vendor', label: 'Vendor', sortable: true },
      { key: 'import_state', label: 'Import state', sortable: true },
      { key: 'actions', label: 'Actions' }
    ],
    sortBy: 'name',
    sortDesc: false
  }),
  validations: {
  },
  computed: {
    ...mapState({
      serverSettings: state => state.server.settings
    }),
    rows () {
      return this.orders.length
    },
    perPage () {
      return this.serverSettings.pagination.ORDERS_IMPORTER || 10
    }
  },
  watch: {
  },
  created () {
    this.fetchOrders()
  },
  methods: {
    importStateText (state) {
      let states = {
        0: 'Unknown',
        1: 'Fetched',
        2: 'Imported',
        99: 'Error'
      }
      return states[state]
    },
    fetchOrders () {
      apiService.getOrdersImporter()
        .then((val) => {
          this.orders = val.data
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('OrdersImporter/Fetch/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('OrdersImporter/Fetch/Toast/Error/Title', 'Fetching orders'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Error getting orders', err)
        })
    },
    importOrder (item) {
      this.$bvModal.msgBoxConfirm(`Take care to edit it first to match categories or ignore parts.`, {
        title: 'Are you sure you want to import that order ?',
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: 'YES',
        cancelTitle: 'NO',
        footerClass: 'p-2',
        hideHeaderClose: false,
        centered: true
      })
        .then((value) => {
          if (value === false) { return }
          if (value === true) {
            apiService.importOrderToInventory(item.id)
              .then(() => {
                this.$bvToast.toast(this.$pgettext('ImportOrderToInventory/Add/Toast/Success/Message', 'Success'), {
                  title: this.$pgettext('ImportOrderToInventory/Add/Toast/Success/Title', 'Import to inventory'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'primary'
                })
                this.fetchOrders()
              })
              .catch((error) => {
                this.$bvToast.toast(this.$pgettext('ImportOrderToInventory/Add/Toast/Error/Message', 'An error occured, please try again later'), {
                  title: this.$pgettext('ImportOrderToInventory/Add/Toast/Error/Title', 'Import to inventory'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'danger'
                })
                logger.default.error('Cannot import to inventory', error.message)
              })
          }
        })
        .catch((err) => {
          logger.default.error('Error with import modal', err)
        })
    }
  }
}
</script>
