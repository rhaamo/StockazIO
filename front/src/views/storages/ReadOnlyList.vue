<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div>
      <ul class="list-none">
        <li>
          <router-link to="#" title="Bulk-generate labels" class="no-underline" @click.prevent="showBulkLabelGenerator()">
            <i class="pi pi-qrcode" aria-hidden="true" /> Bulk-generate labels
          </router-link>
        </li>
      </ul>
      <template v-for="item in storages">
        <ListItem v-if="item.children" :key="item.id" :item="item" :level="1" :readonly="true" />
      </template>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { mapState } from "pinia";
import { h } from "vue";
import ListItem from "@/components/storages/ListItem.vue";
import LabelGeneratorModal from "@/components/label/generator.vue";

export default {
  components: {
    ListItem,
  },
  setup: () => ({
    preloadsStore: usePreloadsStore(),
  }),
  data: () => ({}),
  computed: {
    ...mapState(usePreloadsStore, {
      storages: (store) => {
        return store.storages;
      },
    }),
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
            label: "Storages list",
            command: () => {
              this.$router.push({ name: "view-storage-tree" });
            },
          },
        ],
      };
    },
  },
  methods: {
    showBulkLabelGenerator() {
      let slocs = [];
      const cb = (e) => {
        slocs.push(e);
        e.children.forEach(cb);
      };
      this.storages.forEach(cb);

      this.$dialog.open(LabelGeneratorModal, {
        props: {
          modal: true,
          style: {
            width: "70vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("i", { class: "pi pi-qrcode mr-1" }), h("span", "Label Generator")])];
          },
        },
        data: {
          items: slocs,
          kind: "storage",
        },
      });
    },
  },
};
</script>
