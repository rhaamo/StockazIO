<template>
  <div>
    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="file"
            :class="{
              block: true,
              'p-error': v$.item.file.$invalid && submitted,
              'w-full': true,
            }"
            >CSV File</label
          >
          <InputText
            ref="file"
            v-model="item.file"
            input-id="file"
            type="file"
            :class="{
              'p-invalid': v$.item.file.$invalid && submitted,
              'w-10': true,
            }"
            :accept="allowedUploadTypes"
            @change="importFileChanged($event.target.files)" />
          <small v-if="(v$.item.file.$invalid && submitted) || v$.item.file.$pending.$response" class="p-error">
            {{ v$.item.file.required.$message }}
          </small>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <PvButton label="Import" @click.prevent="submit(!v$.$invalid)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { mapState } from "pinia";
import { useServerStore } from "@/stores/server";

export default {
  inject: ["dialogRef"],
  setup: () => ({
    v$: useVuelidate(),
    toast: useToast(),
  }),
  data: () => ({
    submitted: false,
    item: {
      file: null,
    },
  }),
  created() {},
  validations: {
    item: {
      file: {
        required,
      },
    },
  },
  computed: {
    ...mapState(useServerStore, {
      allowedUploadTypes: (store) => {
        let types = ["text/csv"];
        return types.join(", ");
      },
    }),
  },
  methods: {
    submit(isFormValid) {
      this.submitted = true;
      if (!isFormValid) {
        return;
      }
      this.save();
    },
    save() {
      apiService
        .importLcscOrder(this.item.realFile)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Orders",
            detail: "Imported with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Orders",
            detail: "Import failed",
            life: 5000,
          });
          logger.default.error("Error with order import", err);
          this.dialogRef.close({ finished: true });
        });
    },
    importFileChanged(files) {
      this.item.realFile = files[0];
    },
  },
};
</script>
