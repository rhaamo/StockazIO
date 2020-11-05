<template>
  <div class="add_part">
    <ViewModal :part="partDetails" :can-delete="true" @delete-part="deletePart"
               @view-part-modal-closed="onPartModalClosed"
    />

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
      <div class="col-lg-1">
        <multiselect v-model="filter.footprint" :options="choicesFootprint"
                     group-values="footprints" group-label="category" placeholder="Filter footprint"
                     label="name" track-by="id" @input="filterFootprintChanged"
        />
      </div>
      <div class="col-lg-1">
        <treeselect v-model="filter.storage" :multiple="false"
                    :options="choicesStorageLocation" search-nested :default-expand-level="Infinity"
                    clearable :normalizer="storagesNormalizer" no-children-text
                    placeholder="Filter storage" @input="filterStorageChanged"
        />
      </div>
      <div class="col-lg-1">
        <b-form-checkbox
          v-model="filter.qty"
          value="qty"
          :unchecked-value="null"
          inline
        >
          Only out of stock
        </b-form-checkbox>
        <br>
        <b-form-checkbox
          v-model="filter.qty"
          value="qtyMin"
          :unchecked-value="null"
          inline
        >
          Only qty < min
        </b-form-checkbox>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 mx-auto">
        <b-table id="tablePartsList" ref="tablePartsList" :items="parts"
                 :fields="fields"
                 :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" per-page="0"
                 :current-page="currentPage" :busy.sync="busy"
                 condensed striped
                 sort-icon-left
                 show-empty
                 primary-key="uuid"
                 :no-local-sorting="true"
                 @sort-changed="sortTableChanged"
        >
          <template #cell(qrcode)="data">
            <div @click="showBigQrCode(data.item)">
              <qrcode
                :id="qrcodeId(data.item.id)"
                v-b-tooltip.hover
                :value="qrCodePart(data.item.uuid)"
                :options="{ scale: 1, color: {dark: '#000000', light:'#0000'} }"
                title="click to show bigger QrCode"
                :data-uuid="data.item.uuid"
                :data-name="data.item.name"
                data-toggle="modal"
                data-target="#modalQrCode"
              />
            </div>
          </template>

          <template #cell(name)="data">
            <a href="#" @click.prevent="viewPartModal(data.item)">{{ data.item.name }}</a>
            <br>
            <template v-if="data.item.description">
              {{ data.item.category ? data.item.category.name : 'No category' }}: {{ data.item.description }}
            </template>
            <template v-else>
              {{ data.item.category ? data.item.category.name : 'No category' }}
            </template>
          </template>

          <template #cell(storage)="data">
            {{ data.item.storage && data.item.storage.name ? data.item.storage.name : '-' }}
          </template>

          <template #cell(part_unit)="data">
            {{ data.item.part_unit && data.item.part_unit.name ? data.item.part_unit.name : '-' }}
          </template>

          <template #cell(stock_qty)="data">
            <span v-if="(data.item.stock_qty < data.item.stock_qty_min) || data.item.stock_qty == 0" :id="popoverStockQtyClass(data.item.id)"
                  class="qtyMinWarning"
            >{{ data.item.stock_qty }}
              <i v-b-tooltip.hover class="fa fa-circle"
                 aria-hidden="true"
                 title="Current stock is below minimum stock quantity or exhausted"
              />
            </span>
            <span v-else :id="popoverStockQtyClass(data.item.id)" v-b-tooltip.hover
                  title="click to change qty"
            >{{ data.item.stock_qty }}</span>

            <b-popover
              :target="popoverStockQtyClass(data.item.id)"
              triggers="click"
              placement="auto"
              container="tablePartsList"
            >
              <template #title>
                Change stock qty
              </template>

              <div align="center">
                <b-form-spinbutton v-model="data.item.stock_qty" min="0" />
                <br>
                <b-button size="sm" type="submit" variant="primary"
                          @click.prevent="popoverQtyUpdatePart(data.item.id, data.item.stock_qty)"
                >
                  update
                </b-button>
              </div>
            </b-popover>
          </template>

          <template #cell(stock_qty_min)="data">
            <span :id="popoverStockQtyMinClass(data.item.id)">{{ data.item.stock_qty_min }}</span>

            <b-popover
              :target="popoverStockQtyMinClass(data.item.id)"
              triggers="click"
              placement="auto"
              container="tablePartsList"
            >
              <template #title>
                Change stock min qty
              </template>

              <div align="center">
                <b-form-spinbutton v-model="data.item.stock_qty_min" min="0" />
                <br>
                <b-button size="sm" type="submit" variant="primary"
                          @click.prevent="popoverQtyMinUpdatePart(data.item.id, data.item.stock_qty_min)"
                >
                  update
                </b-button>
              </div>
            </b-popover>
          </template>

          <template #cell(footprint)="data">
            <span
              v-b-tooltip.hover
              :title="data.item.footprint ? data.item.footprint.description : ''"
            >
              {{ data.item.footprint ? data.item.footprint.name : '-' }}
            </span>
          </template>

          <template #cell(actions)="data">
            <b-button variant="link" :to="{ name: 'parts-edit', params: { partId: data.item.id } }">
              <i
                class="fa fa-pencil-square-o"
                aria-hidden="true"
              />
            </b-button>
                &nbsp;
            <b-button variant="link" @click.prevent="deletePart(data.item)">
              <i
                class="fa fa-trash-o"
                aria-hidden="true"
              />
            </b-button>
          </template>
        </b-table>
      </div>
    </div>

    <b-row>
      <b-col md="6" offset-md="1">
        <b-pagination
          v-model="currentPage"
          :total-rows="partsCount"
          :per-page="perPage"
          aria-controls="tablePartsList"
          @change="pageChanged"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import apiService from '../../services/api/api.service'
import QRCode from 'qrcode'
import logger from '@/logging'
import { mapState } from 'vuex'
import ViewModal from '@/components/parts/view_modal'

export default {
  components: {
    ViewModal
  },
  props: {
    category: {
      type: Object
    }
  },
  data: () => ({
    parts: [],
    currentPage: 1,
    partDetails: null,
    partsCount: 0,
    fields: [
      { key: 'qrcode', label: 'QrCode', tdClass: 'qrCode' },
      { key: 'name', label: 'Name', sortable: true },
      { key: 'storage', label: 'Storage', sortable: true },
      { key: 'stock_qty', label: 'Stock', sortable: true },
      { key: 'stock_qty_min', label: 'Min', sortable: true },
      { key: 'part_unit', label: 'Unit', sortable: true },
      { key: 'footprint', label: 'Footprint', sortable: true },
      { key: 'actions', label: 'Actions' }
    ],
    sortBy: 'name',
    sortDesc: false,
    busy: false,
    popoverStockQtyShow: false,
    filter: {
      footprint: null,
      storage: null,
      qty: null
    }
  }),
  computed: {
    ...mapState({
      serverSettings: state => state.server.settings,
      choicesStorageLocation: (state) => state.preloads.storages,
      choicesFootprint: (state) => {
        return state.preloads.footprints.map(x => { return { category: x.name, footprints: x.footprint_set.map(y => { return { id: y.id, name: y.name } }) } })
      }
    }),
    perPage () {
      return this.serverSettings.pagination.PARTS || 10
    },
    categoryId () {
      return this.$route.params.categoryId
    },
    storageId () {
      return this.$route.query.storage
    },
    storageUuid () {
      return this.$route.query.storage_uuid
    },
    searchQuery () {
      return this.$route.query.q
    }
  },
  watch: {
    'categoryId': function () {
      this.fetchParts(1, null)
      this.categoryChanged()
    },
    'searchQuery': function () {
      this.fetchParts(1, { search: this.searchQuery })
    },
    'filter.qty': function () {
      if (this.filter.qty === 'qty') {
        this.fetchParts(1, { qtyType: 'qty' })
      } else if (this.filter.qty === 'qtyMin') {
        this.fetchParts(1, { qtyType: 'qtyMin' })
      } else {
        this.fetchParts(1, null)
      }
    },
    'storageUuid': function () {
      this.fetchParts(1, { storage_uuid: this.storageUuid })
    }
  },
  created () {
    this.$nextTick(() => {
      if (this.searchQuery) {
        this.fetchParts(1, { search: this.searchQuery })
      } else if (this.storageUuid) {
        this.fetchParts(1, { storage_uuid: this.storageUuid })
      } else {
        this.fetchParts(1, null)
      }
      this.categoryChanged()
    })
  },
  methods: {
    popoverQtyUpdatePart (id, qty) {
      apiService.updatePartialPart(id, { stock_qty: qty })
        .then(() => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Part/Update/Toast/Success/Title', 'Updating part qty'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary'
          })
          // eslint-disable-next-line vue/custom-event-name-casing
          this.$root.$emit('bv::hide::popover', this.popoverStockQtyClass(id))
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Update/Toast/Error/Title', 'Updating part qty'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Cannot update part qty', error.message)
        })
    },
    popoverStockQtyClass (id) {
      return `popover-stock-qty-${id}`
    },
    popoverQtyMinUpdatePart (id, qty) {
      apiService.updatePartialPart(id, { stock_qty_min: qty })
        .then(() => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Part/Update/Toast/Success/Title', 'Updating min part qty'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary'
          })
          // eslint-disable-next-line vue/custom-event-name-casing
          this.$root.$emit('bv::hide::popover', this.popoverStockQtyMinClass(id))
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Update/Toast/Error/Title', 'Updating min part qty'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Cannot update min part qty', error.message)
        })
    },
    popoverStockQtyMinClass (id) {
      return `popover-stock-qty-min-${id}`
    },
    categoryChanged () {
      this.$store.commit('setCurrentCategory', { id: this.categoryId })
    },
    pageChanged (page) {
      this.fetchParts(page, null)
    },
    sortTableChanged (ctx) {
      // When changing the sorting order, reset the pagination to page 1
      let opts = ctx.sortDesc ? `-${ctx.sortBy}` : ctx.sortBy
      this.fetchParts(1, opts)
    },
    qrcodeId (id, size) {
      return size ? `qrcode-${id}-${size}` : `qrcode-${id}`
    },
    qrCodePart (uuid) {
      return `stockazio://part/${uuid}`
    },
    async showBigQrCode (part) {
      let qrCodeDataUrl = await QRCode.toDataURL(this.qrCodePart(part.uuid), { width: 300 }).then((url) => { return url })

      const h = this.$createElement
      const titleVNode = h('div', { domProps: { innerHTML: `QrCode for: ${part.name}` } })
      const messageVNode = h('div', { domProps: { style: 'text-align: center;' } }, [
        h('img', { domProps: { src: qrCodeDataUrl } }),
        h('div', {}, ['The content of the QrCode is:', h('br'), h('code', { class: ['qrCodeText'] }, [this.qrCodePart(part.uuid)])])
      ])
      this.$bvModal.msgBoxOk([messageVNode], {
        title: [titleVNode],
        buttonSize: 'sm',
        centered: true,
        size: 'lg'
      })
    },
    fetchParts (page, opts) {
      let params = {
        page: page,
        size: this.perPage,
        ...opts
      }
      if (this.categoryId !== null) {
        params.category_id = this.categoryId
      }
      if (this.searchQuery) {
        params.search = this.searchQuery
      }
      if (this.storageId && !this.filter.storage) {
        params.storage_id = this.storageId
      }
      if (this.storageUuid && !this.filter.storage) {
        params.storage_uuid = this.storageUuid
      }
      if (this.filter.footprint) {
        params.footprint_id = this.filter.footprint.id
      }
      if (this.filter.qty === 'qty') {
        params.qtyType = 'qty'
      } else if (this.filter.qty === 'qtyMin') {
        params.qtyType = 'qtyMin'
      }

      this.busy = true
      apiService.getParts(params)
        .then((res) => {
          this.parts = res.data.results
          this.partsCount = res.data.count
          this.busy = false
          // eslint-disable-next-line vue/custom-event-name-casing
          this.$root.$emit('bv::refresh::table', 'tablePartsList')
        })
    },
    deletePart (part) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the part '${part.name}' ?`, {
        title: 'Plase Confirm',
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
            apiService.deletePart(part.id)
              .then((val) => {
                this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Success/Message', 'Success'), {
                  title: this.$pgettext('Part/Delete/Toast/Success/Title', 'Deleting part'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'primary'
                })
                this.fetchParts(1, null)
              })
              .catch((err) => {
                this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                  title: this.$pgettext('Part/Delete/Toast/Error/Title', 'Deleting part'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'danger'
                })
                logger.default.error('Error with part deletion', err)
                this.fetchParts(1, null)
              })
          }
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    },
    viewPartModal (part) {
      apiService.getPart(part.id)
        .then((val) => {
          this.partDetails = val.data
          this.$bvModal.show('modalManage')
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('Part/ShowModal/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/ShowModal/Toast/Error/Title', 'Part details'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Error fetching part', err)
          this.partDetails = null
        })
    },
    storagesNormalizer: function (node) {
      let childs = (node.children || []).concat(node.storage_locations || [])
      return { id: node.id, label: node.name, children: childs && childs.length ? childs : 0 }
    },
    filterFootprintChanged (value, id) {
      if (value) {
        this.fetchParts(1, { footprint_id: value.id })
      } else {
        this.fetchParts(1, null)
      }
    },
    filterStorageChanged (value, id) {
      if (value) {
        this.fetchParts(1, { storage_id: value })
      } else {
        this.fetchParts(1, null)
      }
    },
    onPartModalClosed () {
      this.partDetails = null
    }
  }
}
</script>
