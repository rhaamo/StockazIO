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
        :globalFilterFields="['name']"
        v-model:filters="filters"
      >
        <template #header>
          <div class="grid">
            <div class="col-2">
              <Button
                label="Add a manufacturer"
                @click.prevent="showAddManufacturerModal"
              />
            </div>

            <div class="col-2 col-offset-7">
              <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText
                  v-model="filters['global'].value"
                  placeholder="Keyword Search"
                />
              </span>
            </div>
          </div>
        </template>

        <Column field="name" header="Name" :sortable="true"></Column>
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
      global: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
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
  methods: {
    showAddManufacturerModal() {},
  },
};
</script>
