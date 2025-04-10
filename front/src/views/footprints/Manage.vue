<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />

    <div class="grid mt-2">
      <div class="col-2">
        <Listbox
          v-model="selectedCategory"
          scroll-height="38rem"
          :options="footprintsCategories"
          option-label="name"
          :multiple="false"
          @change="categoryChanged($event)" />
      </div>

      <div class="col-8 col-offset-1">
        <div class="mb-4">
          <PvButton label="Add category" @click="showAddCategory($event)" />

          <template v-if="selectedCategory">
            <PvButton label="Edit category" class="p-button-secondary ml-2" @click="showEditCategory($event, selectedCategory)" />

            <PvButton label="Delete category" class="p-button-danger ml-2" @click="deleteCategory($event, selectedCategory)" />

            <PvButton label="Add footprint" class="ml-4" @click.prevent="showAddFootprint($event)" />
          </template>
        </div>

        <Divider />

        <div class="mt-4">
          <DataTable
            :value="footprints"
            class="p-datatable-sm"
            striped-rows
            responsive-layout="scroll"
            data-key="id"
            removable-sort
            :paginator="true"
            :rows="20">
            <Column header="Picture">
              <template #body="slotProps">
                <PvImage preview :src="slotProps.data.picture_mini" :alt="slotProps.data.picture" class="product-image" />
              </template>
            </Column>

            <Column field="name" header="Name" :sortable="true"></Column>
            <Column field="description" header="Description"></Column>

            <Column header-style="width: 6.3em">
              <template #body="slotProps">
                <ButtonsEditDelete @edit="showEditFootprint($event, slotProps.data)" @delete="deleteItem($event, slotProps.data)" />
              </template>
            </Column>
          </DataTable>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { useConfirm } from "primevue/useconfirm";
import ManageFootprintModal from "@/components/footprints/FootprintForm.vue";
import ManageCategoryModal from "@/components/footprints/CategoryForm.vue";
import { h } from "vue";
import ButtonsEditDelete from "@/components/btn_edit_delete.vue";

export default {
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
  }),
  components: {
    ButtonsEditDelete,
  },
  data: () => ({
    footprintsCategories: [],
    footprints: [],
    selectedCategory: null,
  }),
  computed: {
    breadcrumb() {
      let footprint = {};
      if (this.selectedCategory) {
        if (this.selectedCategory.description) {
          footprint = {
            label: `${this.selectedCategory.name} (${this.selectedCategory.description})`,
          };
        } else {
          footprint = { label: `${this.selectedCategory.name}` };
        }
      } else {
        footprint = { label: "No category selected" };
      }
      return {
        home: {
          icon: "pi pi-home",
          command: () => {
            this.$router.push({ name: "home" });
          },
        },
        items: [
          {
            label: "Footprints",
            command: () => {
              this.$router.push({ name: "footprints-list" });
            },
          },
          footprint,
        ],
      };
    },
  },
  created() {
    this.fetchFootprintsCategories();
  },
  methods: {
    fetchFootprintsCategories() {
      apiService
        .getFootprintsCategories()
        .then((val) => {
          this.footprintsCategories = val.data;
          this.selectedCategory = val.data && val.data.length > 0 ? val.data[0] : null;
          this.categoryChanged({ value: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Footprints categories",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching footprints categories", err);
        });
    },
    categoryChanged(event) {
      if (!event.value) {
        // unselect event : ignore
        return;
      }

      apiService
        .getFootprintsList({ category_id: this.selectedCategory.id })
        .then((val) => {
          this.footprints = val.data;
          // Also update the store
          this.preloadsStore.setLastUpdate("footprints", new Date("1970/12/12")); // force refresh
          this.preloadsStore.preloadFootprints();
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Footprints",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching footprints", err);
        });
    },
    deleteItem(event, item) {
      this.confirm.require({
        message: `Are you sure you want to delete the footprint '${item.name}' ?`,
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
            .deleteFootprint(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Footprint",
                detail: "Deleted",
                life: 5000,
              });
              this.categoryChanged({ value: true });
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Footprints",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with footprint deletion", err);
              this.categoryChanged({ value: true });
            });
        },
        reject: () => {
          return;
        },
      });
    },
    deleteCategory(event, item) {
      this.confirm.require({
        message: `Are you sure you want to delete the category '${item.name}' ?`,
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
            .deleteFootprintCategory(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Footprint Category",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchFootprintsCategories();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Footprints categories",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with footprint category deletion", err);
              this.fetchFootprintsCategories();
            });
        },
        reject: () => {
          return;
        },
      });
    },
    showAddFootprint() {
      this.$dialog.open(ManageFootprintModal, {
        props: {
          modal: true,
          style: {
            width: "30vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add a footprint")])];
          },
        },
        data: {
          mode: "add",
          category_id: this.selectedCategory.id,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload footprints
            this.categoryChanged({ value: true });
          }
        },
      });
    },
    showEditFootprint(event, item) {
      this.$dialog.open(ManageFootprintModal, {
        props: {
          modal: true,
          style: {
            width: "30vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit footprint")])];
          },
        },
        data: {
          mode: "edit",
          item: item,
          category_id: this.selectedCategory.id,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload footprints
            this.categoryChanged({ value: true });
          }
        },
      });
    },
    showAddCategory() {
      this.$dialog.open(ManageCategoryModal, {
        props: {
          modal: true,
          style: {
            width: "30vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add a category")])];
          },
        },
        data: {
          mode: "add",
          category_id: this.selectedCategory.id,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload footprints
            this.fetchFootprintsCategories();
          }
        },
      });
    },
    showEditCategory(event, item) {
      this.$dialog.open(ManageCategoryModal, {
        props: {
          modal: true,
          style: {
            width: "30vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit category")])];
          },
        },
        data: {
          mode: "edit",
          item: this.selectedCategory,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload footprints
            this.fetchFootprintsCategories({ value: true });
          }
        },
      });
    },
  },
};
</script>
