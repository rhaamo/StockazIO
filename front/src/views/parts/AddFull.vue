<template>
  <div class="add_part">
    <ViewModal
      :part="partDetails" :can-delete="false"
      @view-part-modal-closed="onPartModalClosed"
    />

    <div class="row">
      <div class="col-12">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link :to="{name: 'home'}">
              StockazIO
            </router-link>
          </li>
          <li class="breadcrumb-item active">
            Add new part
          </li>
        </ol>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-md-11 mx-auto">
        <h3>Basic parts informations</h3>
        <b-form>
          <b-row>
            <b-col>
              <b-form-group id="input-group-name" label="Name*" label-for="name">
                <b-form-input
                  id="name"
                  ref="inputname"
                  v-model="form.name"
                  required
                  placeholder="PIC42ACHU"
                  :state="$v.form.name.$dirty ? !$v.form.name.$error : null"
                  @blur="checkPartExists"
                />
                <div v-if="!$v.form.name.required" class="invalid-feedback d-block">
                  Name is required
                </div>
                <div v-if="!$v.form.name.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>
              <div v-if="partsExists && partsExists.length" class="mb-3">
                One or more parts exists with this name: <div v-for="p in partsExists" :key="p.uuid">
                  <a href="#" @click.prevent="viewPartModal(p)">{{ p.name }}</a>&nbsp;
                </div>
                <br><br>
              </div>

              <b-form-group id="input-group-description" label="Description" label-for="description">
                <b-form-input
                  id="description"
                  v-model="form.description"
                  placeholder="A cute little mcu"
                  :state="$v.form.description.$dirty ? !$v.form.description.$error : null"
                />
                <div v-if="!$v.form.description.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>
              <b-form-group id="input-group-comment" label="Comment" label-for="comment">
                <b-form-input
                  id="comment"
                  v-model="form.comment"
                  placeholder="Any comment about this part ?"
                  :state="$v.form.comment.$dirty ? !$v.form.comment.$error : null"
                />
                <div v-if="!$v.form.comment.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>

              <b-form-group id="input-group-qty" label="Stock Qty*" label-for="qty">
                <b-form-input
                  id="qty"
                  v-model="form.qty"
                  required
                  type="number"
                  inputmode="numeric"
                  :state="$v.form.qty.$dirty ? !$v.form.qty.$error : null"
                />
                <div v-if="!$v.form.qty.minValue" class="invalid-feedback d-block">
                  Qty has to be positive
                </div>
                <div v-if="!$v.form.qty.required" class="invalid-feedback d-block">
                  Qty is required
                </div>
              </b-form-group>
              <b-form-group id="input-group-qty-min" label="Stock Qty min*" label-for="qty-min">
                <b-form-input
                  id="qty-min"
                  v-model="form.qty_min"
                  required
                  type="number"
                  inputmode="numeric"
                  :state="$v.form.qty_min.$dirty ? !$v.form.qty_min.$error : null"
                />
                <div v-if="!$v.form.qty_min.minValue" class="invalid-feedback d-block">
                  Qty has to be positive
                </div>
                <div v-if="!$v.form.qty_min.required" class="invalid-feedback d-block">
                  Qty is required
                </div>
              </b-form-group>
              <b-form-group id="input-group-sheet-status" label="Sheet status" label-for="sheet-status">
                <b-form-input
                  id="sheet-status"
                  v-model="form.sheet_status"
                  :state="$v.form.sheet_status.$dirty ? !$v.form.sheet_status.$error : null"
                />
                <div v-if="!$v.form.sheet_status.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>
              <b-form-group id="input-group-condition" label="Part condition" label-for="condition">
                <b-form-input
                  id="condition"
                  v-model="form.condition"
                  placeholder="Condition of the part"
                  :state="$v.form.condition.$dirty ? !$v.form.condition.$error : null"
                />
                <div v-if="!$v.form.condition.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>
              <b-form-group id="input-group-production-remarks" label="Production remarks" label-for="production-remarks">
                <b-form-input
                  id="production-remarks"
                  v-model="form.production_remarks"
                  :state="$v.form.production_remarks.$dirty ? !$v.form.production_remarks.$error : null"
                />
                <div v-if="!$v.form.production_remarks.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>
              <b-form-group id="input-group-internal-pn" label="Internal part number" label-for="internal-pn">
                <b-form-input
                  id="internal-pn"
                  v-model="form.internal_pn"
                  :state="$v.form.internal_pn.$dirty ? !$v.form.internal_pn.$error : null"
                />
                <div v-if="!$v.form.internal_pn.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
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
                <vue-multiselect
                  v-model="form.part_unit" :options="choicesPartUnit" placeholder="Centimeters ? Pieces ?"
                  label="text" track-by="value"
                />
              </b-form-group>

              <b-form-group id="input-group-category" label="Category:" label-for="category">
                <vue-treeselect
                  v-model="form.category" :multiple="false" :options="choicesCategory"
                  search-nested :default-expand-level="Infinity" clearable
                  :normalizer="categoriesNormalizer" no-children-text placeholder="Film resistors ? MCUS ?"
                />
              </b-form-group>

              <b-form-group id="input-group-storage_location" label="Storage location:" label-for="storage_location">
                <vue-treeselect
                  v-model="form.storage_location" :multiple="false" :options="choicesStorageLocation"
                  search-nested :default-expand-level="Infinity" clearable
                  :normalizer="storagesNormalizer" no-children-text placeholder="A box under the bench or some drawer ?"
                  :disable-branch-nodes="true"
                />
              </b-form-group>

              <b-form-group id="input-group-footprint" label="Footprint:" label-for="footprint">
                <vue-multiselect
                  v-model="form.footprint" :options="choicesFootprint" group-values="footprints"
                  group-label="category" placeholder="PDIP, BGA, SOIC, who knows" label="name"
                  track-by="id"
                />
              </b-form-group>

              <b-button type="submit" variant="primary" @click.prevent="addPart('continue')">
                Save and view
              </b-button>
            &nbsp;&nbsp;
              <b-button type="submit" variant="info" @click.prevent="addPart('add_new')">
                Save and add another
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
                          <div v-if="!$v.form.part_parameters_value.$each[i].name.required" class="invalid-feedback d-block">
                            Name is required
                          </div>
                          <div v-if="!$v.form.part_parameters_value.$each[i].name.maxLength" class="invalid-feedback d-block">
                            Maximum length is 255
                          </div>
                        </b-form-group>
                      </b-col>
                      <b-col>
                        <b-form-group :id="ppvId('description', i)" label="Description" :label-for="ppvId('description', i)">
                          <b-form-input
                            :id="ppvId('description', i)"
                            v-model="form.part_parameters_value[i].description"
                          />
                          <div v-if="!$v.form.part_parameters_value.$each[i].description.maxLength" class="invalid-feedback d-block">
                            Maximum length is 255
                          </div>
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
                          <div v-if="!$v.form.part_parameters_value.$each[i].value.required" class="invalid-feedback d-block">
                            Value is required
                          </div>
                          <div v-if="!$v.form.part_parameters_value.$each[i].value.maxLength" class="invalid-feedback d-block">
                            Maximum length is 255
                          </div>
                        </b-form-group>
                      </b-col>
                      <b-col>
                        <b-form-group :id="ppvId('unit', i)" label="Unit:" :label-for="ppvId('unit', i)">
                          <vue-multiselect
                            v-model="form.part_parameters_value[i].unit"
                            :options="choicesPartParametersUnit"
                            label="text" track-by="value"
                          />
                        </b-form-group>
                      </b-col>
                    </b-row>
                    <BtnDeleteInline
                      size="sm" btn-variant-main="danger" btn-variant-ok="success"
                      btn-variant-cancel="danger" btn-main-text="remove item"
                      btn-main-text-disabled="Confirm ?" btn-ok-text="Yes"
                      btn-cancel-text="No" @action-confirmed="deletePpv(i)"
                    />
                    <hr>
                  </div>

                  <b-button size="sm" variant="info" @click.prevent="addPpv">
                    add item
                  </b-button>

                  <template v-if="choicesPartParametersPresets">
                    <b-row class="mt-4">
                      <b-col cols="3">
                        Select a preset to apply
                      </b-col>
                      <b-col cols="5">
                        <b-form-select v-model="selectedPartParametersPreset" :options="choicesPartParametersPresets" size="sm" />
                      </b-col>
                      <b-col cols="3">
                        <BtnDeleteInline
                          size="sm" btn-variant-main="info" btn-variant-ok="success"
                          btn-variant-cancel="info" btn-main-text="apply"
                          btn-main-text-disabled="Confirm ?" btn-ok-text="Yes"
                          btn-cancel-text="No" @action-confirmed="applyPartParametersPreset"
                        />
                      </b-col>
                    </b-row>
                  </template>
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
                            @blur="partManufacturersManufacturerChanged(i)"
                          />
                          <div v-if="!$v.form.manufacturers_sku.$each[i].sku.required" class="invalid-feedback d-block">
                            SKU is required
                          </div>
                          <div v-if="!$v.form.manufacturers_sku.$each[i].sku.maxLength" class="invalid-feedback d-block">
                            Maximum length is 255
                          </div>
                        </b-form-group>
                      </b-col>

                      <b-col>
                        <b-form-group :id="pManufId('manufacturer', i)" label="Manufacturer:" :label-for="pManufId('manufacturer', i)">
                          <vue-multiselect
                            v-model="form.manufacturers_sku[i].manufacturer" :options="choicesManufacturers"
                            label="text" track-by="value" @input="partManufacturersManufacturerChanged(i)"
                          />
                        </b-form-group>
                      </b-col>
                    </b-row>

                    <b-form-group :id="pManufId('datasheet_url', i)" label="Datasheet URL" :label-for="pManufId('datasheet_url', i)">
                      <b-form-input
                        :id="pManufId('datasheet_url', i)"
                        v-model="form.manufacturers_sku[i].datasheet_url"
                      />
                    </b-form-group>

                    <BtnDeleteInline
                      size="sm" btn-variant-main="danger" btn-variant-ok="success"
                      btn-variant-cancel="danger" btn-main-text="remove item"
                      btn-main-text-disabled="Confirm ?" btn-ok-text="Yes"
                      btn-cancel-text="No" @action-confirmed="deletePmanufs(i)"
                    />
                    <hr>
                  </div>
                  <b-button size="sm" variant="info" @click.prevent="addPmanufs">
                    add item
                  </b-button>
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
                            @blur="partDistributorsDistributorChanged(i)"
                          />
                          <div v-if="!$v.form.distributors_sku.$each[i].sku.required" class="invalid-feedback d-block">
                            SKU is required
                          </div>
                          <div v-if="!$v.form.distributors_sku.$each[i].sku.maxLength" class="invalid-feedback d-block">
                            Maximum length is 255
                          </div>
                        </b-form-group>
                      </b-col>

                      <b-col>
                        <b-form-group :id="pDistId('distributor', i)" label="Distributor*:" :label-for="pDistId('distributor', i)">
                          <vue-multiselect
                            v-model="form.distributors_sku[i].distributor" :options="choicesDistributors"
                            label="text" track-by="value"
                            @input="partDistributorsDistributorChanged(i)"
                          />
                          <div v-if="!$v.form.distributors_sku.$each[i].distributor.required" class="invalid-feedback d-block">
                            Distributor is required
                          </div>
                        </b-form-group>
                      </b-col>
                    </b-row>

                    <b-form-group :id="pDistId('datasheet_url', i)" label="Datasheet URL" :label-for="pDistId('datasheet_url', i)">
                      <b-form-input
                        :id="pDistId('datasheet_url', i)"
                        v-model="form.distributors_sku[i].datasheet_url"
                      />
                    </b-form-group>

                    <BtnDeleteInline
                      size="sm" btn-variant-main="danger" btn-variant-ok="success"
                      btn-variant-cancel="danger" btn-main-text="remove item"
                      btn-main-text-disabled="Confirm ?" btn-ok-text="Yes"
                      btn-cancel-text="No" @action-confirmed="deletePdist(i)"
                    />
                    <hr>
                  </div>
                  <b-button size="sm" variant="info" @click.prevent="addPdist">
                    add item
                  </b-button>
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
import logger from '@/logging'
import apiService from '@/services/api/api.service'
import ViewModal from '@/components/parts/view_modal'
import BtnDeleteInline from '@/components/btn_delete_inline'
import utils from '@/utils'

import { mapState } from 'vuex'
import { validationMixin } from 'vuelidate'
import { required, minValue, maxLength } from 'vuelidate/lib/validators'

export default {
  components: {
    ViewModal,
    BtnDeleteInline
  },
  mixins: [
    validationMixin
  ],
  data: () => ({
    selectedPartParametersPreset: {},
    form: {
      name: '',
      description: '',
      comment: '',
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
    },
    partsExists: [],
    partDetails: null
  }),
  validations: {
    form: {
      name: {
        required,
        maxLength: maxLength(255)
      },
      description: {
        maxLength: maxLength(255)
      },
      comment: {
        maxLength: maxLength(255)
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
        maxLength: maxLength(255)
      },
      needs_review: {
      },
      condition: {
        maxLength: maxLength(255)
      },
      can_be_sold: {
      },
      private: {
      },
      production_remarks: {
        maxLength: maxLength(255)
      },
      internal_pn: {
        maxLength: maxLength(255)
      },
      part_unit: {
      },
      category: {
      },
      storage_location: {
      },
      footprint: {
      },
      part_parameters_value: {
        $each: {
          name: { required, maxLength: maxLength(255) },
          description: { maxLength: maxLength(255) },
          value: { required, maxLength: maxLength(255) },
          unit: {}
        }
      },
      manufacturers_sku: {
        $each: {
          sku: { required, maxLength: maxLength(255) }
        }
      },
      distributors_sku: {
        $each: {
          sku: { required, maxLength: maxLength(255) },
          distributor: { required }
        }
      }
    }
  },
  computed: {
    ...mapState({
      choicesPartUnit: (state) => {
        return state.preloads.part_units.map(x => { return { value: x.id, text: `${x.name} (${x.short_name})` } })
      },
      choicesCategory: state => { return [state.preloads.categories] },
      choicesStorageLocation: (state) => {
        return state.preloads.storages.filter(utils.removeStorageCatWithoutLocs)
      },
      choicesPartParametersUnit: (state) => {
        return state.preloads.parameters_unit.map(x => { return { value: x.id, text: `${x.name} (${x.symbol})` } })
      },
      choicesFootprint: (state) => {
        return state.preloads.footprints.map(x => { return { category: x.name, footprints: x.footprint_set.map(y => { return { id: y.id, name: y.name } }) } })
      },
      choicesManufacturers: (state) => {
        return state.preloads.manufacturers.map(x => { return { value: x.id, text: x.name, datasheet_url: x.datasheet_url } })
      },
      choicesDistributors: (state) => {
        return state.preloads.distributors.map(x => { return { value: x.id, text: x.name, datasheet_url: x.datasheet_url } })
      },
      choicesPartParametersPresets: (state) => {
        return state.preloads.partParametersPresets.map(x => { return { value: x, text: x.name } })
      }
    })
  },
  methods: {
    addPart: function (mode) {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('Form has errors')
        this.$bvToast.toast(this.$pgettext('Part/Add/Toast/Error/Message', 'Form has errors, please check all fields.'), {
          title: this.$pgettext('Part/Add/Toast/Error/Title', 'Adding part'),
          autoHideDelay: 5000,
          appendToast: true,
          variant: 'danger',
          toaster: 'b-toaster-top-center'
        })
        return
      }
      let datas = {
        name: this.form.name,
        description: this.form.description,
        comment: this.form.comment,
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
            return { sku: x.sku, manufacturer: x.manufacturer ? x.manufacturer.value : null, datasheet_url: x.datasheet_url }
          }
        }),
        distributors_sku: this.form.distributors_sku.map(x => {
          if (x.sku !== '') {
            return { sku: x.sku, distributor: x.distributor ? x.distributor.value : null, datasheet_url: x.datasheet_url }
          }
        })
      }
      console.log('submitting', datas)
      apiService.createPart(datas)
        .then((resp) => {
          this.$bvToast.toast(this.$pgettext('Part/Add/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Part/Add/Toast/Success/Title', 'Adding part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.$store.commit('incrementCategoryPartsCount', { nodeId: this.form.category })
          if (mode === 'add_new') {
            this.clearForm()
            this.$refs.inputname.focus()
          } else {
            // 'continue'
            this.$router.push({ name: 'parts-details', params: { partId: resp.data.id } })
          }
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('Part/Add/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Add/Toast/Error/Title', 'Adding part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot save part', error.message)
        })
    },
    categoriesNormalizer: function (node) {
      return { id: node.id, label: node.name, children: node.children && node.children.length ? node.children : 0 }
    },
    storagesNormalizer: function (node) {
      let childs = (node.children || []).concat(node.storage_locations || [])
      let id = node.uuid ? node.id : `cat_${node.id}`
      return { id: id, label: node.name, children: childs && childs.length ? childs : 0 }
    },
    clearForm: function () {
      this.form.name = ''
      this.form.description = ''
      this.form.comment = ''
      this.form.qty = 1
      this.form.qty_min = 0
      this.form.sheet_status = ''
      this.form.condition = ''
      this.form.internal_pn = ''
      this.form.needs_review = false
      this.form.footprint = null
      this.form.production_remarks = ''
      this.form.part_parameters_value = []
      this.form.manufacturers_sku = []
      this.form.distributors_sku = []
      this.$v.$reset()
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
        manufacturer: null,
        datasheet_url: ''
      })
    },
    deletePmanufs (idx) {
      this.$delete(this.form.manufacturers_sku, idx)
    },
    addPdist () {
      this.form.distributors_sku.push({
        sku: '',
        distributor: null,
        datasheet_url: ''
      })
    },
    deletePdist (idx) {
      this.$delete(this.form.distributors_sku, idx)
    },
    checkPartExists (event) {
      if (this.form.name === '') { return }
      apiService.partsAutocompleteQuick(this.form.name)
        .then((res) => {
          this.partsExists = res.data
        })
        .catch((err) => {
          logger.default.error('Got an error from the autocompleter', err.message)
          this.partsExists = []
        })
    },
    viewPartModal (part) {
      this.partDetails = part
      this.$bvModal.show('modalManage')
    },
    onPartModalClosed () {
      this.partDetails = null
    },
    replaceDSUrlPlaceholders (index, url, sku) {
      if (url.includes('{sku}') || url.includes('{sku_lower}') || url.includes('{sku_upper}')) {
        url = url.replaceAll('{sku}', sku)
        url = url.replaceAll('{sku_lower}', sku.toLowerCase())
        url = url.replaceAll('{sku_upper}', sku.toUpperCase())
        return url
      }
      return url
    },
    partManufacturersManufacturerChanged (index) {
      let manufacturer = this.form.manufacturers_sku[index].manufacturer
      if (!manufacturer) { return }

      let sku = this.form.manufacturers_sku[index].sku

      if (sku) {
        if (manufacturer.datasheet_url) {
          this.form.manufacturers_sku[index].datasheet_url = this.replaceDSUrlPlaceholders(index, manufacturer.datasheet_url, sku)
        }
      } else {
        this.form.manufacturers_sku[index].datasheet_url = manufacturer.datasheet_url
      }
    },
    partDistributorsDistributorChanged (index) {
      let distributor = this.form.distributors_sku[index].distributor
      if (!distributor) { return }

      let sku = this.form.distributors_sku[index].sku

      if (sku) {
        if (distributor.datasheet_url) {
          this.form.distributors_sku[index].datasheet_url = this.replaceDSUrlPlaceholders(index, distributor.datasheet_url, sku)
        }
      } else {
        this.form.distributors_sku[index].datasheet_url = distributor.datasheet_url
      }
    },
    applyPartParametersPreset () {
      if (this.selectedPartParametersPreset) {
        this.selectedPartParametersPreset.part_parameters_presets.forEach(item => {
          this.form.part_parameters_value.push({
            name: item.name,
            description: item.description,
            value: '',
            unit: item.unit ? { value: item.unit.id, text: `${item.unit.name} (${item.unit.symbol})` } : null
          })
        })
      }
    }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style src="@riophae/vue-treeselect/dist/vue-treeselect.css"></style>
