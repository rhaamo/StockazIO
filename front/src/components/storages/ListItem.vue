<template>
  <div>
    <ul class="list-none mt-1">
      <li class="mt-1 list-none">
        <i class="pi pi-ellipsis-h" aria-hidden="true" /><span class="ml-2">{{ item.name }}</span>

        <template v-if="item.picture">
          <i
            :id="item.uuid"
            v-tooltip.bottom="`Click to show picture`"
            class="pi pi-image ml-2"
            aria-hidden="true"
            @click.prevent="$refs.storage_picture.toggle($event)" />
          <OverlayPanel id="storage_picture" ref="storage_picture" append-to="body" :show-close-icon="true">
            <PvImage preview width="250" :src="item.picture_medium"></PvImage>
          </OverlayPanel>
        </template>

        &nbsp;&nbsp;

        <router-link v-tooltip.bottom="`QrCode label generator`" to="#" class="no-underline" @click.prevent="showLabelGeneratorModal(item)">
          <i class="pi pi-qrcode" aria-hidden="true" />
        </router-link>

        <template v-if="!readonly">
          &nbsp;&nbsp;

          <router-link v-tooltip.bottom="`Edit Element`" to="#" class="no-underline" @click.prevent="editElementModal(item)">
            <i class="pi pi-pencil" aria-hidden="true" />
          </router-link>
          &nbsp;
          <router-link v-tooltip.bottom="`Delete Element`" to="#" class="no-underline" @click.prevent="deleteElementModal(item)">
            <i class="pi pi-trash" aria-hidden="true" />
          </router-link>

          &nbsp;&nbsp;

          <router-link v-tooltip.bottom="`${addElementTitle(item.name)}`" to="#" class="no-underline" @click.prevent="addElementModal(item.id)">
            <i class="pi pi-plus" aria-hidden="true" />
          </router-link>
        </template>
        <br />
        <template v-if="item.description"
          ><span class="pi pi-comment ml-4" v-tooltip.left="'Storage description'"></span> {{ item.description }}
        </template>
      </li>
      <ListItem v-for="category in item.children" :key="category.uuid" :item="category" :level="level + 1" :readonly="readonly" />
    </ul>
  </div>
</template>

<script>
import { h } from "vue";
import ManageItemDialog from "@/components/storages/ManageLocation.vue";
import LabelGeneratorModal from "@/components/label/generator.vue";
import apiService from "@/services/api/api.service";
import logger from "@/logging";
import { useToast } from "primevue/usetoast";
import { usePreloadsStore } from "@/stores/preloads";
import { useConfirm } from "primevue/useconfirm";

export default {
  components: {},
  props: {
    item: Object,
    level: Number,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  setup: () => ({
    toast: useToast(),
    preloadsStore: usePreloadsStore(),
    confirm: useConfirm(),
  }),
  methods: {
    addElementTitle(name) {
      return `Add element under '${name}'`;
    },
    fetchStorages() {
      logger.default.info("reloading storages");
      apiService
        .getStorages()
        .then((val) => {
          this.preloadsStore.setStorages(val.data);
          this.preloadsStore.setLastUpdate("storages", new Date());
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Storages",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching storages", err);
        });
    },
    showLabelGeneratorModal(item) {
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
          items: [this.item],
          kind: "storage",
        },
      });
    },
    editElementModal(item) {
      this.$dialog.open(ManageItemDialog, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit element")])];
          },
        },
        data: {
          id: item.id,
          name: item.name,
          parent_id: { [item.parent]: true },
          picture: item.picture,
          description: item.description,
          mode: "edit",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload storages
            this.fetchStorages();
          }
        },
      });
    },
    deleteElementModal(item) {
      this.confirm.require({
        message: `Are you sure you want to delete the element '${item.name}' ?`,
        icon: "pi pi-exclamation-triangle",
        rejectProps: {
          label: "Cancel",
          severity: "secondary",
          outlined: true,
        },
        acceptProps: {
          label: "Delete",
          severity: "danger",
        },
        accept: () => {
          apiService
            .deleteStorageLocation(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Storage location",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchStorages();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Storage location",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with storage element deletion", err);
              this.fetchStorages();
            });
        },
        reject: () => {
          return;
        },
      });
    },
    addElementModal(id) {
      this.$dialog.open(ManageItemDialog, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add element")])];
          },
        },
        data: {
          name: "",
          parent_id: { [id]: true },
          mode: "add",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload storages
            this.fetchStorages();
          }
        },
      });
    },
  },
};
</script>
