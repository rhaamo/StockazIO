<template>
  <div>
    <ul class="list-none mt-1">
      <li class="mt-1 list-none">
        <i class="fa fa-home" aria-hidden="true" /> {{ item.name }}

        <template v-if="!readonly">
          &nbsp;&nbsp;

          <router-link
            to="#"
            v-tooltip="`Edit Category`"
            @click.prevent="editCategoryModal(item)"
            class="no-underline"
          >
            <i class="fa fa-pencil-square-o" aria-hidden="true" />
          </router-link>
          &nbsp;
          <router-link
            to="#"
            v-tooltip="`Delete Category`"
            @click.prevent="deleteCategoryModal(item)"
            class="no-underline"
          >
            <i class="fa fa-trash-o" aria-hidden="true" />
          </router-link>

          &nbsp;&nbsp;

          <router-link
            to="#"
            v-tooltip="`${addCategoryTitle(item.name)}`"
            @click.prevent="addCategoryModal(item.id)"
            class="no-underline"
          >
            [add category]
          </router-link>

          &nbsp;&nbsp;
          <router-link
            to="#"
            v-tooltip="`${addLocationTitle(item.name)}`"
            @click.prevent="addLocationModal(item.id)"
            class="no-underline"
          >
            [add location/box]
          </router-link>
        </template>
      </li>
      <ListCategory
        v-for="category in item.children"
        :key="category.id"
        :item="category"
        :level="level + 1"
        :readonly="readonly"
      />
      <ul class="mt-1">
        <ListLocation
          v-for="storage in item.storage_locations"
          :key="storage.uuid"
          :item="storage"
          :level="level + 1"
          :readonly="readonly"
        />
      </ul>
    </ul>
  </div>
</template>

<script>
import ListLocation from "@/components/storages/ListLocation.vue";

export default {
  components: {
    ListLocation,
  },
  props: {
    item: Object,
    level: Number,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    addCategoryTitle(name) {
      return `Add category under '${name}'`;
    },
    addLocationTitle(name) {
      return `Add location/box under '${name}'`;
    },
    editCategoryModal(item) {
      console.log("editCategoryModal", item);
    },
    deleteCategoryModal(item) {
      console.log("deleteCategoryModal", item);
    },
    addCategoryModal(id) {
      console.log("addCategoryModal", id);
    },
    addLocationModal(id) {
      console.log("addLocationModal", id);
    },
  },
};
</script>
