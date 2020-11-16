<template>
  <div class="details_part">
    <div v-if="part" class="row">
      <div class="col-lg-9">
        <div class="float-left" @click="showBigQrCode(part)">
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
        <h3>
          <i :class="partDetailsPrivate" /> <router-link v-b-tooltip.hover title="Back to part details" :to="{ name: 'parts-details', params: { partId: part.id } }">
            <i class="fa fa-angle-double-left" aria-hidden="true" />
          </router-link> {{ form.name }}
        </h3>
      </div>
      <div class="col-lg-3">
        <b-button variant="link" @click.prevent="deletePart(part)">
          <i
            class="fa fa-trash-o"
            aria-hidden="true"
          />
        </b-button>
      </div>
    </div>

    <div v-if="part" class="row">
      <div class="col-md-12">
        <b-form @submit.prevent="updatePart">
          <b-row>
            <b-col>
              <b-form-group id="input-group-name" label="Name*" label-for="name">
                <b-form-input
                  id="name"
                  v-model="form.name"
                  required
                  placeholder="PIC42ACHU"
                  :state="$v.form.name.$dirty ? !$v.form.name.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-description" label="Description" label-for="description">
                <b-form-input
                  id="description"
                  v-model="form.description"
                  placeholder="A cute little mcu"
                  :state="$v.form.description.$dirty ? !$v.form.description.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-qty" label="Stock Qty*" label-for="qty">
                <b-form-input
                  id="qty"
                  v-model="form.qty"
                  required
                  type="number"
                  :state="$v.form.qty.$dirty ? !$v.form.qty.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-qty-min" label="Stock Qty min*" label-for="qty-min">
                <b-form-input
                  id="qty-min"
                  v-model="form.qty_min"
                  required
                  type="number"
                  :state="$v.form.qty_min.$dirty ? !$v.form.qty_min.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-sheet-status" label="Sheet status" label-for="sheet-status">
                <b-form-input
                  id="sheet-status"
                  v-model="form.sheet_status"
                  :state="$v.form.sheet_status.$dirty ? !$v.form.sheet_status.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-condition" label="Part condition" label-for="condition">
                <b-form-input
                  id="condition"
                  v-model="form.condition"
                  placeholder="Condition of the part"
                  :state="$v.form.condition.$dirty ? !$v.form.condition.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-production-remarks" label="Production remarks" label-for="production-remarks">
                <b-form-input
                  id="production-remarks"
                  v-model="form.production_remarks"
                  :state="$v.form.production_remarks.$dirty ? !$v.form.production_remarks.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-internal-pn" label="Internal part number" label-for="internal-pn">
                <b-form-input
                  id="internal-pn"
                  v-model="form.internal_pn"
                  :state="$v.form.internal_pn.$dirty ? !$v.form.internal_pn.$error : null"
                />
              </b-form-group>

              <b-form-group>
                <b-form-checkbox
                  id="needs-review-1"
                  v-model="form.needs_review"
                  name="needs-review-1"
                  value="true"
                  unchecked-value="false"
                  inline
                  :state="$v.form.needs_review.$dirty ? !$v.form.needs_review.$error : null"
                >
                  This sheet needs review
                </b-form-checkbox>
                <b-form-checkbox
                  id="can_be_sold-1"
                  v-model="form.can_be_sold"
                  name="can_be_sold-1"
                  value="true"
                  unchecked-value="false"
                  inline
                  :state="$v.form.can_be_sold.$dirty ? !$v.form.can_be_sold.$error : null"
                >
                  That part can be sold
                </b-form-checkbox>
                <b-form-checkbox
                  id="private-1"
                  v-model="form.private"
                  name="private-1"
                  value="true"
                  unchecked-value="false"
                  inline
                  :state="$v.form.private.$dirty ? !$v.form.private.$error : null"
                >
                  That part is private
                </b-form-checkbox>
              </b-form-group>

              <b-form-group id="input-group-part-unit" label="Part unit:" label-for="part-unit">
                <multiselect v-model="form.part_unit" :options="choicesPartUnit" placeholder="Centimeters ? Pieces ?"
                             label="text"
                />
              </b-form-group>

              <b-form-group id="input-group-category" label="Category:" label-for="category">
                <treeselect v-model="form.category" :multiple="false" :options="choicesCategory"
                            search-nested :default-expand-level="Infinity" clearable
                            :normalizer="categoriesNormalizer" no-children-text placeholder="Film resistors ? MCUS ?"
                />
              </b-form-group>

              <b-form-group id="input-group-storage_location" label="Storage location:" label-for="storage_location">
                <treeselect v-model="form.storage_location" :multiple="false" :options="choicesStorageLocation"
                            search-nested :default-expand-level="Infinity" clearable
                            :normalizer="storagesNormalizer" no-children-text placeholder="A box under the bench or some drawer ?"
                />
              </b-form-group>

              <b-form-group id="input-group-footprint" label="Footprint:" label-for="footprint">
                <multiselect v-model="form.footprint" :options="choicesFootprint" group-values="footprints"
                             group-label="category" placeholder="PDIP, BGA, SOIC, who knows" label="name"
                             track-by="id"
                />
              </b-form-group>

              <b-button type="submit" variant="primary">
                Update part
              </b-button>
            </b-col>

            <b-col>
              <b-tabs content-class="mt-3">
                <b-tab title="Parameters">
                  <div v-for="(_, i) in form.part_parameters_value" :key="i">
                    <b-row>
                      <b-col>
                        <b-form-group :id="ppvId('name', i)" label="Name*" :label-for="ppvId('name', i)">
                          <b-form-input
                            :id="ppvId('name', i)"
                            v-model="form.part_parameters_value[i].name"
                            required
                          />
                        </b-form-group>
                      </b-col>
                      <b-col>
                        <b-form-group :id="ppvId('description', i)" label="Description" :label-for="ppvId('description', i)">
                          <b-form-input
                            :id="ppvId('description', i)"
                            v-model="form.part_parameters_value[i].description"
                          />
                        </b-form-group>
                      </b-col>
                    </b-row>
                    <b-row>
                      <b-col>
                        <b-form-group :id="ppvId('value', i)" label="Value*" :label-for="ppvId('value', i)">
                          <b-form-input
                            :id="ppvId('value', i)"
                            v-model="form.part_parameters_value[i].value"
                            required
                          />
                        </b-form-group>
                      </b-col>
                      <b-col>
                        <b-form-group :id="ppvId('unit', i)" label="Unit:" :label-for="ppvId('unit', i)">
                          <multiselect v-model="form.part_parameters_value[i].unit"
                                       :options="choicesPartParametersUnit"
                                       label="text" track-by="value"
                          />
                        </b-form-group>
                      </b-col>
                    </b-row>
                    <div @click.prevent="deletePpv(i)">
                      <i class="fa fa-minus-square" aria-hidden="true" /> remove item
                    </div>
                    <hr>
                  </div>
                  <div @click.prevent="addPpv">
                    <i class="fa fa-plus-square" aria-hidden="true" /> add item
                  </div>
                </b-tab>

                <b-tab title="Manufacturers">
                  <div v-for="(_, i) in form.manufacturers_sku" :key="i">
                    <b-row>
                      <b-col>
                        <b-form-group :id="pManufId('sku', i)" label="SKU*" :label-for="pManufId('sku', i)">
                          <b-form-input
                            :id="pManufId('sku', i)"
                            v-model="form.manufacturers_sku[i].sku"
                            required
                          />
                        </b-form-group>
                      </b-col>

                      <b-col>
                        <b-form-group :id="pManufId('manufacturer', i)" label="Manufacturer*:" :label-for="pManufId('manufacturer', i)">
                          <multiselect v-model="form.manufacturers_sku[i].manufacturer" :options="choicesManufacturers"
                                       label="text" track-by="value" :allow-empty="true"
                          />
                        </b-form-group>
                      </b-col>
                    </b-row>
                    <div @click.prevent="deletePmanufs(i)">
                      <i class="fa fa-minus-square" aria-hidden="true" /> remove item
                    </div>
                    <hr>
                  </div>
                  <div @click.prevent="addPmanufs">
                    <i class="fa fa-plus-square" aria-hidden="true" /> add item
                  </div>
                </b-tab>

                <b-tab title="Distributors">
                  <div v-for="(_, i) in form.distributors_sku" :key="i">
                    <b-row>
                      <b-col>
                        <b-form-group :id="pDistId('sku', i)" label="SKU*" :label-for="pDistId('sku', i)">
                          <b-form-input
                            :id="pDistId('sku', i)"
                            v-model="form.distributors_sku[i].sku"
                            required
                          />
                        </b-form-group>
                      </b-col>

                      <b-col>
                        <b-form-group :id="pDistId('distributor', i)" label="Distributor*:" :label-for="pDistId('distributor', i)">
                          <multiselect v-model="form.distributors_sku[i].distributor" :options="choicesDistributors"
                                       label="text" track-by="value"
                          />
                        </b-form-group>
                      </b-col>
                    </b-row>
                    <div @click.prevent="deletePdist(i)">
                      <i class="fa fa-minus-square" aria-hidden="true" /> remove item
                    </div>
                    <hr>
                  </div>
                  <div @click.prevent="addPdist">
                    <i class="fa fa-plus-square" aria-hidden="true" /> add item
                  </div>
                </b-tab>
              </b-tabs>
            </b-col>
          </b-row>
        </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '../../services/api/api.service'
import QRCode from 'qrcode'
import logger from '@/logging'
import { validationMixin } from 'vuelidate'
import { required, minValue } from 'vuelidate/lib/validators'
import { mapState } from 'vuex'

export default {
  mixins: [
    validationMixin
  ],
  props: {
    category: {
      type: Object
    }
  },
  data: () => ({
    part: null,
    form: {
      name: '',
      description: '',
      qty: 1,
      qty_min: 0,
      sheet_status: '',
      needs_review: false,
      condition: '',
      can_be_sold: false,
      private: false,
      production_remarks: '',
      internal_pn: '',
      part_unit: null,
      category: null,
      storage_location: null,
      footprint: null,
      part_parameters_value: [],
      manufacturers_sku: [],
      distributors_sku: []
    }
  }),
  computed: {
    ...mapState({
      choicesPartUnit: (state) => {
        return state.preloads.part_units.map(x => { return { value: x.id, text: `${x.name} (${x.short_name})` } })
      },
      choicesCategory: state => { return [state.preloads.categories] },
      choicesStorageLocation: (state) => state.preloads.storages,
      choicesPartParametersUnit: (state) => {
        return state.preloads.parameters_unit.map(x => { return { value: x.id, text: `${x.name} (${x.prefix}${x.symbol})` } })
      },
      choicesFootprint: (state) => {
        return state.preloads.footprints.map(x => { return { category: x.name, footprints: x.footprint_set.map(y => { return { id: y.id, name: y.name } }) } })
      },
      partDetailsPrivate () { return this.form && this.form.private === 'true' ? 'fa icon-private fa-lock' : '' },
      choicesManufacturers: (state) => {
        return state.preloads.manufacturers.map(x => { return { value: x.id, text: x.name } })
      },
      choicesDistributors: (state) => {
        return state.preloads.distributors.map(x => { return { value: x.id, text: x.name } })
      }
    }),
    partId () {
      return this.$route.params.partId
    }
  },
  validations: {
    form: {
      name: {
        required
      },
      description: {
      },
      qty: {
        required,
        minValue: minValue(0)
      },
      qty_min: {
        required,
        minValue: minValue(0)
      },
      sheet_status: {
      },
      needs_review: {
      },
      condition: {
      },
      can_be_sold: {
      },
      private: {
      },
      production_remarks: {
      },
      internal_pn: {
      },
      part_unit: {
      },
      category: {
      },
      storage_location: {
      },
      footprint: {
      }
    }
  },
  watch: {
  },
  created () {
    this.fetchPart()
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
    fetchPart () {
      apiService.getPart(this.partId)
        .then((res) => {
          this.part = res.data
          this.form.name = this.part.name
          this.form.description = this.part.description
          this.form.qty = this.part.stock_qty
          this.form.qty_min = this.part.stock_qty_min
          this.form.sheet_status = this.part.status
          this.form.needs_review = this.part.needs_review
          this.form.condition = this.part.condition
          this.form.can_be_sold = this.part.can_be_sold
          this.form.private = this.part.private
          this.form.production_remarks = this.part.production_remarks
          this.form.internal_pn = this.part.internal_part_number
          this.form.part_parameters_value = this.part.part_parameters_value.map(x => {
            return {
              id: x.id,
              name: x.name,
              description: x.description,
              value: x.value,
              unit: {
                text: `${x.unit.name} (${x.unit.symbol})`,
                value: x.unit.id
              }
            }
          })
          this.form.manufacturers_sku = this.part.manufacturers_sku.map(x => {
            return {
              id: x.id,
              sku: x.sku,
              manufacturer: {
                text: x.manufacturer ? x.manufacturer.name : null,
                value: x.manufacturer ? x.manufacturer.id : null
              }
            }
          })
          this.form.distributors_sku = this.part.distributors_sku.map(x => {
            return {
              id: x.id,
              sku: x.sku,
              distributor: {
                text: x.distributor.name,
                value: x.distributor.id
              }
            }
          })

          this.form.part_unit = this.part.part_unit ? { value: this.part.part_unit.id, text: `${this.part.part_unit.name} (${this.part.part_unit.short_name})` } : null
          this.form.category = this.part.category ? this.part.category.id : null
          this.form.storage_location = this.part.storage ? this.part.storage.id : null
          this.form.footprint = this.part.footprint
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('Part/Details/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Details/Toast/Error/Title', 'Fetching part details'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Error with fetching part', err.message)
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

          apiService.deletePart(part.id)
            .then((val) => {
              this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Success/Message', 'Success'), {
                title: this.$pgettext('Part/Delete/Toast/Success/Title', 'Deleting part'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'primary',
                toaster: 'b-toaster-top-center'
              })
              this.fetchParts()
              console.log(val)
            })
            .catch((err) => {
              this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                title: this.$pgettext('Part/Delete/Toast/Error/Title', 'Deleting part'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'danger',
                toaster: 'b-toaster-top-center'
              })
              logger.default.error('Error with part deletion', err)
              this.fetchParts()
            })
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    },
    updatePart () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('Form has errors')
      }
      let datas = {
        name: this.form.name,
        description: this.form.description,
        stock_qty: this.form.qty,
        stock_qty_min: this.form.qty_min,
        status: this.form.sheet_status,
        needs_review: this.form.needs_review,
        condition: this.form.condition,
        can_be_sold: this.form.can_be_sold,
        private: this.form.private,
        production_remarks: this.form.production_remarks,
        internal_part_number: this.form.internal_pn,
        part_unit: this.form.part_unit ? this.form.part_unit.value : null,
        category: this.form.category,
        storage: this.form.storage_location,
        footprint: this.form.footprint ? this.form.footprint.id : null,
        part_parameters_value: this.form.part_parameters_value.map(x => {
          if (x.name !== '' && x.value !== '') {
            return { name: x.name, description: x.description, value: x.value, unit: x.unit ? x.unit.value : null }
          }
        }),
        manufacturers_sku: this.form.manufacturers_sku.map(x => {
          if (x.sku !== '') {
            return { sku: x.sku, manufacturer: x.manufacturer ? x.manufacturer.value : null }
          }
        }),
        distributors_sku: this.form.distributors_sku.map(x => {
          if (x.sku !== '') {
            return { sku: x.sku, distributor: x.distributor ? x.distributor.value : null }
          }
        })
      }
      apiService.updatePart(this.part.id, datas)
        .then(() => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Part/Update/Toast/Success/Title', 'Updating part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.$v.$reset()
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Update/Toast/Error/Title', 'Updating part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot update part', error.message)
        })
    },
    categoriesNormalizer: function (node) {
      return { id: node.id, label: node.name, children: node.children && node.children.length ? node.children : 0 }
    },
    storagesNormalizer: function (node) {
      let childs = (node.children || []).concat(node.storage_locations || [])
      return { id: node.id, label: node.name, children: childs && childs.length ? childs : 0 }
    },
    ppvId (func, idx) {
      return `input-ppv-${func}-${idx}`
    },
    pManufId (func, idx) {
      return `input-pmanuf-${func}-${idx}`
    },
    pDistId (func, idx) {
      return `input-pdist-${func}-${idx}`
    },
    addPpv () {
      this.form.part_parameters_value.push({
        name: '',
        description: '',
        value: '',
        unit: null
      })
    },
    deletePpv (idx) {
      this.$delete(this.form.part_parameters_value, idx)
    },
    addPmanufs () {
      this.form.manufacturers_sku.push({
        sku: '',
        manufacturer: null
      })
    },
    deletePmanufs (idx) {
      this.$delete(this.form.manufacturers_sku, idx)
    },
    addPdist () {
      this.form.distributors_sku.push({
        sku: '',
        distributor: null
      })
    },
    deletePdist (idx) {
      this.$delete(this.form.distributors_sku, idx)
    }
  }
}
</script>
