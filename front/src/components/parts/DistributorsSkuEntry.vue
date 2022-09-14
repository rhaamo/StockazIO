<template>
  <div>
    <div class="grid">
      <div class="col-6">
        <label
          for="sku"
          :class="{
            block: true,
            'p-error': v$.item.sku.$invalid && submitted,
            'w-10': true,
          }"
          >Name*</label
        >
        <InputText
          ref="`sku"
          inputId="sku"
          type="text"
          v-model="item.sku"
          placeholder="SKU_ID"
          :class="{
            'p-invalid': v$.item.sku.$invalid && submitted,
            'w-10': true,
          }"
          @input="updateDatasheetUrl"
        />
        <small
          v-if="
            (v$.item.sku.$invalid && submitted) ||
            v$.item.sku.$pending.$response
          "
          class="p-error"
          ><br />
          {{ v$.item.sku.required.$message }}
          <template v-if="v$.item.sku.required && v$.item.sku.maxLength"
            ><br
          /></template>
          {{ v$.item.sku.maxLength.$message }}
        </small>
      </div>

      <div class="col-6">
        <label for="distributor" class="block">Distributor</label>
        <Dropdown
          inputId="distributor"
          v-model="item.distributor"
          class="w-10"
          :options="choicesDistributors"
          optionLabel="text"
          :filter="true"
          @change="updateDatasheetUrl"
        />
      </div>
    </div>

    <div>
      <label
        for="datasheet_url"
        :class="{
          block: true,
          'p-error': v$.item.datasheet_url.$invalid && submitted,
          'w-11': true,
        }"
        >Datsheet URL</label
      >
      <InputText
        ref="datasheet_url"
        inputId="datasheet_url"
        type="text"
        v-model="item.datasheet_url"
        placeholder="http://somewhere/"
        :class="{
          'p-invalid': v$.item.datasheet_url.$invalid && submitted,
          'w-11': true,
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
      </small>
    </div>

    <div class="mt-2">
      <Button
        @click.prevent="$emit('deleteItem', $event)"
        label="remove item"
        class="p-button-danger"
      />
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength, url } from "@vuelidate/validators";
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
      choicesDistributors: (store) =>
        store.distributors.map((x) => {
          return { value: x.id, text: x.name, datasheet_url: x.datasheet_url };
        }),
    }),
  },
  validations: {
    item: {
      sku: {
        required,
        maxLength: maxLength(255),
      },
      distributor: {
        required,
      },
      datasheet_url: {
        url,
      },
    },
  },
  methods: {
    replaceUrl(url, sku) {
      if (
        url.includes("{sku}") ||
        url.includes("{sku_lower}") ||
        url.includes("{sku_upper}")
      ) {
        url = url.replaceAll("{sku}", sku);
        url = url.replaceAll("{sku_lower}", sku.toLowerCase());
        url = url.replaceAll("{sku_upper}", sku.toUpperCase());
        return url;
      }
      return url;
    },
    updateDatasheetUrl() {
      if (!this.item.distributor) {
        return;
      }

      if (this.item.sku) {
        if (this.item.datasheet_url) {
          this.item.datasheet_url = this.replaceUrl(
            this.item.distributor.datasheet_url,
            this.item.sku
          );
        }
      } else {
        this.item.datasheet_url = this.item.distributor.datasheet_url;
      }
    },
  },
};
</script>
