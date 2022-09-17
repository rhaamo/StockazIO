<template>
  <div>
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
          autofocus
          v-focus
          ref="name"
          inputId="name"
          type="text"
          v-model="item.name"
          :class="{
            'p-invalid': v$.item.name.$invalid && submitted,
            'w-10': true,
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
          inputId="logo"
          type="file"
          v-model="item.logo"
          @change="logoFileChanged($event.target.files)"
          :class="{
            'p-invalid': v$.item.logo.$invalid && submitted,
            'w-10': true,
          }"
          :accept="allowedUploadTypes"
        />
        <small
          v-if="
            (v$.item.logo.$invalid && submitted) ||
            v$.item.logo.$pending.$response
          "
          class="p-error"
        >
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
        <Textarea
          v-focus
          ref="address"
          inputId="address"
          type="text"
          v-model="item.address"
          :class="{
            'p-invalid': v$.item.address.$invalid && submitted,
            'w-10': true,
          }"
        />
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
        <Textarea
          v-focus
          ref="comment"
          inputId="comment"
          type="text"
          v-model="item.comment"
          :class="{
            'p-invalid': v$.item.comment.$invalid && submitted,
            'w-10': true,
          }"
        />
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
          inputId="url"
          type="url"
          v-model="item.url"
          placeholder="http://somewhere/"
          :class="{
            'p-invalid': v$.item.url.$invalid && submitted,
            'w-10': true,
          }"
        />
        <small
          v-if="
            (v$.item.url.$invalid && submitted) ||
            v$.item.url.$pending.$response
          "
          class="p-error"
        >
          {{ v$.item.url.url.$message }}
          <template v-if="v$.item.url.url && v$.item.url.maxLength"
            ><br
          /></template>
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
          inputId="phone"
          type="text"
          v-model="item.phone"
          :class="{
            'p-invalid': v$.item.phone.$invalid && submitted,
            'w-10': true,
          }"
        />
        <small
          v-if="
            (v$.item.phone.$invalid && submitted) ||
            v$.item.phone.$pending.$response
          "
          class="p-error"
        >
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
          inputId="email"
          type="email"
          v-model="item.email"
          :class="{
            'p-invalid': v$.item.email.$invalid && submitted,
            'w-10': true,
          }"
        />
        <small
          v-if="
            (v$.item.email.$invalid && submitted) ||
            v$.item.email.$pending.$response
          "
          class="p-error"
        >
          {{ v$.item.email.email.$message }}
          <template v-if="v$.item.email.email && v$.item.email.maxLength"
            ><br
          /></template>
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
          inputId="fax"
          type="text"
          v-model="item.fax"
          :class="{
            'p-invalid': v$.item.fax.$invalid && submitted,
            'w-10': true,
          }"
        />
        <small
          v-if="
            (v$.item.fax.$invalid && submitted) ||
            v$.item.fax.$pending.$response
          "
          class="p-error"
        >
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
          inputId="datasheet_url"
          type="url"
          v-model="item.datasheet_url"
          placeholder="http://somewhere/{sku}.pdf"
          :class="{
            'p-invalid': v$.item.datasheet_url.$invalid && submitted,
            'w-10': true,
          }"
        />
        <small
          v-if="
            (v$.item.datasheet_url.$invalid && submitted) ||
            v$.item.datasheet_url.$pending.$response
          "
          class="p-error"
        >
          {{ v$.item.datasheet_url.url.$message }}
          <template
            v-if="v$.item.datasheet_url.url && v$.item.datasheet_url.maxLength"
            ><br
          /></template>
          {{ v$.item.datasheet_url.maxLength.$message }}
        </small>
      </div>

      <div class="col-6 pt-5">
        You can uses the following template in the datasheet url:<br />
        {sku}, {sku_lower}, {sku_upper}
      </div>

      <div class="col-6">
        <Button label="Save" @click.prevent="submit(!v$.$invalid)" />
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
        address: this.dialogRef.data.item.address,
        url: this.dialogRef.data.item.url,
        email: this.dialogRef.data.item.email,
        comment: this.dialogRef.data.item.comment,
        phone: this.dialogRef.data.item.phone,
        fax: this.dialogRef.data.item.fax,
        hasLogo: this.dialogRef.data.item.logo,
        datasheet_url: this.dialogRef.data.item.datasheet_url,
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
      let distributor = {
        name: this.item.name,
        address: this.item.address,
        url: this.item.url,
        email: this.item.email,
        comment: this.item.comment,
        phone: this.item.phone,
        fax: this.item.fax,
        logo: this.item.realLogo,
        datasheet_url: this.item.datasheet_url,
      };

      apiService
        .createDistributor(distributor)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Distributor",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Distributor",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with distributor saving", err);
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      let distributor = {
        name: this.item.name,
        address: this.item.address,
        url: this.item.url,
        email: this.item.email,
        comment: this.item.comment,
        phone: this.item.phone,
        fax: this.item.fax,
        datasheet_url: this.item.datasheet_url,
      };

      if (this.item.realLogo) {
        distributor.logo = this.item.realLogo;
      }

      apiService
        .updateDistributor(this.item.id, distributor)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Distributor",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Distributor",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with distributor update", err);
          this.dialogRef.close({ finished: true });
        });
    },
    logoFileChanged(files) {
      this.item.realLogo = files[0];
    },
  },
};
</script>
