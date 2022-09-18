<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />

    <div class="mt-4 ml-4">
      <div class="grid">
        <div class="col-1">Parts<Divider /></div>
        <div class="col-1">{{ parts_count }}<Divider /></div>
      </div>

      <div class="grid">
        <div class="col-1">Categories<Divider /></div>
        <div class="col-1">{{ categories_count }}<Divider /></div>
      </div>

      <div class="grid">
        <div class="col-1">App Version<Divider /></div>
        <div class="col-1">{{ version }}<Divider /></div>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from "@/services/api/api.service";

export default {
  data: () => ({
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [{ label: "Informations" }],
    },
    parts_count: 0,
    categories_count: 0,
    version: "0.0",
  }),
  created() {
    apiService.getInformations().then((data) => {
      this.parts_count = data.data.parts_count;
      this.categories_count = data.data.categories_count;
      this.version = data.data.version;
    });
  },
};
</script>
