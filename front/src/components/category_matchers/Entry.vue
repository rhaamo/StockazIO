<template>
  <div>
    <div class="grid">
      <div class="col-5">
        <div class="p-inputgroup">
          <IconField>
            <InputIcon>/</InputIcon>
            <InputText
              ref="regexp"
              v-model="item.regexp"
              input-id="regexp"
              type="text"
              :class="{
                'p-invalid': v$.item.regexp.$invalid && submitted,
                'w-full': true,
              }" />
            <InputIcon>/i</InputIcon>
          </IconField>
        </div>

        <small v-if="(v$.item.regexp.$invalid && submitted) || v$.item.regexp.$pending.$response" class="p-error"
          ><br />
          {{ v$.item.regexp.required.$message }}
          <template v-if="v$.item.regexp.required && v$.item.regexp.maxLength"><br /></template>
          {{ v$.item.regexp.maxLength.$message }}
        </small>
      </div>

      <div class="col-3">
        <TreeSelect
          v-model="item.category"
          input-id="category"
          placeholder="Film resistors ? MCUs ?"
          :options="categories"
          selection-mode="single"
          class="w-full"
          :filter="true"
          :fluid="true"
          :show-clear="true" />
        <small v-if="(v$.item.category.$invalid && submitted) || v$.item.category.$pending.$response" class="p-error"
          ><br />
          {{ v$.item.category.required.$message }}
        </small>
      </div>

      <div class="col-2">
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
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";

export default {
  model: {
    prop: "item",
    event: "change",
  },
  props: {
    item: { type: Object, required: true },
    submitted: { type: Boolean, required: true },
    categories: { type: Array, required: true },
  },
  setup: () => ({
    v$: useVuelidate(),
  }),
  validations: {
    item: {
      regexp: {
        required,
        maxLength: maxLength(255),
      },
      category: {
        required,
      },
    },
  },
};
</script>
