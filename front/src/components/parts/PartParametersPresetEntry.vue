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
          ref="name"
          inputId="name"
          type="text"
          v-model="item.name"
          placeholder="Value name"
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
          for="description"
          :class="{
            block: true,
            'p-error': v$.item.description.$invalid && submitted,
            'w-10': true,
          }"
          >Description</label
        >
        <InputText
          ref="description"
          inputId="description"
          type="text"
          v-model="item.description"
          placeholder="Description"
          :class="{
            'p-invalid': v$.item.description.$invalid && submitted,
            'w-10': true,
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
      </div>
    </div>

    <div class="grid">
      <div class="col-12">
        <label for="unit" class="block">Unit</label>
        <Dropdown
          inputId="unit"
          v-model="item.unit"
          class="w-11"
          :options="choicesPartUnit"
          optionLabel="text"
          optionValue="value"
          :filter="true"
        />
      </div>
    </div>

    <div class="mt-2">
      <ButtonDeleteInline
        size="p-button-sm"
        btn-variant-main="p-button-danger"
        btn-variant-ok="p-button-success"
        btn-variant-cancel="p-button-danger"
        btn-main-text="remove item"
        btn-main-text-disabled="Confirm ?"
        btn-ok-text="Yes"
        btn-cancel-text="No"
        @action-confirmed="$emit('deleteItem', $event)"
      />
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";
import { mapState } from "pinia";
import { usePreloadsStore } from "@/stores/preloads";

export default {
  props: {
    item: { type: Object, required: true },
    submitted: { type: Boolean, required: true },
  },
  data: () => ({}),
  setup: () => ({
    v$: useVuelidate(),
    preloadsStore: usePreloadsStore(),
  }),
  model: {
    prop: "item",
    event: "change",
  },
  computed: {
    ...mapState(usePreloadsStore, {
      choicesPartUnit: (store) =>
        store.parameters_unit.map((x) => {
          return { value: x.id, text: `${x.name} (${x.symbol})` };
        }),
    }),
  },
  validations: {
    item: {
      name: {
        required,
        maxLength: maxLength(255),
      },
      description: {
        maxLength: maxLength(255),
      },
      unit: {},
    },
  },
};
</script>
