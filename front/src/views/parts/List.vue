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
                <div @click="showBigQrCode(part)">
                  <qrcode
                    :id="qrcodeId(part.id)"
                    v-b-tooltip.hover
                    :value="qrCodePart(part.uuid)"
                    :options="{ scale: 1 }"
                    title="click to show bigger QrCode"
                    :data-uuid="part.uuid"
                    :data-name="part.name"
                    data-toggle="modal"
                    data-target="#modalQrCode"
                  />
                </div>
              </td>
              <td>
                <a href="#" @click.prevent="viewPartModal(part)">{{ part.name }}</a>
                <template v-if="part.description">
                  <br>{{ part.description }}
                </template>
              </td>
              <td>{{ part.storage ? part.storage.name : '-' }}</td>
              <td>{{ part.stock_qty }}</td>
              <td>{{ part.stock_qty_min }}</td>
              <td>{{ part.part_unit ? part.part_unit.name : '-' }}</td>
              <td>
                <span
                  v-b-tooltip.hover
                  :title="part.footprint ? part.footprint.description : ''"
                >
                  {{ part.footprint ? part.footprint.name : '-' }}
                </span>
              </td>
              <td>
                <b-button variant="link" @click.prevent="editPart(part)">
                  <i
                    class="fa fa-pencil-square-o"
                    aria-hidden="true"
                  />
                </b-button>
                &nbsp;
                <b-button variant="link" @click.prevent="deletePart(part)">
                  <i
                    class="fa fa-trash-o"
                    aria-hidden="true"
                  />
                </b-button>
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
import QRCode from 'qrcode'
import logger from '@/logging'

export default {
  props: {
    category: {
      type: Object
    }
  },
  data: () => ({
    parts: [],
    page: 0, // TODO/FIXME no pagination yet
    search_query: '', // TODO/FIXME no search yet
    partDetails: null
  }),
  computed: {
    categoryId () {
      return this.$route.params.categoryId
    },
    sortBy () {
      return (this.$route.params.sort === 'name' || this.$route.params.sort === '-name') ? 'name' : null
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
    fetchParts () {
      if (this.categoryId) {
        apiService.getPartsByCategory(this.categoryId)
          .then((res) => {
            this.parts = res.data
          })
      } else {
        apiService.getParts()
          .then((res) => {
            this.parts = res.data
          })
      }
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
                this.fetchParts()
              })
              .catch((err) => {
                this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                  title: this.$pgettext('Part/Delete/Toast/Error/Title', 'Deleting part'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'danger'
                })
                logger.default.error('Error with part deletion', err)
                this.fetchParts()
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
