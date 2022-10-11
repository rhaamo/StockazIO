<template>
  <div>
    <ul class="list-none mt-1">
      <li class="mt-1 list-none">
        <i class="fa fa-ellipsis-h" aria-hidden="true" /> {{ item.name }}

        <template v-if="item.picture">
          &nbsp;
          <i
            :id="item.uuid"
            class="fa fa-file-image-o"
            aria-hidden="true"
            v-tooltip="`Click to show picture`"
            @click.prevent="$refs.storage_picture.toggle($event)"
          />
          <OverlayPanel
            ref="storage_picture"
            appendTo="body"
            :showCloseIcon="true"
            id="storage_picture"
          >
            <PvImage preview width="250" :src="item.picture_medium"></PvImage>
          </OverlayPanel>
        </template>

        &nbsp;&nbsp;

        <router-link
          to="#"
          v-tooltip="`QrCode label generator`"
          @click.prevent="showLabelGeneratorModal(item)"
          class="no-underline"
        >
          <i class="fa fa-qrcode" aria-hidden="true" />
        </router-link>

        <template v-if="!readonly">
          &nbsp;&nbsp;

          <router-link
            to="#"
            v-tooltip="`Edit Element`"
            @click.prevent="editElementModal(item)"
            class="no-underline"
          >
            <i class="fa fa-pencil-square-o" aria-hidden="true" />
          </router-link>
          &nbsp;
          <router-link
            to="#"
            v-tooltip="`Delete Element`"
            @click.prevent="deleteElementModal(item)"
            class="no-underline"
          >
            <i class="fa fa-trash-o" aria-hidden="true" />
          </router-link>

          &nbsp;&nbsp;

          <router-link
            to="#"
            v-tooltip="`${addElementTitle(item.name)}`"
            @click.prevent="addElementModal(item.id)"
            class="no-underline"
          >
            [add sub element]
          </router-link>
        </template>
        <br />
        <template v-if="item.description">
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&raquo; {{ item.description }}
        </template>
      </li>
      <ListItem
        v-for="category in item.children"
        :key="category.uuid"
        :item="category"
        :level="level + 1"
        :readonly="readonly"
      />
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
        },
        templates: {
          header: () => {
            return [
              h("h3", [
                h("i", { class: "fa fa-qrcode mr-1" }),
                h("span", "Label Generator"),
              ]),
            ];
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
        header: `Deleting '${item.name}' ?`,
        icon: "fa fa-exclamation-triangle",
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
