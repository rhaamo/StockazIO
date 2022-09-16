<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        :value="manufacturers"
        class="p-datatable-sm"
        stripedRows
        responsiveLayout="scroll"
        :paginator="true"
        :rows="perPage"
        removableSort
        filterDisplay="row"
        :globalFilterFields="['name']"
        v-model:filters="filters"
      >
        <Column field="name" header="Name" :sortable="true">
          <template #filter="{ filterModel, filterCallback }">
            <InputText
              type="text"
              v-model="filterModel.value"
              @keydown.enter="filterCallback()"
              class="p-column-filter"
              :placeholder="`Search by name - `"
              v-tooltip.top.focus="'Hit enter key to filter'"
            />
          </template>
        </Column>
        <Column field="logo" header="Logo">
          <template #body="slotProps">
            <img
              :src="slotProps.data.logo_mini"
              style="max-width: 100px"
              :alt="slotProps.data.name"
              lazy
              v-if="slotProps.data.logo"
            />
          </template>
        </Column>
        <Column field="address" header="Address"></Column>
        <Column field="url" header="URL">
          <template #body="slotProps">
            <template v-if="slotProps.data.url">
              <a :href="slotProps.data.url" target="_blank">{{
                slotProps.data.url
              }}</a>
            </template>
            <template v-if="slotProps.data.url && slotProps.data.email"
              ><br
            /></template>
            <template v-if="slotProps.data.email">
              {{ slotProps.data.email }}
            </template>
          </template>
        </Column>
        <Column field="comment" header="Comment"></Column>
        <Column field="phones" header="Phones">
          <template #body="slotProps">
            <template v-if="slotProps.data.phone">
              Tel: {{ slotProps.data.phone }}
            </template>
            <template v-if="slotProps.data.phone && slotProps.data.fax">
              <br />
            </template>
            <template v-if="slotProps.data.fax">
              Fax: {{ slotProps.data.fax }}
            </template>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { useServerStore } from "@/stores/server";
import { mapState } from "pinia";
import { FilterMatchMode } from "primevue/api";

export default {
  data: () => ({
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [{ label: "Manufacturers" }],
    },
    filters: {
      name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    },
  }),
  computed: {
    ...mapState(usePreloadsStore, {
      manufacturers: (store) => {
        return store.manufacturers;
      },
    }),
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.MANUFACTURERS || 10,
    }),
  },
};
</script>
