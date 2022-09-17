<template>
  <div>
    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="name"
            :class="{
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
            placeholder="Under the bed"
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

    <template v-if="item.parent_id && !item.parent_id.null">
      <div class="flex justify-content-center">
        <div class="flex flex-grow-1 align-items-center justify-content-center">
          <div class="field w-10">
            <label for="parent_category" class="block mt-1"
              >Parent category</label
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
          <Button label="Save" @click.prevent="submit(!v$.$invalid)" />
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
    this.item.id = this.dialogRef.data.id;
    this.item.name = this.dialogRef.data.name;
    this.item.parent_id = this.dialogRef.data.parent_id;
    this.mode = this.dialogRef.data.mode;
  },
  validations: {
    item: {
      name: { required, maxLength: maxLength(200) },
      parent_id: {},
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
            icon: e.uuid ? `fa fa-folder-open` : `fa fa-home`,
            children: e.children && e.children.length ? e.children.map(cb) : [],
          };
          // return obj
          return obj;
        };
        return store.storages.map(cb);
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
      let storageCategory = {
        name: this.item.name,
      };

      if (this.item.parent_id && !this.item.parent_id.null) {
        storageCategory.parent = Object.keys(this.item.parent_id)[0];
      }

      apiService
        .createStorageCategory(storageCategory)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Storage Category",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Storage Category",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with storage category saving", err);
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      let storageCategory = {
        name: this.item.name,
      };

      if (this.item.parent_id && !this.item.parent_id.null) {
        storageCategory.parent = Object.keys(this.item.parent_id)[0];
      }

      apiService
        .updateStorageCategory(this.item.id, storageCategory)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Storage Category",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Storage Category",
            detail: "Update failed",
            life: 5000,
          });
          logger.default.error("Error with storage category update", err);
          this.dialogRef.close({ finished: true });
        });
    },
  },
};
</script>
