<template>
  <div>
    <form @submit.prevent="submit(!v$.$invalid)" v-if="projectsLoaded">
      <div class="flex justify-content-center">
        <div class="flex flex-grow-1 align-items-center justify-content-center">
          <div class="field w-10">
            <label
              for="name"
              :class="{
                block: true,
                'p-error': v$.item.project.$invalid && submitted,
              }"
              fluid
              >Project</label
            >
            <Dropdown
              v-model="item.project"
              :options="projects"
              filter
              optionLabel="name"
              optionValue="id"
              placeholder="Select a Project"
              fluid
              :invalid="v$.item.project.$invalid && submitted"></Dropdown>
            <small v-if="(v$.item.project.$invalid && submitted) || v$.item.project.$pending.$response" class="p-error"
              ><br />
              {{ v$.item.project.required.$message }}
            </small>
          </div>
        </div>
      </div>

      <div class="flex justify-content-center">
        <div class="flex flex-grow-1 align-items-center justify-content-center">
          <div class="field w-10">
            <label
              for="quantity"
              :class="{
                block: true,
                'p-error': v$.item.quantity.$invalid && submitted,
              }"
              fluid
              >Quantity</label
            >
            <InputNumber
              ref="quantity"
              v-model="item.quantity"
              input-id="quantity"
              placeholder="What does it do ?"
              fluid
              :invalid="v$.item.quantity.$invalid && submitted"
              :min="0"
              showButtons
              buttonLayout="horizontal" />
          </div>
        </div>
      </div>

      <div class="flex justify-content-center">
        <div class="flex flex-grow-1 align-items-center justify-content-center">
          <div class="field-checkbox w-10">
            <Checkbox v-model="item.sourced" :invalid="v$.item.sourced.$invalid && submitted" input-id="sourced" :binary="true" />
            <label
              for="sourced"
              :class="{
                'p-error': v$.item.sourced.$invalid && submitted,
              }"
              >Sourced</label
            >
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
              }"
              fluid
              >Notes</label
            >
            <InputText ref="notes" v-model="item.notes" input-id="notes" type="text" :invalid="v$.item.notes.$invalid && submitted" fluid />
            <small v-if="(v$.item.notes.$invalid && submitted) || v$.item.notes.$pending.$response" class="p-error"
              ><br />
              {{ v$.item.notes.maxLength.$message }}
            </small>
          </div>
        </div>
      </div>

      <div class="flex justify-content-center">
        <div class="flex flex-grow-1 align-items-center justify-content-center">
          <div class="field w-10">
            <PvButton type="submit" label="Add" @click.prevent="submit(!v$.$invalid)" />
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, minValue, maxLength } from "@vuelidate/validators";
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
      project: null,
      quantity: 0,
      sourced: false,
      notes: "",
    },
    part: null,
    submitted: false,
    projects: [],
    totalRecords: 0,
    projectsLoaded: false,
  }),
  created() {
    this.loadLazyData();

    if (this.dialogRef.data.part) {
      this.part = this.dialogRef.data.part;
    }
  },
  validations: {
    item: {
      project: {
        required,
      },
      quantity: {
        minValue: minValue(0),
      },
      sourced: {},
      notes: { maxLength: maxLength(255) },
    },
  },
  computed: {},
  methods: {
    loadLazyData() {
      apiService
        .getProjects()
        .then((res) => {
          this.projects = res.data;
          this.totalRecords = res.data.length;
          this.projectsLoaded = true;
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Projects list",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching projects", err);
        });
    },
    submit(isFormValid) {
      this.submitted = true;
      if (!isFormValid) {
        return;
      }
      this.save();
    },
    save() {
      let datas = {
        part: this.part.id,
        qty: this.item.quantity,
        sourced: this.item.sourced,
        notes: this.item.notes,
        project: this.item.project,
      };

      apiService
        .projectAddPart(this.item.project, datas)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Add part to project",
            detail: "Added with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true, item: this.item });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Add part to project",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with project saving", err);
          this.dialogRef.close({ finished: true, error: true, item: this.item });
        });
    },
  },
};
</script>
