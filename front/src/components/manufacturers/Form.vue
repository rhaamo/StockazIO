<template>
  <div>
    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <form @submit.prevent="submit(!v$.$invalid)">
            <div class="grid">
              <div class="col-6">
                <label
                  for="name"
                  :class="{
                    block: true,
                    'p-error': v$.item.name.$invalid && submitted,
                    'w-10': true,
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
                  :class="{
                    'p-invalid': v$.item.name.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.item.name.$invalid && submitted) || v$.item.name.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.item.name.required.$message }}
                  <template v-if="v$.item.name.required && v$.item.name.maxLength"><br /></template>
                  {{ v$.item.name.maxLength.$message }}
                </small>
              </div>

              <div class="col-6">
                <label
                  for="logo"
                  :class="{
                    block: true,
                    'p-error': v$.item.logo.$invalid && submitted,
                    'w-10': true,
                  }"
                  >Logo</label
                >
                <InputText
                  ref="logo"
                  v-model="item.logo"
                  input-id="logo"
                  type="file"
                  :class="{
                    'p-invalid': v$.item.logo.$invalid && submitted,
                    'w-10': true,
                  }"
                  :accept="allowedUploadTypes"
                  @change="logoFileChanged($event.target.files)" />
                <small v-if="(v$.item.logo.$invalid && submitted) || v$.item.logo.$pending.$response" class="p-error">
                  {{ v$.item.logo.required.$message }}
                </small>

                <template v-if="mode === 'edit' && typeof item.hasLogo === 'string'">
                  <br />
                  Actual logo <a :href="item.hasLogo" target="_blank">file</a>.
                </template>
              </div>

              <div class="col-6">
                <label
                  for="address"
                  :class="{
                    block: true,
                    'p-error': v$.item.address.$invalid && submitted,
                    'w-10': true,
                    'mt-3': true,
                  }"
                  >Address</label
                >
                <PvTextarea
                  ref="address"
                  v-model="item.address"
                  v-focus
                  input-id="address"
                  type="text"
                  :class="{
                    'p-invalid': v$.item.address.$invalid && submitted,
                    'w-10': true,
                  }" />
              </div>

              <div class="col-6">
                <label
                  for="comment"
                  :class="{
                    block: true,
                    'p-error': v$.item.comment.$invalid && submitted,
                    'w-10': true,
                    'mt-3': true,
                  }"
                  >Comment</label
                >
                <PvTextarea
                  ref="comment"
                  v-model="item.comment"
                  v-focus
                  input-id="comment"
                  type="text"
                  :class="{
                    'p-invalid': v$.item.comment.$invalid && submitted,
                    'w-10': true,
                  }" />
              </div>

              <div class="col-6">
                <label
                  for="url"
                  :class="{
                    block: true,
                    'p-error': v$.item.url.$invalid && submitted,
                    'w-10': true,
                    'mt-3': true,
                  }"
                  >Website</label
                >
                <InputText
                  ref="url"
                  v-model="item.url"
                  input-id="url"
                  type="url"
                  placeholder="http://somewhere/"
                  :class="{
                    'p-invalid': v$.item.url.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.item.url.$invalid && submitted) || v$.item.url.$pending.$response" class="p-error">
                  {{ v$.item.url.url.$message }}
                  <template v-if="v$.item.url.url && v$.item.url.maxLength"><br /></template>
                  {{ v$.item.url.maxLength.$message }}
                </small>
              </div>

              <div class="col-6">
                <label
                  for="phone"
                  :class="{
                    block: true,
                    'p-error': v$.item.phone.$invalid && submitted,
                    'w-10': true,
                    'mt-3': true,
                  }"
                  >Phone</label
                >
                <InputText
                  ref="phone"
                  v-model="item.phone"
                  input-id="phone"
                  type="text"
                  :class="{
                    'p-invalid': v$.item.phone.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.item.phone.$invalid && submitted) || v$.item.phone.$pending.$response" class="p-error">
                  {{ v$.item.phone.maxLength.$message }}
                </small>
              </div>

              <div class="col-6">
                <label
                  for="email"
                  :class="{
                    block: true,
                    'p-error': v$.item.email.$invalid && submitted,
                    'w-10': true,
                    'mt-3': true,
                  }"
                  >Email</label
                >
                <InputText
                  ref="email"
                  v-model="item.email"
                  input-id="email"
                  type="email"
                  :class="{
                    'p-invalid': v$.item.email.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.item.email.$invalid && submitted) || v$.item.email.$pending.$response" class="p-error">
                  {{ v$.item.email.email.$message }}
                  <template v-if="v$.item.email.email && v$.item.email.maxLength"><br /></template>
                  {{ v$.item.email.maxLength.$message }}
                </small>
              </div>

              <div class="col-6">
                <label
                  for="fax"
                  :class="{
                    block: true,
                    'p-error': v$.item.fax.$invalid && submitted,
                    'w-10': true,
                    'mt-3': true,
                  }"
                  >FAX</label
                >
                <InputText
                  ref="fax"
                  v-model="item.fax"
                  input-id="fax"
                  type="text"
                  :class="{
                    'p-invalid': v$.item.fax.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.item.fax.$invalid && submitted) || v$.item.fax.$pending.$response" class="p-error">
                  {{ v$.item.fax.maxLength.$message }}
                </small>
              </div>

              <div class="col-6">
                <label
                  for="datasheet_url"
                  :class="{
                    block: true,
                    'p-error': v$.item.datasheet_url.$invalid && submitted,
                    'w-10': true,
                    'mt-3': true,
                  }"
                  >Datasheet URL Template</label
                >
                <InputText
                  ref="datasheet_url"
                  v-model="item.datasheet_url"
                  input-id="datasheet_url"
                  type="url"
                  placeholder="http://somewhere/{sku}.pdf"
                  :class="{
                    'p-invalid': v$.item.datasheet_url.$invalid && submitted,
                    'w-10': true,
                  }" />
                <br />
                You can uses the following template in the datasheet url:<br />
                {sku}, {sku_lower}, {sku_upper}
                <small v-if="(v$.item.datasheet_url.$invalid && submitted) || v$.item.datasheet_url.$pending.$response" class="p-error">
                  <br />
                  {{ v$.item.datasheet_url.url.$message }}
                  <template v-if="v$.item.datasheet_url.url && v$.item.datasheet_url.maxLength"><br /></template>
                  {{ v$.item.datasheet_url.maxLength.$message }}
                </small>
              </div>

              <div class="col-6">
                <label
                  for="aliases"
                  :class="{
                    block: true,
                    'p-error': v$.item.aliases.$invalid && submitted,
                    'w-10': true,
                    'mt-3': true,
                  }"
                  >Aliases (comma separated values)</label
                >
                <InputText
                  ref="aliases"
                  v-model="item.aliases"
                  input-id="aliases"
                  type="text"
                  placeholder="aliases"
                  :class="{
                    'p-invalid': v$.item.aliases.$invalid && submitted,
                    'w-full': true,
                  }" />
                <small v-if="(v$.item.aliases.$invalid && submitted) || v$.item.aliases.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.item.aliases.maxLength.$message }}
                </small>
              </div>

              <div class="col-6">
                <PvButton type="submit" label="Save" @click.prevent="submit(!v$.$invalid)" />
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, email, url, maxLength } from "@vuelidate/validators";
import { mapState } from "pinia";
import { useServerStore } from "@/stores/server";
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
      address: "",
      url: "",
      email: "",
      comment: "",
      phone: "",
      fax: "",
      logo: null,
      datasheet_url: "",
      aliases: "",
    },
    submitted: false,
  }),
  created() {
    this.mode = this.dialogRef.data.mode; // add / edit
    if (this.dialogRef.data.item) {
      this.item = {
        id: this.dialogRef.data.item.id,
        name: this.dialogRef.data.item.name,
        address: this.dialogRef.data.item.address,
        url: this.dialogRef.data.item.url,
        email: this.dialogRef.data.item.email,
        comment: this.dialogRef.data.item.comment,
        phone: this.dialogRef.data.item.phone,
        fax: this.dialogRef.data.item.fax,
        hasLogo: this.dialogRef.data.item.logo,
        datasheet_url: this.dialogRef.data.item.datasheet_url,
        aliases: this.dialogRef.data.item.aliases,
      };
    }
  },
  validations: {
    item: {
      name: { required, maxLength: maxLength(255) },
      address: {},
      url: { url, maxLength: maxLength(255) },
      datasheet_url: { url, maxLength: maxLength(255) },
      email: { email, maxLength: maxLength(255) },
      comment: {},
      phone: { maxLength: maxLength(255) },
      fax: { maxLength: maxLength(255) },
      logo: {},
      aliases: { maxLength: maxLength(255) },
    },
  },
  computed: {
    ...mapState(useServerStore, {
      allowedUploadTypes: (store) => {
        let types = store.settings.partAttachmentAllowedTypes || ["image/png", "image/jpeg"];
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
      let manufacturer = {
        name: this.item.name,
        address: this.item.address,
        url: this.item.url,
        email: this.item.email,
        comment: this.item.comment,
        phone: this.item.phone,
        fax: this.item.fax,
        logo: this.item.realLogo,
        datasheet_url: this.item.datasheet_url,
        aliases: this.item.aliases,
      };

      apiService
        .createManufacturer(manufacturer)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Manufacturer",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Manufacturer",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with manufacturer saving", err);
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      let manufacturer = {
        name: this.item.name,
        address: this.item.address,
        url: this.item.url,
        email: this.item.email,
        comment: this.item.comment,
        phone: this.item.phone,
        fax: this.item.fax,
        datasheet_url: this.item.datasheet_url,
        aliases: this.item.aliases,
      };

      if (this.item.realLogo) {
        manufacturer.logo = this.item.realLogo;
      }

      apiService
        .updateManufacturer(this.item.id, manufacturer)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Manufacturer",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Manufacturer",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with manufacturer update", err);
          this.dialogRef.close({ finished: true });
        });
    },
    logoFileChanged(files) {
      this.item.realLogo = files[0];
    },
    addAlias(event) {
      this.item.parts_manufacturers_alias.push({
        alias: "",
      });
    },
    deleteAlias(event, idx) {
      this.item.parts_manufacturers_alias.splice(idx, 1);
    },
  },
};
</script>
