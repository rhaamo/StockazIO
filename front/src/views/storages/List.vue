<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div>
      <ul class="list-none">
        <li>
          <router-link
            to="#"
            title="Add storage category on root level"
            @click.prevent="showAddCategoryDialog"
            class="no-underline"
          >
            <i class="fa fa-plus-square-o" aria-hidden="true" /> Add root
            category
          </router-link>

          &nbsp;&nbsp;&nbsp;

          <router-link
            to="#"
            title="Bulk-generate labels"
            @click.prevent="showBulkLabelGenerator()"
            class="no-underline"
          >
            <i class="fa fa-qrcode" aria-hidden="true" /> Bulk-generate labels
          </router-link>
        </li>
      </ul>
      <template v-for="item in storages">
        <ListCategory
          v-if="item.children && item.storage_locations"
          :key="item.id"
          :item="item"
          :level="1"
        />
        <ListLocation v-else :key="item.uuid" :item="item" />
      </template>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { mapState } from "pinia";
import ListCategory from "@/components/storages/ListCategory.vue";
import ListLocation from "@/components/storages/ListLocation.vue";

export default {
  components: {
    ListCategory,
    ListLocation,
  },
  data: () => ({
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [{ label: "Storages management" }],
    },
  }),
  setup: () => ({
    preloadsStore: usePreloadsStore(),
  }),
  computed: {
    ...mapState(usePreloadsStore, {
      storages: (store) => {
        return store.storages;
      },
    }),
  },
  methods: {
    showBulkLabelGenerator() {
      console.log("showBulkLabelGenerator");
    },
    showAddCategoryDialog() {
      console.log("showAddCategoryDialog");
    },
  },
};
</script>
