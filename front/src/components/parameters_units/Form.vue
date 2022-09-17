<template>
  <div>
    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="name"
            :class="{
              block: true,
              'p-error': v$.item.name.$invalid && submitted,
              'w-full': true,
            }"
            >Name*</label
          >
          <InputText
            autofocus
            v-focus
            ref="name"
            inputId="name"
            type="text"
            v-model="item.name"
            placeholder="Ampere"
            :class="{
              'p-invalid': v$.item.name.$invalid && submitted,
              'w-full': true,
            }"
          />
          <small
            v-if="
              (v$.item.name.$invalid && submitted) ||
              v$.item.name.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.item.name.required.$message }}
            <template v-if="v$.item.name.required && v$.item.name.maxLength"
              ><br
            /></template>
            {{ v$.item.name.maxLength.$message }}
          </small>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="symbol"
            :class="{
              block: true,
              'p-error': v$.item.symbol.$invalid && submitted,
              'w-full': true,
            }"
            >Symbol</label
          >
          <InputText
            ref="symbol"
            inputId="symbol"
            type="text"
            v-model="item.symbol"
            placeholder="A"
            :class="{
              'p-invalid': v$.item.symbol.$invalid && submitted,
              'w-full': true,
            }"
          />
          <small
            v-if="
              (v$.item.symbol.$invalid && submitted) ||
              v$.item.symbol.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.item.symbol.maxLength.$message }}
          </small>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="description"
            :class="{
              block: true,
              'p-error': v$.item.description.$invalid && submitted,
              'w-full': true,
            }"
            >Description</label
          >
          <InputText
            ref="description"
            inputId="description"
            type="text"
            v-model="item.description"
            :class="{
              'p-invalid': v$.item.description.$invalid && submitted,
              'w-full': true,
            }"
          />
          <small
            v-if="
              (v$.item.description.$invalid && submitted) ||
              v$.item.description.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.item.description.maxLength.$message }}
          </small>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <Button label="Save" @click.prevent="submit(!v$.$invalid)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";

export default {
  inject: ["dialogRef"],
  data: () => ({
    mode: null,
    item: {
      name: "",
      short_name: "",
      description: "",
    },
    submitted: false,
  }),
  setup: () => ({
    v$: useVuelidate(),
    toast: useToast(),
  }),
  created() {
    this.mode = this.dialogRef.data.mode; // add / edit
    if (this.dialogRef.data.item) {
      this.item = {
        id: this.dialogRef.data.item.id,
        name: this.dialogRef.data.item.name,
        symbol: this.dialogRef.data.item.symbol,
        description: this.dialogRef.data.item.description,
      };
    }
  },
  validations: {
    item: {
      name: { required, maxLength: maxLength(255) },
      symbol: { maxLength: maxLength(255) },
      description: { maxLength: maxLength(255) },
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
      let part_unit = {
        name: this.item.name,
        symbol: this.item.symbol,
        description: this.item.description,
      };

      apiService
        .createParametersUnits(part_unit)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Parameter unit",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Parameter unit",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with parameter unit saving", err);
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      let part_unit = {
        name: this.item.name,
        symbol: this.item.symbol,
        description: this.item.description,
      };

      apiService
        .updateParametersUnits(this.item.id, part_unit)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Parameter unit",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Parameter unit",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with parameter unit update", err);
          this.dialogRef.close({ finished: true });
        });
    },
  },
};
</script>
