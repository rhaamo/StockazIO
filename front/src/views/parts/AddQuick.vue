<template>
  <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
  <div class="card ml-5">
    <h2>Basic parts informations</h2>
    <form>
      <div class="formgrid grid">
        <div class="field col-12 md:col-6">
          <label
            for="Name"
            :class="{
              block: true,
              'p-error': v$.form.name.$invalid && submitted,
            }"
            >Name*</label>
          <InputText
            type="text"
            v-model="form.name"
            placeholder="PIC42ACHU"
            :class="{
              'p-invalid': v$.form.name.$invalid && submitted,
              'w-10': true,
            }"
          />
          <small
            v-if="
              (v$.form.name.$invalid && submitted) ||
              v$.form.name.$pending.$response
            "
            class="p-error"
            ><br />{{ v$.form.name.required.$message }}</small>
        </div>
        <div class="field col-12 md:col-6">
          <label for="part_unit" class="block">Part unit</label>
          <MultiSelect placeholder="Centimeters ? Pieces ?" class="w-7" />
        </div>

        <div class="field col-12 md:col-6">
          <label for="Name" class="block">Description</label>
          <InputText type="text" placeholder="A cute little mcu" class="w-10" />
        </div>
        <div class="field col-12 md:col-6">
          <label for="part_unit" class="block">Category</label>
          <TreeSelect placeholder="Film resistors ? MCUs ?" class="w-7" />
        </div>

        <div class="field col-12 md:col-6">
          <label for="Name" class="block">Comment</label>
          <InputText
            type="text"
            placeholder="Any comment about this part ?"
            class="w-10"
          />
        </div>
        <div class="field col-12 md:col-6">
          <label for="part_unit" class="block">Storage Location</label>
          <TreeSelect
            placeholder="A box under the bench or some drawer ?"
            class="w-7"
          />
        </div>

        <div class="field col-12 md:col-3">
          <label for="Name" class="block">Stock Qty*</label>
          <InputNumber
            inputId="minmax-buttons"
            mode="decimal"
            showButtons
            :min="0"
            class="w-8"
          />
        </div>
        <div class="field col-12 md:col-3">
          <label for="Name" class="block">Stock Qty Min*</label>
          <InputNumber
            inputId="minmax-buttons"
            mode="decimal"
            showButtons
            :min="0"
            class="w-8"
          />
        </div>

        <div class="field col-12 md:col-6">
          <label for="part_unit" class="block">Footprint</label>
          <MultiSelect placeholder="PDIP, BGA, SOIC, who knows" class="w-7" />
        </div>

        <div class="field col-12 md:col-6">
          <label for="Name" class="block">Sheet status</label>
          <InputText type="text" class="w-10" />
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
          <label for="Name" class="block">Part Condition</label>
          <InputText
            type="text"
            placeholder="Condition of the part"
            class="w-5"
          />
        </div>

        <div class="field col-12 md:col-12">
          <label for="Name" class="block">Production Remarks</label>
          <InputText type="text" class="w-5" />
        </div>

        <div class="field col-12 md:col-12">
          <label for="Name" class="block">Internal Part Number</label>
          <InputText type="text" class="w-5" />
        </div>

        <div class="field-checkbox col-12 md:col-2">
          <Checkbox inputId="binary" :binary="true" />
          <label for="Name">This sheet needs review</label>
        </div>
        <div class="field-checkbox col-12 md:col-2">
          <Checkbox inputId="binary" :binary="true" />
          <label for="Name">That part can be sold</label>
        </div>
        <div class="field-checkbox col-12 md:col-2">
          <Checkbox inputId="binary" :binary="true" />
          <label for="Name">That part is private</label>
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
  },
};
</script>
