<template>
  <div class="add_part">
    <div class="row">
      <div class="col-lg-9">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link :to="{name: 'home'}">
              StockazIO
            </router-link>
          </li>
          <li class="breadcrumb-item active">
            Quick add new part
          </li>
        </ol>
      </div>
    </div>

    <div class="row">
      <div class="col-md-11 mx-auto">
        <h3>Basic parts informations</h3>
        <b-form @submit.prevent="addPart">
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
                             label="text" track-by="value"
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
                Add part
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
                  coin
                </b-tab>

                <b-tab title="Distributors">
                  coin
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

import { mapState } from 'vuex'
import { validationMixin } from 'vuelidate'
import { required, minValue } from 'vuelidate/lib/validators'

export default {
  mixins: [
    validationMixin
  ],
  data: () => ({
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
      part_parameters_value: []
    }
  }),
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
      }
    })
  },
  methods: {
    addPart: function () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('Form has errors')
        return
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
        })
      }
      console.log('submitting', datas)
      apiService.createPart(datas)
        .then(() => {
          this.$bvToast.toast(this.$pgettext('Part/Add/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Part/Add/Toast/Success/Title', 'Adding part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary'
          })
          this.clearForm()
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('Part/Add/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Add/Toast/Error/Title', 'Adding part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Cannot save part', error.message)
        })
    },
    categoriesNormalizer: function (node) {
      return { id: node.id, label: node.name, children: node.children && node.children.length ? node.children : 0 }
    },
    storagesNormalizer: function (node) {
      let childs = (node.children || []).concat(node.storage_locations || [])
      return { id: node.id, label: node.name, children: childs && childs.length ? childs : 0 }
    },
    clearForm: function () {
      this.form.name = ''
      this.form.description = ''
      this.form.qty = 1
      this.form.qty_min = 0
      this.form.sheet_status = ''
      this.form.condition = ''
      this.form.internal_pn = ''
      this.form.needs_review = false
      this.form.footprint = null
      this.form.production_remarks = ''
      this.form.part_parameters_value = []
      this.$v.$reset()
    },
    ppvId (func, idx) {
      return `input-ppv-${func}-${idx}`
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
    }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style src="@riophae/vue-treeselect/dist/vue-treeselect.css"></style>
