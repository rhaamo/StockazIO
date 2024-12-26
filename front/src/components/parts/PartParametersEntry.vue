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
          v-model="item.name"
          input-id="name"
          type="text"
          placeholder="Value name"
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
          v-model="item.description"
          input-id="description"
          type="text"
          placeholder="Description"
          :class="{
            'p-invalid': v$.item.description.$invalid && submitted,
            'w-10': true,
          }" />
        <small v-if="(v$.item.description.$invalid && submitted) || v$.item.description.$pending.$response" class="p-error">
          {{ v$.item.description.maxLength.$message }}
        </small>
      </div>
    </div>

    <div class="grid">
      <div class="col-6">
        <label
          for="value"
          :class="{
            block: true,
            'p-error': v$.item.value.$invalid && submitted,
            'w-10': true,
          }"
          >Value*</label
        >
        <InputText
          ref="value"
          v-model="item.value"
          input-id="value"
          type="text"
          placeholder="42"
          :class="{
            'p-invalid': v$.item.value.$invalid && submitted,
            'w-10': true,
          }" />
        <small v-if="(v$.item.value.$invalid && submitted) || v$.item.value.$pending.$response" class="p-error"
          ><br />
          {{ v$.item.value.required.$message }}
          <template v-if="v$.item.value.required && v$.item.value.maxLength"><br /></template>
          {{ v$.item.value.maxLength.$message }}
        </small>
      </div>

      <div class="col-6">
        <label for="unit" class="block">Unit</label>
        <Dropdown
          v-model="item.unit"
          input-id="unit"
          class="w-10"
          :options="choicesPartUnit"
          option-label="text"
          option-value="value"
          :filter="true" />
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
        @action-confirmed="$emit('deleteItem', $event)" />
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";
import { mapState } from "pinia";
import { usePreloadsStore } from "@/stores/preloads";

export default {
  model: {
    prop: "item",
    event: "change",
  },
  props: {
    item: { type: Object, required: true },
    submitted: { type: Boolean, required: true },
  },
  setup: () => ({
    v$: useVuelidate(),
    preloadsStore: usePreloadsStore(),
  }),
  data: () => ({}),
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
      value: {
        required,
        maxLength: maxLength(255),
      },
      unit: {},
    },
  },
};
</script>
