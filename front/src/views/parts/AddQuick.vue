<template>
  <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
  <div class="card ml-5">
    <h2>Basic parts informations</h2>
    <form>
      <div class="formgrid grid">
        <div class="field col-12 md:col-6">
          <label
            for="name"
            :class="{
              block: true,
              'p-error': v$.form.name.$invalid && submitted,
              'w-10': true,
            }"
            >Name*</label
          >
          <InputText
            id="name"
            type="text"
            v-model="form.name"
            placeholder="PIC42ACHU"
            :class="{
              'p-invalid': v$.form.name.$invalid && submitted,
              'w-10': true,
            }"
            @blur="checkIfPartExists"
          />
          <small
            v-if="
              (v$.form.name.$invalid && submitted) ||
              v$.form.name.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.name.required.$message }}
            <template v-if="v$.form.name.required && v$.form.name.maxLength"
              ><br
            /></template>
            {{ v$.form.name.maxLength.$message }}
          </small>
          <div v-if="partsExists && partsExists.length">
            One or more parts exists with this name:
            <div v-for="p in partsExists" :key="p.uuid">
              <a href="#">{{ p.name }}</a
              >&nbsp;
            </div>
          </div>
        </div>
        <div class="field col-12 md:col-6">
          <label for="part_unit" class="block">Part unit</label>
          <MultiSelect
            v-model="form.part_unit"
            placeholder="Centimeters ? Pieces ?"
            class="w-7"
            :options="choicesPartUnit"
            optionLabel="text"
            optionValue="value"
            :selectionLimit="1"
          />
        </div>

        <div class="field col-12 md:col-6">
          <label
            for="description"
            :class="{
              block: true,
              'p-error': v$.form.description.$invalid && submitted,
              'w-10': true,
            }"
            >Description</label
          >
          <InputText
            id="description"
            type="text"
            placeholder="A cute little mcu"
            :class="{
              'p-invalid': v$.form.description.$invalid && submitted,
              'w-10': true,
            }"
            v-model="form.description"
          />
          <small
            v-if="
              (v$.form.description.$invalid && submitted) ||
              v$.form.description.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.description.maxLength.$message }}
          </small>
        </div>
        <div class="field col-12 md:col-6">
          <label for="part_unit" class="block">Category</label>
          <TreeSelect placeholder="Film resistors ? MCUs ?" class="w-7" />
        </div>

        <div class="field col-12 md:col-6">
          <label
            for="comment"
            :class="{
              block: true,
              'p-error': v$.form.comment.$invalid && submitted,
              'w-10': true,
            }"
            >Comment</label
          >
          <InputText
            id="comment"
            type="text"
            placeholder="Any comment about this part ?"
            v-model="form.comment"
            :class="{
              'p-invalid': v$.form.description.$invalid && submitted,
              'w-10': true,
            }"
          />
          <small
            v-if="
              (v$.form.comment.$invalid && submitted) ||
              v$.form.comment.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.comment.maxLength.$message }}
          </small>
        </div>
        <div class="field col-12 md:col-6">
          <label for="storage_location" class="block">Storage Location</label>
          <TreeSelect
            id="storage_location"
            placeholder="A box under the bench or some drawer ?"
            class="w-7"
            v-model="form.storage_location"
            :options="choicesStorageLocation"
            selectionMode="single"
          />
        </div>

        <div class="field col-12 md:col-3">
          <label
            for="qty"
            :class="{
              block: true,
              'p-error': v$.form.qty.$invalid && submitted,
              'w-8': true,
            }"
            >Stock Qty*</label
          >
          <InputNumber
            id="qty"
            mode="decimal"
            showButtons
            :min="0"
            :class="{
              'p-invalid': v$.form.qty.$invalid && submitted,
              'w-8': true,
            }"
            v-model="form.qty"
          />
          <small
            v-if="
              (v$.form.qty.$invalid && submitted) ||
              v$.form.qty.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.qty.required.$message }}
            <template v-if="v$.form.qty.required && v$.form.qty.minValue"
              ><br
            /></template>
            {{ v$.form.qty.minValue.$message }}
          </small>
        </div>
        <div class="field col-12 md:col-3">
          <label
            for="qty_min"
            :class="{
              block: true,
              'p-error': v$.form.qty_min.$invalid && submitted,
              'w-8': true,
            }"
            >Stock Qty Min*</label
          >
          <InputNumber
            id="qty_min"
            mode="decimal"
            showButtons
            :min="0"
            :class="{
              'p-invalid': v$.form.qty_min.$invalid && submitted,
              'w-8': true,
            }"
            v-model="form.qty_min"
          />
          <small
            v-if="
              (v$.form.qty_min.$invalid && submitted) ||
              v$.form.qty_min.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.qty_min.required.$message }}
            <template
              v-if="v$.form.qty_min.required && v$.form.qty_min.minValue"
              ><br
            /></template>
            {{ v$.form.qty_min.minValue.$message }}
          </small>
        </div>

        <div class="field col-12 md:col-6">
          <label for="footprint" class="block">Footprint</label>
          <MultiSelect
            id="footprint"
            v-model="form.footprint"
            placeholder="PDIP, BGA, SOIC, who knows"
            class="w-7"
            :options="choicesFootprint"
            optionLabel="name"
            optionValue="id"
            optionGroupLabel="category"
            optionGroupChildren="footprints"
            :selectionLimit="1"
            :filter="true"
          />
        </div>

        <div class="field col-12 md:col-6">
          <label
            for="sheet_status"
            :class="{
              block: true,
              'p-error': v$.form.sheet_status.$invalid && submitted,
              'w-10': true,
            }"
            >Sheet status</label
          >
          <InputText
            id="sheet_status"
            type="text"
            :class="{
              'p-invalid': v$.form.sheet_status.$invalid && submitted,
              'w-10': true,
            }"
            v-model="form.sheet_status"
          />
          <small
            v-if="
              (v$.form.sheet_status.$invalid && submitted) ||
              v$.form.sheet_status.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.sheet_status.maxLength.$message }}
          </small>
        </div>

        <div class="field col-12 md:col-6">
          <!-- save and save add another-->
          <Button
            label="Save and view"
            class="p-button-primary"
            @click.prevent="submit(!v$.$invalid, 'continue')"
          />
          <Button
            label="Save and add another"
            class="ml-2 p-button-secondary"
            @click.prevent="submit(!v$.$invalid, 'add_new')"
          />
        </div>

        <div class="field col-12 md:col-12">
          <label
            for="condition"
            :class="{
              block: true,
              'p-error': v$.form.condition.$invalid && submitted,
              'w-5': true,
            }"
            >Part Condition</label
          >
          <InputText
            type="text"
            id="condition"
            v-model="form.condition"
            placeholder="Condition of the part"
            :class="{
              'p-invalid': v$.form.condition.$invalid && submitted,
              'w-5': true,
            }"
          />
          <small
            v-if="
              (v$.form.condition.$invalid && submitted) ||
              v$.form.condition.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.condition.maxLength.$message }}
          </small>
        </div>

        <div class="field col-12 md:col-12">
          <label
            for="production_remarks"
            :class="{
              block: true,
              'p-error': v$.form.production_remarks.$invalid && submitted,
              'w-5': true,
            }"
            >Production Remarks</label
          >
          <InputText
            id="production_remarks"
            v-model="form.production_remarks"
            type="text"
            :class="{
              'p-invalid': v$.form.production_remarks.$invalid && submitted,
              'w-5': true,
            }"
          />
          <small
            v-if="
              (v$.form.production_remarks.$invalid && submitted) ||
              v$.form.production_remarks.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.production_remarks.maxLength.$message }}
          </small>
        </div>

        <div class="field col-12 md:col-12">
          <label
            for="internal_pn"
            :class="{
              block: true,
              'p-error': v$.form.internal_pn.$invalid && submitted,
              'w-5': true,
            }"
            >Internal Part Number</label
          >
          <InputText
            id="internal_pn"
            v-model="form.internal_pn"
            type="text"
            :class="{
              'p-invalid': v$.form.internal_pn.$invalid && submitted,
              'w-5': true,
            }"
          />
          <small
            v-if="
              (v$.form.internal_pn.$invalid && submitted) ||
              v$.form.internal_pn.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.internal_pn.maxLength.$message }}
          </small>
        </div>

        <div class="field-checkbox col-12 md:col-2">
          <Checkbox
            :class="{
              'p-invalid': v$.form.needs_review.$invalid && submitted,
            }"
            inputId="needs_review"
            v-model="form.needs_review"
            :binary="true"
          />
          <label
            for="needs_review"
            :class="{
              'p-error': v$.form.needs_review.$invalid && submitted,
            }"
            >This sheet needs review</label
          >
        </div>
        <div class="field-checkbox col-12 md:col-2">
          <Checkbox
            :class="{
              'p-invalid': v$.form.can_be_sold.$invalid && submitted,
            }"
            inputId="can_be_sold"
            :binary="true"
            v-model="form.can_be_sold"
          />
          <label
            :class="{
              'p-error': v$.form.can_be_sold.$invalid && submitted,
            }"
            for="can_be_sold"
            >That part can be sold</label
          >
        </div>
        <div class="field-checkbox col-12 md:col-2">
          <Checkbox
            :class="{
              'p-invalid': v$.form.private.$invalid && submitted,
            }"
            inputId="private"
            :binary="true"
            v-model="form.private"
          />
          <label
            :class="{
              'p-error': v$.form.private.$invalid && submitted,
            }"
            for="private"
            >That part is private</label
          >
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { usePreloadsStore } from "@/stores/preloads";
import { required, maxLength, integer, minValue } from "@vuelidate/validators";
import logger from "@/logging";
import apiService from "@/services/api/api.service";
import { mapState } from "pinia";
import utils from "@/utils.js";

export default {
  data: () => ({
    submitted: false,
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [{ label: "Quick add new part" }],
    },
    form: {
      name: "",
      description: "",
      comment: "",
      qty: 1,
      qty_min: 0,
      sheet_status: "",
      condition: "",
      needs_review: false,
      can_be_sold: false,
      private: false,
      production_remarks: "",
      internal_pn: "",
      part_unit: null,
      category: null,
      storage_location: null,
      footprint: null,
    },
    partsExists: [],
    partDetails: null,
  }),
  setup: () => ({
    v$: useVuelidate(),
    preloadsStore: usePreloadsStore(),
  }),
  computed: {
    ...mapState(usePreloadsStore, {
      choicesPartUnit: (store) =>
        store.part_units.map((x) => {
          return { value: x.id, text: `${x.name} (${x.short_name})` };
        }),
      choicesCategory: (store) => store.categories,
      choicesStorageLocation: (store) => {
        const cb = (e) => {
          // base object
          let obj = {
            key: e.uuid ? e.id : `cat-${e.id}`,
            label: e.name,
            icon: e.uuid ? `fa fa-folder-open` : `fa fa-home`,
          };
          // Selectable only if no locations
          obj["selectable"] = e.storage_locations ? false : true;
          // Merge children with storage_locations
          if (e.storage_locations && e.children) {
            obj["children"] = e.children.concat(e.storage_locations).map(cb);
          }
          // return obj
          return obj;
        };
        return store.storages.filter(utils.removeStorageCatWithoutLocs).map(cb);
      },
      choicesFootprint: (store) =>
        store.footprints.map((x) => {
          return {
            category: x.name,
            footprints: x.footprint_set.map((y) => {
              return { id: y.id, name: y.name };
            }),
          };
        }),
    }),
  },
  validations: {
    form: {
      name: {
        required,
        maxLength: maxLength(255),
      },
      description: {
        maxLength: maxLength(255),
      },
      comment: {
        maxLength: maxLength(255),
      },
      qty: {
        required,
        integer,
        minValue: minValue(0),
      },
      qty_min: {
        required,
        integer,
        minValue: minValue(0),
      },
      sheet_status: {
        maxLength: maxLength(255),
      },
      needs_review: {},
      condition: {
        maxLength: maxLength(255),
      },
      can_be_sold: {},
      private: {},
      production_remarks: {
        maxLength: maxLength(255),
      },
      internal_pn: {
        maxLength: maxLength(255),
      },
      part_unit: {},
      category: {},
      storage_location: {},
      footprint: {},
    },
  },
  methods: {
    submit(isFormValid, mode) {
      this.submitted = true;

      if (!isFormValid) {
        return;
      }
    },
    checkIfPartExists(event) {
      if (this.form.name === "") {
        return;
      }
      apiService
        .partsAutocompleteQuick(this.form.name)
        .then((res) => {
          this.partsExists = res.data;
        })
        .catch((err) => {
          if (err.response.status === 404) {
            logger.default.info("Autocompleter said part not found");
          } else {
            logger.default.error(
              "Got an error from the autocompleter",
              err.message
            );
          }
          this.partsExists = [];
        });
    },
  },
};
</script>
