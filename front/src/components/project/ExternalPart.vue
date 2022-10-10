<template>
  <div>
    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="part_name"
            :class="{
              block: true,
              'p-error': v$.item.part_name.$invalid && submitted,
              'w-full': true,
            }"
            >Name*</label
          >
          <InputText
            autofocus
            v-focus
            ref="part_name"
            inputId="part_name"
            type="text"
            v-model="item.part_name"
            placeholder="PIC42ACHU"
            :class="{
              'p-invalid': v$.item.part_name.$invalid && submitted,
              'w-full': true,
            }"
          />
          <small
            v-if="
              (v$.item.part_name.$invalid && submitted) ||
              v$.item.part_name.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.item.part_name.required.$message }}
            <template
              v-if="v$.item.part_name.required && v$.item.part_name.maxLength"
              ><br
            /></template>
            {{ v$.item.part_name.maxLength.$message }}
          </small>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="qty"
            :class="{
              block: true,
              'p-error': v$.item.qty.$invalid && submitted,
              'w-full': true,
            }"
            >Qty</label
          >
          <InputNumber
            ref="qty"
            inputId="qty"
            type="text"
            v-model="item.qty"
            showButtons
            :class="{
              'p-invalid': v$.item.qty.$invalid && submitted,
              'w-full': true,
            }"
          />
          <small
            v-if="
              (v$.item.qty.$invalid && submitted) ||
              v$.item.qty.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.item.qty.required.$message }}
            <template v-if="v$.item.qty.required && v$.item.qty.minVal"
              ><br
            /></template>
            {{ v$.item.qty.minVal.$message }}
          </small>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="notes"
            :class="{
              block: true,
              'p-error': v$.item.notes.$invalid && submitted,
              'w-full': true,
            }"
            >Notes</label
          >
          <InputText
            ref="notes"
            inputId="notes"
            type="text"
            v-model="item.notes"
            :class="{
              'p-invalid': v$.item.notes.$invalid && submitted,
              'w-full': true,
            }"
          />
          <small
            v-if="
              (v$.item.notes.$invalid && submitted) ||
              v$.item.notes.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.item.notes.maxLength.$message }}
          </small>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field-checkbox w-10">
          <Checkbox
            :class="{
              'p-invalid': v$.item.sourced.$invalid && submitted,
            }"
            inputId="sourced"
            v-model="item.sourced"
            :binary="true"
          />
          <label
            for="sourced"
            :class="{
              'p-error': v$.item.sourced.$invalid && submitted,
            }"
            >Sourced</label
          >
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <PvButton label="Save" @click.prevent="submit(!v$.$invalid)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength, minValue } from "@vuelidate/validators";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";

export default {
  inject: ["dialogRef"],
  data: () => ({
    mode: null,
    item: {
      part_name: "",
      qty: 1,
      sourced: false,
      notes: "",
    },
    project: null,
    submitted: false,
  }),
  setup: () => ({
    v$: useVuelidate(),
    toast: useToast(),
  }),
  created() {
    this.mode = this.dialogRef.data.mode; // add / edit
    this.project = this.dialogRef.data.project;

    if (this.dialogRef.data.item) {
      this.item = {
        id: this.dialogRef.data.item.id,
        part_name: this.dialogRef.data.item.part_name,
        qty: this.dialogRef.data.item.qty,
        sourced: this.dialogRef.data.item.sourced,
        notes: this.dialogRef.data.item.notes,
        project: this.project.id,
      };
    }
  },
  validations: {
    item: {
      part_name: { required, maxLength: maxLength(255) },
      qty: {
        required,
        minValue: minValue(0),
      },
      sourced: {},
      notes: { maxLength: maxLength(255) },
    },
  },
  computed: {},
  methods: {
    submit(isFormValid) {
      this.submitted = true;
      if (!isFormValid) {
        return;
      }

      if (this.mode === "add") {
        this.save();
      } else {
        this.edit();
      }
    },
    save() {
      let part = {
        part_name: this.item.part_name,
        qty: this.item.qty,
        sourced: this.item.sourced,
        notes: this.item.notes,
        project: this.project.id,
      };

      apiService
        .projectAddPart(this.project.id, part)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "External part",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "External part",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with external part saving", err);
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      let part = {
        part_name: this.item.part_name,
        qty: this.item.qty,
        sourced: this.item.sourced,
        notes: this.item.notes,
        project: this.project.id,
      };

      apiService
        .projectUpdatePart(this.project.id, this.item.id, part)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "External part",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "External part",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with external part update", err);
          this.dialogRef.close({ finished: true });
        });
    },
  },
};
</script>
