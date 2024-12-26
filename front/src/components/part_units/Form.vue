<template>
  <div>
    <form @submit.prevent="submit(!v$.$invalid)">
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
              ref="name"
              v-model="item.name"
              v-focus
              autofocus
              input-id="name"
              type="text"
              placeholder="Centimeters"
              :class="{
                'p-invalid': v$.item.name.$invalid && submitted,
                'w-full': true,
              }" />
            <small v-if="(v$.item.name.$invalid && submitted) || v$.item.name.$pending.$response" class="p-error"
              ><br />
              {{ v$.item.name.required.$message }}
              <template v-if="v$.item.name.required && v$.item.name.maxLength"><br /></template>
              {{ v$.item.name.maxLength.$message }}
            </small>
          </div>
        </div>
      </div>

      <div class="flex justify-content-center">
        <div class="flex flex-grow-1 align-items-center justify-content-center">
          <div class="field w-10">
            <label
              for="short_name"
              :class="{
                block: true,
                'p-error': v$.item.short_name.$invalid && submitted,
                'w-full': true,
              }"
              >Short name*</label
            >
            <InputText
              ref="short_name"
              v-model="item.short_name"
              input-id="short_name"
              type="text"
              placeholder="cm"
              :class="{
                'p-invalid': v$.item.short_name.$invalid && submitted,
                'w-full': true,
              }" />
            <small v-if="(v$.item.short_name.$invalid && submitted) || v$.item.short_name.$pending.$response" class="p-error"
              ><br />
              {{ v$.item.short_name.required.$message }}
              <template v-if="v$.item.short_name.required && v$.item.short_name.maxLength"><br /></template>
              {{ v$.item.short_name.maxLength.$message }}
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
              v-model="item.description"
              input-id="description"
              type="text"
              :class="{
                'p-invalid': v$.item.description.$invalid && submitted,
                'w-full': true,
              }" />
            <small v-if="(v$.item.description.$invalid && submitted) || v$.item.description.$pending.$response" class="p-error"
              ><br />
              {{ v$.item.description.maxLength.$message }}
            </small>
          </div>
        </div>
      </div>

      <div class="flex justify-content-center">
        <div class="flex flex-grow-1 align-items-center justify-content-center">
          <div class="field w-10">
            <PvButton type="submit" label="Save" @click.prevent="submit(!v$.$invalid)" />
          </div>
        </div>
      </div>
    </form>
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
  setup: () => ({
    v$: useVuelidate(),
    toast: useToast(),
  }),
  data: () => ({
    mode: null,
    item: {
      name: "",
      short_name: "",
      description: "",
    },
    submitted: false,
  }),
  created() {
    this.mode = this.dialogRef.data.mode; // add / edit
    if (this.dialogRef.data.item) {
      this.item = {
        id: this.dialogRef.data.item.id,
        name: this.dialogRef.data.item.name,
        short_name: this.dialogRef.data.item.short_name,
        description: this.dialogRef.data.item.description,
      };
    }
  },
  validations: {
    item: {
      name: { required, maxLength: maxLength(255) },
      short_name: { required, maxLength: maxLength(255) },
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
        short_name: this.item.short_name,
        description: this.item.description,
      };

      apiService
        .createPartUnit(part_unit)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Part unit",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Part unit",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with part unit saving", err);
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      let part_unit = {
        name: this.item.name,
        short_name: this.item.short_name,
        description: this.item.description,
      };

      apiService
        .updatePartUnit(this.item.id, part_unit)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Part unit",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Part unit",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with part unit update", err);
          this.dialogRef.close({ finished: true });
        });
    },
  },
};
</script>
