<template>
  <div class="add_part">
    <div class="row">
      <div class="col-lg-9">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><router-link :to="{name: 'home'}">StockazIO</router-link></li>
          <li class="breadcrumb-item active">Quick add new part</li>
        </ol>
      </div>
    </div>

    <div class="row">
      <div class="col-md-11 mx-auto">
        <h3>Basic parts informations</h3>
        <b-form @submit="addPart">
          <b-row>
            <b-col>
              <b-form-group id="input-group-name" label="Name*" label-for="name">
                <b-form-input
                  id="name"
                  v-model="form.name"
                  required
                  placeholder="PIC42ACHU"
                ></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-description" label="Description" label-for="description">
                <b-form-input
                  id="description"
                  v-model="form.description"
                  placeholder="A cute little mcu"
                ></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-qty" label="Stock Qty*" label-for="qty">
                <b-form-input
                  id="qty"
                  v-model="form.qty"
                  required
                  type='number'
                ></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-qty-min" label="Stock Qty min*" label-for="qty-min">
                <b-form-input
                  id="qty-min"
                  v-model="form.qty_min"
                  required
                  type='number'
                ></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-sheet-status" label="Sheet status" label-for="sheet-status">
                <b-form-input
                  id="sheet-status"
                  v-model="form.sheet_status"
                ></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-condition" label="Part condition" label-for="condition">
                <b-form-input
                  id="condition"
                  v-model="form.condition"
                  placeholder="Condition of the part"
                ></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-internal-pn" label="Internal part number" label-for="internal-pn">
                <b-form-input
                  id="internal-pn"
                  v-model="form.internal_pn"
                ></b-form-input>
              </b-form-group>

              <b-form-group>
              <b-form-checkbox
                id="needs-review-1"
                v-model="form.needs_review"
                name="needs-review-1"
                value="true"
                unchecked-value="false"
                inline
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
              >
                That part is private
              </b-form-checkbox>
              </b-form-group>
            </b-col>

            <b-col>
              <b-form-group id="input-group-part-unit" label="Part unit:" label-for="part-unit">
                <multiselect v-model="form.part_unit" :options="choicesPartUnit" placeholder="Select an unit" label="text" track-by="value"></multiselect>
              </b-form-group>
              <b-form-group id="input-group-category" label="Category:" label-for="category">
                <b-form-select
                  id="category"
                  v-model="form.category"
                  :options="choicesCategory"
                  required
                ></b-form-select>
              </b-form-group>
              <b-form-group id="input-group-storage_location" label="Storage location:" label-for="storage_location">
                <b-form-select
                  id="storage_location"
                  v-model="form.storage_location"
                  :options="choicesStorageLocation"
                  required
                ></b-form-select>
              </b-form-group>
              <b-form-group id="input-group-footprint" label="Footprint:" label-for="footprint">
                <b-form-select
                  id="footprint"
                  v-model="form.footprint"
                  :options="choicesFootprint"
                  required
                ></b-form-select>
              </b-form-group>
            </b-col>
          </b-row>
        </b-form>
      </div>
    </div>

  </div>
</template>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<script>
import { mapState } from 'vuex'

export default {
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
      internal_pn: '',
      part_unit: null,
      category: null,
      storage_location: null,
      footprint: null
    }
  }),
  computed: {
    ...mapState({
      choicesPartUnit: (state) => {
        return state.preloads.part_units.map(function (x) { return { value: x.id, text: `${x.name} (${x.short_name})` } })
      },
      choicesCategory: state => state.preloads.categories,
      choicesStorageLocation: state => state.preloads.storages,
      choicesFootprint: state => state.preloads.footprints
    })
  },
  methods: {
    addPart: function () {
    }
  }
}
</script>
