<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />

    <div class="grid mt-2">
      <div class="col-2">
        <PvMenu :model="templatesList" @blur.stop="null" />
      </div>

      <div class="col-6">
        <h1 v-if="!form.id">Add new label template</h1>
        <h1 v-else>{{ form.name }}</h1>
        <form @submit.prevent="submit(!v$.$invalid)">
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
              ref="name"
              v-model="form.name"
              v-focus
              autofocus
              input-id="name"
              type="text"
              placeholder="Brother 69x42mm"
              :class="{
                'p-invalid': v$.form.name.$invalid && submitted,
                'w-full': true,
              }" />
            <small v-if="(v$.form.name.$invalid && submitted) || v$.form.name.$pending.$response" class="p-error"
              ><br />
              {{ v$.form.name.required.$message }}
              <template v-if="v$.form.name.required && v$.form.name.maxLength"><br /></template>
              {{ v$.form.name.maxLength.$message }}
            </small>
          </div>

          <div class="grid mt-2">
            <div class="col-3">
              <label
                for="width"
                :class="{
                  block: true,
                  'p-error': v$.form.width.$invalid && submitted,
                }"
                >Width</label
              >
              <InputNumber
                v-model="form.width"
                input-id="width"
                mode="decimal"
                show-buttons
                :min="0"
                placeholder="69"
                :invalid="v$.form.width.$invalid && submitted" />
              <small v-if="(v$.form.width.$invalid && submitted) || v$.form.width.$pending.$response" class="p-error"
                ><br />
                {{ v$.form.width.required.$message }}
                <template v-if="v$.form.width.required && v$.form.width.minValue"><br /></template>
                {{ v$.form.width.minValue.$message }}
              </small>
            </div>

            <div class="col-3">
              <label
                for="height"
                :class="{
                  block: true,
                  'p-error': v$.form.height.$invalid && submitted,
                }"
                >Height</label
              >
              <InputNumber
                v-model="form.height"
                input-id="height"
                mode="decimal"
                show-buttons
                :min="0"
                placeholder="42"
                :invalid="v$.form.height.$invalid && submitted" />
              <small v-if="(v$.form.height.$invalid && submitted) || v$.form.height.$pending.$response" class="p-error"
                ><br />
                {{ v$.form.height.required.$message }}
                <template v-if="v$.form.height.required && v$.form.height.minValue"><br /></template>
                {{ v$.form.height.minValue.$message }}
              </small>
            </div>
            <div class="col-3">
              <label
                for="height"
                :class="{
                  block: true,
                  'p-error': v$.form.height.$invalid && submitted,
                }"
                >Set as default</label
              >
              <ToggleSwitch class="mt-1" v-model="form.default" />
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
              v-model="form.template"
              input-id="template"
              type="text"
              :class="{
                'p-invalid': v$.form.template.$invalid && submitted,
                'w-full': true,
              }"
              rows="10" />
            <small v-if="(v$.form.template.$invalid && submitted) || v$.form.template.$pending.$response" class="p-error"
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
              >Description Template</label
            >
            <PvTextarea
              ref="text_template"
              v-model="form.text_template"
              input-id="text_template"
              type="text"
              :class="{
                'p-invalid': v$.form.text_template.$invalid && submitted,
                'w-full': true,
              }"
              rows="5" />
            <small v-if="(v$.form.text_template.$invalid && submitted) || v$.form.text_template.$pending.$response" class="p-error"
              ><br />
              {{ v$.form.text_template.required.$message }}
            </small>
          </div>

          <div class="mt-2">
            <PvButton type="submit" label="Save" @click.prevent="submit(!v$.$invalid)" />
            <template v-if="selectedTemplate && 'id' in selectedTemplate && selectedTemplate.id != 0">
              <PvButton label="Delete" class="p-button-danger ml-2" @click.prevent="deleteItem" />
            </template>
          </div>
        </form>
      </div>

      <div class="col-4">
        The template is a JSON as string, you can look at
        <a href="https://pdfme.com/docs/getting-started#sample-template" target="_blank">this doc</a>
        for the exact schema syntax.<br />
        You can also checkout the <a href="https://github.com/rhaamo/StockazIO/tree/master/docs" target="_blank">docs</a> folder for the template
        files to uses with <a href="https://pdfme.com/template-design" target="_blank">this online designer</a>.<br />
        Please note that, currently, only three elements can use substitutions.<br />
        The QrCode element needs to be called "qrcode", and the description "description", the name will stays as the plain name (full storage path
        for storage).<br />
        The following list will show available substitutions.<br />
        You can add other fixed elements if wanted.<br /><br /><br />
        The following substitutions for the Description Template is available, depending if it's a Storage Location or Part:
        <ul>
          <li>Both Part and Storage:</li>
          <li><code>{name}</code> Name of the element</li>
          <li><code>{description}</code> Description of the element</li>
          <li><code>{qrcode}</code> QrCode of the element</li>
          <li class="mt-4">For Parts only:</li>
          <li><code>{category_name}</code> Name of the category (if any) of the item</li>
          <li><code>{category_path}</code> Full path of the category (if any) of the item</li>
          <li><code>{storage_name}</code> Name of the storage (if any) of the item</li>
          <li><code>{storage_path}</code> Full path of the storage (if any) of the item</li>
          <li><code>{footprint}</code> Footprint value</li>
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
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
    v$: useVuelidate(),
  }),
  data: () => ({
    submitted: false,
    selectedTemplate: null,
    form: {
      id: null,
      name: "",
      default: false,
      height: 42,
      width: 69,
      template: "",
      text_template: "",
    },
  }),
  created() {
    this.selectedTemplate = null;
  },
  validations: {
    form: {
      name: { required, maxLength: maxLength(255) },
      default: { required },
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
    templatesList() {
      return [
        {
          label: "Add new",
          icon: "pi pi-plus",
          command: () => {
            this.resetForm();
            this.selectedTemplate = null;
          },
        },
        {
          separator: true,
        },
        ...this.labelTemplates.map((x) => {
          return {
            label: x.name,
            icon: `pi ${x.default ? "pi-check" : "pi-receipt"}`,
            command: () => {
              this.form = x;
              this.selectedTemplate = x;
            },
          };
        }),
      ];
    },
    breadcrumb() {
      return {
        home: {
          icon: "pi pi-home",
          command: () => {
            this.$router.push({ name: "home" });
          },
        },
        items: [
          {
            label: "Label Templates",
            command: () => {
              this.$router.push({ name: "label-templates-list" });
            },
          },
        ],
      };
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
        default: false,
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
        default: this.form.default,
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
        default: this.form.default,
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
        icon: "pi pi-exclamation-triangle",
        rejectProps: {
          label: "Cancel",
          severity: "secondary",
          outlined: true,
        },
        acceptProps: {
          label: "Delete",
          severity: "danger",
        },
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
              this.selectedTemplate = null;
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
              this.selectedTemplate = null;
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
