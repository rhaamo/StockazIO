<template>
  <div class="add_part">
    <b-modal id="modalManage" ref="modalManage"
             size="xl" @cancel="partModalClose" @close="partModalClose"
             @hidden="partModalClose"
    >
      <template #modal-header="{ close }">
        <h5 id="modalPartTitle">
          <i title="Private" :class="partDetailsPrivate" /> <span class="modal-title">{{ partDetailsName }}</span>
        </h5>
        <button type="button" class="close" data-dismiss="modal"
                aria-label="Close" @click="close()"
        >
          <span aria-hidden="true">&times;</span>
        </button>
      </template>
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <div class="row">
              <div class="col-md-12">
                <div class="row no-gutters">
                  <div class="col-md-3">
                    <b>Qty:</b> <span class="qty">{{ partDetailsQty }}</span>
                  </div>
                  <div class="col-md-3">
                    <b>Min:</b> <span class="qty-min">{{ partDetailsQtyMin }}</span>
                  </div>
                  <div class="col-md-6">
                    <b>Unit:</b> <span class="unit">{{ partDetailsUnit }}</span>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12">
                    <div class="description">
                      {{ partDetailsDescription }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-lg-12">
                <table class="table table-sm">
                  <tbody>
                    <tr>
                      <td>Footprint:</td>
                      <td><span class="footprint">{{ partDetailsFootprint }}</span></td>
                    </tr>
                    <tr>
                      <td>Storage:</td>
                      <td><span class="storage">{{ partDetailsStorage }}</span></td>
                    </tr>
                    <tr>
                      <td>Category:</td>
                      <td><span class="category">{{ partDetailsCategory }}</span></td>
                    </tr>
                    <tr>
                      <td>Internal part number:</td>
                      <td><span class="internal-pn">{{ partDetailsInternalPn }}</span></td>
                    </tr>
                    <tr>
                      <td>Comment:</td>
                      <td><span class="comment">{{ partDetailsComment }}</span></td>
                    </tr>
                    <tr>
                      <td>Production remarks:</td>
                      <td><span class="production-remarks">{{ partDetailsProdRemarks }}</span></td>
                    </tr>
                    <tr>
                      <td>Sheet Need review:</td>
                      <td><i title="Shet review needed" :class="partDetailsNeedReviewClasses" /> <span class="need-review" /><span class="sheet-status" /></td>
                    </tr>
                    <tr>
                      <td>Part Condition:</td>
                      <td><span class="condition">{{ partDetailsCondition }}</span></td>
                    </tr>
                    <tr>
                      <td>Can be sold:</td>
                      <td><i title="Can be sold" :class="partDetailsCanBeSoldClasses" /> <span class="can-be-sold" /></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="col-md-6">
            <b-tabs content-class="mt-3">
              <b-tab title="Parameters">
                <table id="table-parameters" class="table table-sm">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Description</th>
                      <th>Value</th>
                      <th>Unit</th>
                    </tr>
                  </thead>
                  <tbody v-if="partDetailsParameters && partDetailsParameters.length">
                    <tr v-for="pu in partDetailsParameters" :key="pu.id">
                      <td>{{ pu.name }}</td>
                      <td>{{ pu.description }}</td>
                      <td>{{ pu.value }}</td>
                      <td>{{ pu.unit ? pu.unit.name : '' }}</td>
                    </tr>
                  </tbody>
                </table>
              </b-tab>
              <b-tab title="Distributors">
                <table id="table-distributors" class="table table-sm">
                  <thead>
                    <tr>
                      <th>SKU</th>
                      <th>Distributor</th>
                    </tr>
                  </thead>
                  <tbody v-if="partDetailsDistributors && partDetailsDistributors.length">
                    <tr v-for="dist in partDetailsDistributors" :key="dist.id">
                      <td>{{ dist.sku }}</td>
                      <td>{{ dist.distributor.name }}</td>
                    </tr>
                  </tbody>
                </table>
              </b-tab>
              <b-tab title="Manufacturers">
                <table id="table-manufacturers" class="table table-sm">
                  <thead>
                    <tr>
                      <th>SKU</th>
                      <th>Manufacturer</th>
                    </tr>
                  </thead>
                  <tbody v-if="partDetailsManufacturers && partDetailsManufacturers.length">
                    <tr v-for="manuf in partDetailsManufacturers" :key="manuf.id">
                      <td>{{ manuf.sku }}</td>
                      <td>{{ manuf.manufacturer.name }}</td>
                    </tr>
                  </tbody>
                </table>
              </b-tab>
            </b-tabs>
          </div>
        </div>
      </div>
      <template #modal-footer="{ cancel }">
        <b-button size="sm" variant="outline-primary" :to="{ name: 'parts-details', params: { partId: partDetailsId } }">
          Show full details
        </b-button>

        <b-button size="sm" variant="danger" @click="deletePart(partDetails)">
          Delete
        </b-button>

        <b-button size="sm" variant="success" @click="cancel">
          Close
        </b-button>
      </template>
    </b-modal>

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
            <template v-if="data.item.description">
              <br>{{ data.item.description }}
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

export default {
  props: {
    category: {
      type: Object
    }
  },
  data: () => ({
    parts: [],
    currentPage: 1,
    search_query: '', // TODO/FIXME no search yet
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
    popoverStockQtyShow: false
  }),
  computed: {
    ...mapState({
      serverSettings: state => state.server.settings
    }),
    perPage () {
      return this.serverSettings.pagination.PARTS || 10
    },
    categoryId () {
      return this.$route.params.categoryId
    },
    partDetailsQty () { return this.partDetails ? this.partDetails.stock_qty : 0 },
    partDetailsQtyMin () { return this.partDetails ? this.partDetails.stock_qty_min : 0 },
    partDetailsDescription () { return this.partDetails ? this.partDetails.description : 0 },
    partDetailsUnit () {
      if (this.partDetails && this.partDetails.part_unit) {
        if (this.partDetails.part_unit.short_name) {
          return `${this.partDetails.part_unit.name} (${this.partDetails.part_unit.short_name})`
        } else {
          return this.partDetails.part_unit.name
        }
      } else {
        return ''
      }
    },
    partDetailsFootprint () {
      if (this.partDetails && this.partDetails.footprint) {
        return this.partDetails.footprint.name
      } else {
        return ''
      }
    },
    partDetailsStorage () {
      if (this.partDetails && this.partDetails.storage) {
        return this.partDetails.storage.name
      } else {
        return ''
      }
    },
    partDetailsCategory () {
      if (this.partDetails && this.partDetails.category) {
        return this.partDetails.category.name
      } else {
        return ''
      }
    },
    partDetailsId () { return this.partDetails ? this.partDetails.id : 0 },
    partDetailsName () { return this.partDetails ? this.partDetails.name : '' },
    partDetailsInternalPn () { return this.partDetails ? this.partDetails.internal_part_number : '' },
    partDetailsComment () { return this.partDetails ? this.partDetails.comment : '' },
    partDetailsProdRemarks () { return this.partDetails ? this.partDetails.production_remarks : '' },
    partDetailsNeedReviewClasses () { return this.partDetails && this.partDetails.needs_review ? 'fa icon-need-review fa-check' : 'fa icon-need-review fa-close' },
    partDetailsCanBeSoldClasses () { return this.partDetails && this.partDetails.can_be_sold ? 'fa icon-need-review fa-dollar' : 'fa icon-need-review fa-close' },
    partDetailsPrivate () { return this.partDetails && this.partDetails.private ? 'fa icon-private fa-lock' : '' },
    partDetailsCondition () { return this.partDetails ? this.partDetails.condition : '' },
    partDetailsParameters () { return this.partDetails ? this.partDetails.part_parameters_value : [] },
    partDetailsDistributors () { return this.partDetails ? this.partDetails.distributors_sku : [] },
    partDetailsManufacturers () { return this.partDetails ? this.partDetails.manufacturers_sku : [] }
  },
  watch: {
    'categoryId': function () {
      this.fetchParts(1, null)
      this.categoryChanged()
    }
  },
  created () {
    this.$nextTick(() => {
      this.fetchParts(1, null)
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
      this.fetchParts(1, ctx)
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
    fetchParts (page, sorting) {
      let params = {
        page: page,
        size: this.perPage
      }
      if (this.categoryId !== null) {
        params.category_id = this.categoryId
      }
      if (sorting) {
        params.ordering = sorting.sortDesc ? `-${sorting.sortBy}` : sorting.sortBy
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
    partModalClose () {
      this.$bvModal.hide('modalManage')
      this.partDetails = null
    }
  }
}
</script>
