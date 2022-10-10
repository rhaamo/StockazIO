<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />

    <div class="grid mt-2">
      <div class="col-2">
        <Listbox
          v-model="selectedTemplate"
          :options="choicesTemplates"
          optionLabel="name"
          :multiple="false"
          @change="templateChanged($event)"
        />
      </div>

      <div class="col-6">
        <div>
          <label
            for="name"
            :class="{
              block: true,
              'p-error': v$.form.name.$invalid && submitted,
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
            v-model="form.name"
            placeholder="Brother 69x42mm"
            :class="{
              'p-invalid': v$.form.name.$invalid && submitted,
              'w-full': true,
            }"
          />
          <small
            v-if="
              (v$.form.name.$invalid && submitted) ||
              v$.form.name.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.name.required.$message }}
            <template v-if="v$.form.name.required && v$.form.name.maxLength"
              ><br
            /></template>
            {{ v$.form.name.maxLength.$message }}
          </small>
        </div>

        <div class="grid mt-2">
          <div class="col-5">
            <label
              for="width"
              :class="{
                block: true,
                'p-error': v$.form.width.$invalid && submitted,
                'w-full': true,
              }"
              >Width</label
            >
            <InputNumber
              inputId="width"
              mode="decimal"
              showButtons
              :min="0"
              placeholder="69"
              :class="{
                'p-invalid': v$.form.width.$invalid && submitted,
                'w-full': true,
              }"
              v-model="form.width"
            />
            <small
              v-if="
                (v$.form.width.$invalid && submitted) ||
                v$.form.width.$pending.$response
              "
              class="p-error"
              ><br />
              {{ v$.form.width.required.$message }}
              <template v-if="v$.form.width.required && v$.form.width.minValue"
                ><br
              /></template>
              {{ v$.form.width.minValue.$message }}
            </small>
          </div>

          <div class="col-5 col-offset-1">
            <label
              for="height"
              :class="{
                block: true,
                'p-error': v$.form.height.$invalid && submitted,
                'w-full': true,
              }"
              >Height</label
            >
            <InputNumber
              inputId="height"
              mode="decimal"
              showButtons
              :min="0"
              placeholder="42"
              :class="{
                'p-invalid': v$.form.height.$invalid && submitted,
                'w-full': true,
              }"
              v-model="form.height"
            />
            <small
              v-if="
                (v$.form.height.$invalid && submitted) ||
                v$.form.height.$pending.$response
              "
              class="p-error"
              ><br />
              {{ v$.form.height.required.$message }}
              <template
                v-if="v$.form.height.required && v$.form.height.minValue"
                ><br
              /></template>
              {{ v$.form.height.minValue.$message }}
            </small>
          </div>
        </div>

        <div class="mt-2">
          <label
            for="template"
            :class="{
              block: true,
              'p-error': v$.form.template.$invalid && submitted,
              'w-full': true,
            }"
            >Template</label
          >
          <PvTextarea
            ref="template"
            inputId="template"
            type="text"
            v-model="form.template"
            :class="{
              'p-invalid': v$.form.template.$invalid && submitted,
              'w-full': true,
            }"
            rows="10"
          />
          <small
            v-if="
              (v$.form.template.$invalid && submitted) ||
              v$.form.template.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.template.required.$message }}
          </small>
        </div>

        <div class="mt-2">
          <label
            for="text_template"
            :class="{
              block: true,
              'p-error': v$.form.text_template.$invalid && submitted,
              'w-full': true,
            }"
            >Text Template</label
          >
          <PvTextarea
            ref="text_template"
            inputId="text_template"
            type="text"
            v-model="form.text_template"
            :class="{
              'p-invalid': v$.form.text_template.$invalid && submitted,
              'w-full': true,
            }"
            rows="5"
          />
          <small
            v-if="
              (v$.form.text_template.$invalid && submitted) ||
              v$.form.text_template.$pending.$response
            "
            class="p-error"
            ><br />
            {{ v$.form.text_template.required.$message }}
          </small>
        </div>

        <div class="mt-2">
          <Button label="Save" @click.prevent="submit(!v$.$invalid)" />
          <template
            v-if="
              this.selectedTemplate &&
              'id' in this.selectedTemplate &&
              this.selectedTemplate.id != 0
            "
          >
            <Button
              label="Delete"
              class="p-button-danger ml-2"
              @click.prevent="deleteItem"
            />
          </template>
        </div>
      </div>

      <div class="col-4">
        The template is a JSON as string, you can look at
        <a
          href="https://pdfme.com/docs/getting-started#sample-template"
          target="_blank"
          >this doc</a
        >
        for the exact schema syntax.<br />
        Please note that, currently, only two elements can use substitutions.<br />
        The QrCode element needs to be called "qrcode", and the text one "text",
        the following list will show available substitutions.<br />
        You can add other fixed elements if wanted.<br /><br /><br />
        The following substitutions for the Text Template is available,
        depending if it's a Storage Location or Part:
        <ul>
          <li>
            <code>{name}</code> Name of the element
            <small>(storage, part)</small>
          </li>
          <li>
            <code>{description}</code> Description of the element
            <small>(storage, part)</small>
          </li>
          <li>
            <code>{qrcode}</code> QrCode of the element
            <small>(storage, part)</small>
          </li>
          <li>
            <code>{category_name}</code> Name of the parent category (if any) of
            the element <small>(storage)</small>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { useConfirm } from "primevue/useconfirm";
import { mapState } from "pinia";
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength, minValue } from "@vuelidate/validators";

export default {
  data: () => ({
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [
        { label: "Label Templates", to: { name: "label-templates-list" } },
      ],
    },
    submitted: false,
    selectedTemplate: null,
    form: {
      id: null,
      name: "",
      height: 42,
      width: 69,
      template: "",
      text_template: "",
    },
  }),
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
    v$: useVuelidate(),
  }),
  created() {
    this.selectedTemplate = this.choicesTemplates[0];
  },
  validations: {
    form: {
      name: { required, maxLength: maxLength(255) },
      height: {
        required,
        minValue: minValue(0),
      },
      width: {
        required,
        minValue: minValue(0),
      },
      template: { required },
      text_template: { required },
    },
  },
  computed: {
    ...mapState(usePreloadsStore, {
      labelTemplates: (store) => {
        return store.label_templates;
      },
    }),
    choicesTemplates() {
      return [{ id: 0, name: "Add new" }].concat(this.labelTemplates);
    },
  },
  methods: {
    fetchLabelTemplates() {
      apiService
        .getLabelTemplates()
        .then((val) => {
          this.preloadsStore.setLabelTemplates(val.data);
          this.preloadsStore.setLastUpdate("label_templates", new Date());
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Label Templates",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching label templates", err);
        });
    },
    templateChanged(event) {
      if (!event.value) {
        // unselect event : ignore
        return;
      }

      if ("id" in event.value && event.value.id === 0) {
        this.resetForm();
      } else {
        this.form = event.value;
      }
    },
    resetForm() {
      this.form = {
        id: null,
        name: "",
        height: 42,
        width: 69,
        template: "",
        text_template: "",
      };
    },
    submit(isFormValid) {
      this.submitted = true;

      if (!isFormValid) {
        return;
      }

      if ("id" in this.selectedTemplate && this.selectedTemplate.id === 0) {
        this.save();
        this.resetForm();
      } else {
        this.edit();
      }

      this.submitted = false;
    },
    save() {
      let lt = {
        name: this.form.name,
        width: this.form.width,
        height: this.form.height,
        template: this.form.template,
        text_template: this.form.text_template,
      };

      apiService
        .createLabelTemplate(lt)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Label Template",
            detail: "Saved with success",
            life: 5000,
          });
          this.fetchLabelTemplates();
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Label Template",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with label template saving", err);
          this.fetchLabelTemplates();
        });
    },
    edit() {
      let lt = {
        name: this.form.name,
        width: this.form.width,
        height: this.form.height,
        template: this.form.template,
        text_template: this.form.text_template,
      };

      apiService
        .updateLabelTemplate(this.form.id, lt)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Label Template",
            detail: "Updated with success",
            life: 5000,
          });
          this.fetchLabelTemplates();
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Label Template",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with label template update", err);
          this.fetchLabelTemplates();
        });
    },
    deleteItem() {
      this.confirm.require({
        message: `Are you sure you want to delete the template '${this.form.name}' ?`,
        header: `Deleting '${this.form.name}' ?`,
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          apiService
            .deleteLabelTemplate(this.form.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Label Template",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchLabelTemplates();
              this.selectedTemplate = this.choicesTemplates[0];
              this.resetForm();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Label Template",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with label template deletion", err);
              this.fetchLabelTemplates();
              this.selectedTemplate = this.choicesTemplates[0];
              this.resetForm();
            });
        },
        reject: () => {
          return;
        },
      });
    },
  },
};
</script>
