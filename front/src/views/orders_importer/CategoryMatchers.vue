<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <div class="grid" v-if="matchers.length">
        <div class="col-5">Regexp</div>
        <div class="col-3">Category</div>
      </div>

      <div v-for="(_, i) in matchers" :key="i">
        <CategoryMatcherEntry
          v-model:item="matchers[i]"
          v-model:categories="choicesCategory"
          :submitted="submitted"
          @deleteItem="deleteCategoryMatcher($event, i)"
        />
      </div>

      <Divider />

      <PvButton
        label="add matcher"
        @click.prevent="addCategoryMatcher"
      ></PvButton>
      <PvButton
        label="save matchers"
        class="p-button-success ml-2"
        @click.prevent="submit(!v$.$invalid)"
      ></PvButton>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { useConfirm } from "primevue/useconfirm";
import CategoryMatcherEntry from "@/components/category_matchers/Entry.vue";
import { mapState } from "pinia";
import { useVuelidate } from "@vuelidate/core";

export default {
  components: {
    CategoryMatcherEntry,
  },
  data: () => ({
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [
        { label: "Orders importer", to: { name: "orders-importer" } },
        {
          label: "Category Matchers",
          to: { name: "orders-importer-category-matcher" },
        },
      ],
    },
    matchers: [],
    deleted: [],
    submitted: false,
  }),
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
    v$: useVuelidate(),
  }),
  computed: {
    ...mapState(usePreloadsStore, {
      choicesCategory: (store) => {
        const cb = (e) => {
          // base object
          let obj = {
            key: e.id,
            label: e.name,
            icon: `fa fa-folder-o`,
          };
          obj["selectable"] = true;
          obj["children"] = e.children.map(cb);
          return obj;
        };
        return [store.categories].map(cb);
      },
    }),
  },
  validations: {
    matchers: {},
  },
  mounted() {
    this.$nextTick(() => {
      this.loadLazyData();
    });
  },
  methods: {
    loadLazyData() {
      this.loading = true;

      apiService
        .getCategoryMatchers()
        .then((res) => {
          this.matchers = res.data.map((x) => {
            return {
              id: x.id,
              regexp: x.regexp,
              category: { [x.category.id]: true },
            };
          });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Category Matchers",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching category matchers", err);
        });
    },
    addCategoryMatcher() {
      this.matchers.push({
        regexp: "",
        category: null,
      });
    },
    deleteCategoryMatcher(event, index) {
      if (this.matchers[index].id) {
        // mark it as deletion
        this.deleted.push(this.matchers[index].id);
      }
      this.matchers.splice(index, 1);
    },
    submit(isFormValid) {
      this.submitted = true;

      if (!isFormValid) {
        return;
      }

      let cmToUpdate = this.matchers.map((x) => {
        return {
          id: x.id,
          regexp: x.regexp,
          category: Object.keys(x.category)[0],
        };
      });

      apiService
        .updateCategoryMatchers({ update: cmToUpdate, delete: this.deleted })
        .then((resp) => {
          this.toast.add({
            severity: "success",
            summary: "Updating category matchers",
            detail: "Success",
            life: 5000,
          });
          this.loadLazyData();
          this.deleted = [];
        })
        .catch((error) => {
          this.toast.add({
            severity: "error",
            summary: "Updating category matchers",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error(
            "Cannot update category matchers",
            error.message
          );
          this.loadLazyData();
          this.deleted = [];
        });
    },
  },
};
</script>
