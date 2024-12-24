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
            >Name</label
          >
          <InputText
            autofocus
            v-focus
            ref="name"
            inputId="name"
            type="text"
            v-model="item.name"
            :class="{
              'p-invalid': v$.item.name.$invalid && submitted,
              'w-full': true,
            }"
          />
          <small v-if="(v$.item.name.$invalid && submitted) || v$.item.name.$pending.$response" class="p-error"
            ><br />
            {{ v$.item.name.required.$message }}
            <template v-if="v$.item.name.required && v$.item.name.maxLength"><br /></template>
            {{ v$.item.name.maxLength.$message }}
          </small>

          <div class="mt-4" v-if="parent">Parent category: {{ parent.name }}.</div>

          <div class="mt-4">
            <PvButton label="Save" @click.prevent="submit(!v$.$invalid)" />
          </div>
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
      parent: null,
    },
    submitted: false,
  }),
  setup: () => ({
    v$: useVuelidate(),
    toast: useToast(),
  }),
  created() {
    this.mode = this.dialogRef.data.mode; // add / edit
    this.parent = this.dialogRef.data.parent;
    this.item.parent = this.parent ? this.parent.id : null;

    if (this.dialogRef.data.item) {
      this.item = {
        id: this.dialogRef.data.item.id,
        name: this.dialogRef.data.item.name,
        parent: this.dialogRef.data.item.parent,
      };
    }
  },
  validations: {
    item: {
      name: { required, maxLength: maxLength(255) },
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
      apiService
        .createCategory(this.item)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Category",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Category",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with category saving", err);
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      apiService
        .updateCategory(this.item.id, {
          name: this.item.name,
        })
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Category",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Category",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with category update", err);
          this.dialogRef.close({ finished: true });
        });
    },
  },
};
</script>
