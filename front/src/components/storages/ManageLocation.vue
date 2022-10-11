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
            placeholder="That one box"
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
            for="description"
            :class="{
              block: true,
              'p-error': v$.item.description.$invalid && submitted,
              'w-full': true,
            }"
            >description</label
          >
          <InputText
            ref="description"
            inputId="description"
            type="text"
            v-model="item.description"
            placeholder="Full of emptyness"
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

    <template v-if="item.parent_id && !item.parent_id.null">
      <div class="flex justify-content-center">
        <div class="flex flex-grow-1 align-items-center justify-content-center">
          <div class="field w-10">
            <label for="parent_category" class="block mt-1"
              >Storage place</label
            >
            <TreeSelect
              inputId="parent_category"
              class="w-full"
              v-model="item.parent_id"
              :options="choicesCategories"
              selectionMode="single"
            />
          </div>
        </div>
      </div>
    </template>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="picture"
            :class="{
              block: true,
              'p-error': v$.item.picture.$invalid && submitted,
              'w-full': true,
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
            Actual picture <a :href="item.hasPicture" target="_blank">file</a>.
          </template>
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
import useVuelidate from "@vuelidate/core";
import { useToast } from "primevue/usetoast";
import { required, maxLength } from "@vuelidate/validators";
import apiService from "@/services/api/api.service";
import { usePreloadsStore } from "@/stores/preloads";
import { mapState } from "pinia";
import logger from "@/logging";
import { useServerStore } from "@/stores/server";

export default {
  inject: ["dialogRef"],
  data: () => ({
    submitted: false,
    item: {
      name: "",
      parent_id: null,
    },
  }),
  setup: () => ({
    v$: useVuelidate(),
    toast: useToast(),
  }),
  created() {
    this.mode = this.dialogRef.data.mode;

    this.item.id = this.dialogRef.data.id;
    this.item.name = this.dialogRef.data.name;
    this.item.parent_id = this.dialogRef.data.parent_id;
    this.item.description = this.dialogRef.data.description;
    this.item.hasPicture = this.dialogRef.data.picture;
  },
  validations: {
    item: {
      name: { required, maxLength: maxLength(200) },
      parent_id: {},
      description: { maxLength: maxLength(255) },
      picture: {},
    },
  },
  computed: {
    ...mapState(usePreloadsStore, {
      choicesCategories: (store) => {
        const cb = (e) => {
          // base object
          let obj = {
            key: e.id,
            label: e.name,
            icon: "fa fa-ellipsis-h",
            children: e.children && e.children.length ? e.children.map(cb) : [],
          };
          // return obj
          return obj;
        };
        return store.storages.map(cb);
      },
    }),
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
    pictureFileChanged(files) {
      this.item.realPicture = files[0];
    },
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
      let storageLocation = {
        name: this.item.name,
        description: this.item.description,
        picture: this.item.realPicture,
      };

      if (this.item.parent_id && !this.item.parent_id.null) {
        storageLocation.parent = Object.keys(this.item.parent_id)[0];
      }

      apiService
        .createStorageLocation(storageLocation)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Storage Location",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Storage Location",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with storage location saving", err);
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      let storageLocation = {
        name: this.item.name,
        description: this.item.description,
      };

      if (this.item.parent_id && !this.item.parent_id == null) {
        storageLocation.parent = Object.keys(this.item.parent_id)[0];
      }

      if (this.item.realPicture) {
        storageLocation.picture = this.item.realPicture;
      }

      apiService
        .updateStorageLocation(this.item.id, storageLocation)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Storage Location",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Storage Location",
            detail: "Update failed",
            life: 5000,
          });
          logger.default.error("Error with storage location update", err);
          this.dialogRef.close({ finished: true });
        });
    },
  },
};
</script>
