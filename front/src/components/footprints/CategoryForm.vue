<template>
  <div>
    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <form @submit.prevent="submit(!v$.$invalid)">
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

            <label
              for="description"
              :class="{
                block: true,
                'p-error': v$.item.description.$invalid && submitted,
                'w-full': true,
                'mt-3': true,
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
            <small v-if="(v$.item.description.$invalid && submitted) || v$.item.description.$pending.$response" class="p-error">
              {{ v$.item.description.maxLength.$message }}
            </small>

            <div class="mt-4">
              <PvButton type="submit" label="Save" @click.prevent="submit(!v$.$invalid)" />
            </div>
          </form>
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
        description: this.dialogRef.data.item.description,
      };
    }
  },
  validations: {
    item: {
      name: { required, maxLength: maxLength(255) },
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
      let category = {
        name: this.item.name,
        description: this.item.description,
      };

      apiService
        .createFootprintCategory(category)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Footprint category",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          let errMsg = "name" in err.response.data ? err.response.data.name[0] : "Save failed";

          this.toast.add({
            severity: "error",
            summary: "Footprint category",
            detail: errMsg,
            life: 5000,
          });
          logger.default.error("Error with footprint category saving", err);
        });
    },
    edit() {
      let category = {
        name: this.item.name,
        description: this.item.description,
      };

      apiService
        .updateFootprintCategory(this.item.id, category)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Footprint category",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          let errMsg = "name" in err.response.data ? err.response.data.name[0] : "Save failed";

          this.toast.add({
            severity: "error",
            summary: "Footprint category",
            detail: errMsg,
            life: 5000,
          });
          logger.default.error("Error with footprint category update", err);
        });
    },
    pictureFileChanged(files) {
      this.item.realPicture = files[0];
    },
  },
};
</script>
