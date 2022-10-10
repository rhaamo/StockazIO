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
          <small
            v-if="
              (v$.item.description.$invalid && submitted) ||
              v$.item.description.$pending.$response
            "
            class="p-error"
          >
            {{ v$.item.description.maxLength.$message }}
          </small>

          <label
            for="picture"
            :class="{
              block: true,
              'p-error': v$.item.picture.$invalid && submitted,
              'w-full': true,
              'mt-3': true,
            }"
            >Picture</label
          >
          <InputText
            ref="picture"
            inputId="picture"
            type="file"
            v-model="item.picture"
            @change="pictureFileChanged($event.target.files)"
            :class="{
              'p-invalid': v$.item.picture.$invalid && submitted,
              'w-full': true,
            }"
            :accept="allowedUploadTypes"
          />
          <small
            v-if="
              (v$.item.picture.$invalid && submitted) ||
              v$.item.picture.$pending.$response
            "
            class="p-error"
          >
            {{ v$.item.picture.required.$message }}
          </small>

          <template
            v-if="mode === 'edit' && typeof item.hasPicture === 'string'"
          >
            <br />
            Actual picture
            <a :href="item.hasPicture" target="_blank">file</a>.
          </template>

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
import { mapState } from "pinia";
import { useServerStore } from "@/stores/server";
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
      picture: "",
    },
    category_id: null,
    submitted: false,
  }),
  setup: () => ({
    v$: useVuelidate(),
    toast: useToast(),
  }),
  created() {
    this.mode = this.dialogRef.data.mode; // add / edit
    this.category_id = this.dialogRef.data.category_id;
    if (this.dialogRef.data.item) {
      this.item = {
        id: this.dialogRef.data.item.id,
        name: this.dialogRef.data.item.name,
        description: this.dialogRef.data.item.description,
        hasPicture: this.dialogRef.data.item.picture,
      };
    }
  },
  validations: {
    item: {
      name: { required, maxLength: maxLength(255) },
      description: { maxLength: maxLength(255) },
      picture: {},
    },
  },
  computed: {
    ...mapState(useServerStore, {
      allowedUploadTypes: (store) => {
        let types = store.settings.partAttachmentAllowedTypes || [
          "image/png",
          "image/jpeg",
        ];
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

      if (this.mode === "add") {
        this.save();
      } else {
        this.edit();
      }
    },
    save() {
      let footprint = {
        name: this.item.name,
        description: this.item.description,
        picture: this.item.realPicture,
        category: this.category_id,
      };

      apiService
        .createFootprint(footprint)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Footprint",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          let errMsg =
            "name" in err.response.data
              ? err.response.data.name[0]
              : "Save failed";

          this.toast.add({
            severity: "error",
            summary: "Footprint",
            detail: errMsg,
            life: 5000,
          });
          logger.default.error("Error with footprint saving", err);
        });
    },
    edit() {
      let footprint = {
        name: this.item.name,
        description: this.item.description,
        category: this.category_id,
      };

      if (this.item.realPicture) {
        footprint.picture = this.item.realPicture;
      }

      apiService
        .updateFootprint(this.item.id, footprint)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Footprint",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          let errMsg =
            "name" in err.response.data
              ? err.response.data.name[0]
              : "Save failed";

          this.toast.add({
            severity: "error",
            summary: "Footprint",
            detail: errMsg,
            life: 5000,
          });
          logger.default.error("Error with footprint update", err);
        });
    },
    pictureFileChanged(files) {
      this.item.realPicture = files[0];
    },
  },
};
</script>
