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
            placeholder="Capacitor XXX"
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
          <Divider />
          <div v-for="(_, i) in item.part_parameters_presets" :key="i">
            <PartParametersPresetEntry
              v-model:item="item.part_parameters_presets[i]"
              :submitted="submitted"
              @deleteItem="deletePartParameter($event, i)"
            />
            <Divider />
          </div>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <Button
            @click.prevent="addPartParameter($event)"
            class="p-button-help"
            label="add item"
          />
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
import { required, maxLength } from "@vuelidate/validators";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import PartParametersPresetEntry from "@/components/parts/PartParametersPresetEntry.vue";

export default {
  inject: ["dialogRef"],
  components: {
    PartParametersPresetEntry,
  },
  data: () => ({
    mode: null,
    item: {
      name: "",
      part_parameters_presets: [],
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
        part_parameters_presets:
          this.dialogRef.data.item.part_parameters_presets.map((x) => {
            return {
              id: x.id,
              name: x.name,
              description: x.description,
              unit: x.unit ? x.unit.id : null,
            };
          }),
      };
    }
  },
  validations: {
    item: {
      name: { required, maxLength: maxLength(255) },
    },
  },
  computed: {},
  methods: {
    addPartParameter(event) {
      this.item.part_parameters_presets.push({
        name: "",
        description: "",
        value: "",
        unit: null,
      });
    },
    deletePartParameter(event, idx) {
      this.item.part_parameters_presets.splice(idx, 1);
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
      let part_unit = {
        name: this.item.name,
        part_parameters_presets: this.item.part_parameters_presets,
      };

      apiService
        .createPartParameterPresets(part_unit)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Parameters preset",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Parameters preset",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error(
            "Error with part parameters presets saving",
            err
          );
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      let part_unit = {
        name: this.item.name,
        part_parameters_presets: this.item.part_parameters_presets,
      };

      apiService
        .updatePartParameterPresets(this.item.id, part_unit)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Parameters preset",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Parameters preset",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error(
            "Error with part parameters presets update",
            err
          );
          this.dialogRef.close({ finished: true });
        });
    },
  },
};
</script>
