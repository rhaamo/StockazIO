<template>
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

                  <tr>
                    <td>Added:</td>
                    <td>{{ partDetailsAddedOn }}</td>
                  </tr>
                  <tr>
                    <td>Updated:</td>
                    <td>{{ partDetailsUpdatedOn }}</td>
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
                    <td>{{ dist.distributor ? dist.distributor.name : '-' }}</td>
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
                    <th />
                  </tr>
                </thead>
                <tbody v-if="partDetailsManufacturers && partDetailsManufacturers.length">
                  <tr v-for="manuf in partDetailsManufacturers" :key="manuf.id">
                    <td>{{ manuf.sku }}</td>
                    <td>{{ manuf.manufacturer ? manuf.manufacturer.name : '-' }}</td>
                    <td v-if="manuf.manufacturer">
                      <img v-if="manuf.manufacturer.logo" :src="manuf.manufacturer.logo_mini" style="max-width:100px;">
                    </td>
                  </tr>
                </tbody>
              </table>
            </b-tab>
            <b-tab title="Files">
              <table id="table-files-attachments" class="table table-sm">
                <thead>
                  <tr>
                    <th>Link</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody v-if="partDetailsAttachments && partDetailsAttachments.length">
                  <tr v-for="file in partDetailsAttachments" :key="file.id">
                    <td style="width: 10em;">
                      <a target="_blank" :href="file.file">link to file</a>
                    </td>
                    <td>{{ file.description }}</td>
                  </tr>
                </tbody>
              </table>
            </b-tab>

            <b-tab title="Stock history">
              <table id="table-stock-history" class="table table-sm">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Amount</th>
                    <th />
                  </tr>
                </thead>
                <tbody v-if="partDetailsStockHistory && partDetailsStockHistory.length">
                  <tr v-for="psh in partDetailsStockHistory" :key="psh.id">
                    <td style="width: 15em;">
                      {{ formatDate(psh.created_at) }}
                    </td>
                    <td>{{ psh.diff }}</td>
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

      <b-button v-if="canDelete" size="sm" variant="danger"
                @click="deletePart(part)"
      >
        Delete
      </b-button>

      <b-button size="sm" variant="success" @click="cancel">
        Close
      </b-button>
    </template>
  </b-modal>
</template>

<script>
import moment from 'moment'

export default {
  props: {
    part: {
      type: Object
    },
    canDelete: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    partDetailsQty () { return this.part ? this.part.stock_qty : 0 },
    partDetailsQtyMin () { return this.part ? this.part.stock_qty_min : 0 },
    partDetailsDescription () { return this.part ? this.part.description : 0 },
    partDetailsUnit () {
      if (this.part && this.part.part_unit) {
        if (this.part.part_unit.short_name) {
          return `${this.part.part_unit.name} (${this.part.part_unit.short_name})`
        } else {
          return this.part.part_unit.name
        }
      } else {
        return ''
      }
    },
    partDetailsFootprint () {
      if (this.part && this.part.footprint) {
        return this.part.footprint.name
      } else {
        return ''
      }
    },
    partDetailsStorage () {
      if (this.part && this.part.storage) {
        return this.part.storage.name
      } else {
        return ''
      }
    },
    partDetailsCategory () {
      if (this.part && this.part.category) {
        return this.part.category.name
      } else {
        return ''
      }
    },
    partDetailsId () { return this.part ? this.part.id : 0 },
    partDetailsName () { return this.part ? this.part.name : '' },
    partDetailsInternalPn () { return this.part ? this.part.internal_part_number : '' },
    partDetailsComment () { return this.part ? this.part.comment : '' },
    partDetailsProdRemarks () { return this.part ? this.part.production_remarks : '' },
    partDetailsNeedReviewClasses () { return this.part && this.part.needs_review ? 'fa icon-need-review fa-check' : 'fa icon-need-review fa-close' },
    partDetailsCanBeSoldClasses () { return this.part && this.part.can_be_sold ? 'fa icon-need-review fa-dollar' : 'fa icon-need-review fa-close' },
    partDetailsPrivate () { return this.part && this.part.private ? 'fa icon-private fa-lock' : '' },
    partDetailsCondition () { return this.part ? this.part.condition : '' },
    partDetailsParameters () { return this.part ? this.part.part_parameters_value : [] },
    partDetailsDistributors () { return this.part ? this.part.distributors_sku : [] },
    partDetailsManufacturers () { return this.part ? this.part.manufacturers_sku : [] },
    partDetailsAttachments () { return this.part ? this.part.part_attachments : [] },
    partDetailsAddedOn () {
      return this.part && this.part.created_at ? this.formatDate(this.part.created_at) : ''
    },
    partDetailsUpdatedOn () {
      return this.part && this.part.updated_at ? this.formatDate(this.part.updated_at) : ''
    },
    partDetailsStockHistory () {
      return this.part && this.part.part_stock_history ? this.part.part_stock_history : []
    }
  },
  methods: {
    formatDate (date) {
      return moment(date).format('ddd MMM D YYYY HH:mm zz')
    },
    partModalClose () {
      this.$bvModal.hide('modalManage')
      this.$emit('view-part-modal-closed')
    },
    deletePart (part) {
      this.$emit('delete-part', part)
      this.partModalClose()
    }
  }
}
</script>
