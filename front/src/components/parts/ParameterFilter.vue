<template>
  <div>
    <div class="grid">
      <div class="col-4">
        <label for="name" class="block">Name</label>
        <Dropdown
          inputId="name"
          v-model="item.name"
          class="w-full"
          :options="choicesNames"
          optionLabel="text"
          :filter="true"
        />
        <small
          v-if="v$.item.name.$invalid || v$.item.name.$pending.$response"
          class="p-error"
        >
          {{ v$.item.name.required.$message }}
        </small>
      </div>

      <div class="col-2">
        <label for="mode" class="block">Mode</label>
        <Dropdown
          inputId="mode"
          v-model="item.mode"
          class="w-full"
          :options="choicesModes"
          optionLabel="text"
        />
        <small
          v-if="v$.item.mode.$invalid || v$.item.mode.$pending.$response"
          class="p-error"
        >
          {{ v$.item.mode.required.$message }}
        </small>
      </div>

      <div class="col-4">
        <label
          for="value"
          :class="{
            block: true,
            'p-error': v$.item.value.$invalid,
            'w-full': true,
          }"
          >Value</label
        >
        <InputText
          ref="value"
          inputId="value"
          type="text"
          v-model="item.value"
          placeholder="value"
          :class="{
            'p-invalid': v$.item.value.$invalid,
            'w-full': true,
          }"
        />
        <small
          v-if="v$.item.value.$invalid || v$.item.value.$pending.$response"
          class="p-error"
        >
          {{ v$.item.value.required.$message }}
        </small>
      </div>

      <div class="col-2 pt-4">
        <ButtonDeleteInline
          size="p-button-sm"
          btn-variant-main="p-button-danger"
          btn-variant-ok="p-button-success"
          btn-variant-cancel="p-button-danger"
          btn-main-text="remove filter"
          btn-main-text-disabled="Confirm ?"
          btn-ok-text="Yes"
          btn-cancel-text="No"
          @action-confirmed="$emit('deleteItem', $event)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";

export default {
  props: {
    item: { type: Object, required: true },
    names: { type: Array, required: true },
  },
  data: () => ({}),
  setup: () => ({
    v$: useVuelidate(),
  }),
  model: {
    prop: "item",
    event: "change",
  },
  computed: {
    choicesModes() {
      return [
        { text: "Starts With", value: "startsWith" },
        { text: "Ends With", value: "endsWith" },
        { text: "Contains", value: "contains" },
        { text: "Not contains", value: "notContains" },
        { text: "Not equals", value: "notEquals" },
        { text: "Equals", value: "equals" },
        { text: "Less than", value: "lt" },
        { text: "Less than or equal to", value: "lte" },
        { text: "Greater than", value: "gt" },
        { text: "Greater than or equal to", value: "gte" },
      ];
    },
    choicesNames() {
      return this.names.map((x) => {
        return { text: x, value: x };
      });
    },
  },
  validations: {
    item: {
      name: {
        required,
      },
      mode: {
        required,
      },
      value: {
        required,
      },
    },
  },
  methods: {},
};
</script>
