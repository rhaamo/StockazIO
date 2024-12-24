<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div>
      <ul class="list-none">
        <li>
          <router-link to="#" title="Bulk-generate labels" @click.prevent="showBulkLabelGenerator()" class="no-underline">
            <i class="fa fa-qrcode" aria-hidden="true" /> Bulk-generate labels
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
  data: () => ({
    breadcrumb: {
      home: {
        icon: "pi pi-home",
        command: () => {
          this.$router.push({ name: "home" });
        },
      },
      items: [
        {
          label: "Storages management",
          command: () => {
            this.$router.push({ name: "view-storage-tree" });
          },
        },
      ],
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
        },
        templates: {
          header: () => {
            return [h("h3", [h("i", { class: "fa fa-qrcode mr-1" }), h("span", "Label Generator")])];
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
