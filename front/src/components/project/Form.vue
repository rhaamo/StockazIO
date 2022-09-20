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
            placeholder="My cool project"
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
            >Description</label
          >
          <InputText
            ref="description"
            inputId="description"
            type="text"
            v-model="item.description"
            placeholder="What does it do ?"
            :class="{
              'p-invalid': v$.item.description.$invalid && submitted,
              'w-full': true,
            }"
          />
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="notes"
            :class="{
              block: true,
              'p-error': v$.item.notes.$invalid && submitted,
              'w-full': true,
            }"
            >Notes</label
          >
          <InputText
            ref="notes"
            inputId="notes"
            type="text"
            v-model="item.notes"
            placeholder="AAAAAAAAaaaaaaaaa"
            :class="{
              'p-invalid': v$.item.notes.$invalid && submitted,
              'w-full': true,
            }"
          />
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="bom_url"
            :class="{
              block: true,
              'p-error': v$.item.ibom_url.$invalid && submitted,
              'w-full': true,
            }"
            >BOM Url</label
          >
          <InputText
            ref="bom_url"
            inputId="bom_url"
            type="text"
            v-model="item.ibom_url"
            :class="{
              'p-invalid': v$.item.ibom_url.$invalid && submitted,
              'w-full': true,
            }"
          />
          <small
            v-if="
              (v$.item.ibom_url.$invalid && submitted) ||
              v$.item.ibom_url.$pending.$response
            "
            class="p-error"
          >
            {{ v$.item.ibom_url.maxLength.$message }}
          </small>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label for="state" class="block">State</label>
          <Dropdown
            inputId="state"
            v-model="item.state"
            class="w-full"
            :options="choicesStates"
            optionLabel="text"
            optionValue="value"
            :filter="false"
          />
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <label
            for="state_notes"
            :class="{
              block: true,
              'p-error': v$.item.state_notes.$invalid && submitted,
              'w-full': true,
            }"
            >State notes</label
          >
          <InputText
            ref="state_notes"
            inputId="state_notes"
            type="text"
            v-model="item.state_notes"
            placeholder="blocked by X, waiting for Y"
            :class="{
              'p-invalid': v$.item.state_notes.$invalid && submitted,
              'w-full': true,
            }"
          />
          <small
            v-if="
              (v$.item.state_notes.$invalid && submitted) ||
              v$.item.state_notes.$pending.$response
            "
            class="p-error"
          >
            {{ v$.item.state_notes.maxLength.$message }}
          </small>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field-checkbox w-10">
          <Checkbox
            :class="{
              'p-invalid': v$.item.public.$invalid && submitted,
            }"
            inputId="public"
            v-model="item.public"
            :binary="true"
          />
          <label
            for="public"
            :class="{
              'p-error': v$.item.public.$invalid && submitted,
            }"
            >Public project</label
          >
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <p>
            You will be able to add attachments and parts after saving the
            project.
          </p>
        </div>
      </div>
    </div>

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
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength, integer, between } from "@vuelidate/validators";
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
      notes: "",
      ibom_url: "",
      state: 99,
      state_notes: "",
      public: false,
    },
    submitted: false,
    choicesStates: [
      { value: 1, text: "Planned" },
      { value: 2, text: "Ongoing" },
      { value: 3, text: "Finished" },
      { value: 4, text: "On-Hold" },
      { value: 5, text: "Abandonned" },
      { value: 99, text: "Unknown" },
    ],
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
        notes: this.dialogRef.data.item.notes,
        description: this.dialogRef.data.item.description,
        ibom_url: this.dialogRef.data.item.ibom_url,
        state: this.dialogRef.data.item.state,
        state_notes: this.dialogRef.data.item.state_notes,
        public: this.dialogRef.data.item.public,
      };
    }
  },
  validations: {
    item: {
      name: {
        required,
        maxLength: maxLength(255),
      },
      description: {},
      notes: {},
      ibom_url: { maxLength: maxLength(255) },
      state: {
        required,
        integer,
        between: between(0, 99),
      },
      state_notes: {
        maxLength: maxLength(255),
      },
      public: {},
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
      let datas = {
        name: this.item.name,
        description: this.item.description,
        notes: this.item.notes,
        ibom_url: this.item.ibom_url,
        state: this.item.state,
        public: this.item.public,
        state_notes: this.item.state_notes,
      };

      apiService
        .createProject(datas)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Project",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Project",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with project saving", err);
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      let datas = {
        name: this.item.name,
        description: this.item.description,
        notes: this.item.notes,
        ibom_url: this.item.ibom_url,
        state: this.item.state,
        public: this.item.public,
        state_notes: this.item.state_notes,
      };

      apiService
        .updateProject(this.item.id, datas)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Project",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Project",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with project update", err);
          this.dialogRef.close({ finished: true });
        });
    },
  },
};
</script>
