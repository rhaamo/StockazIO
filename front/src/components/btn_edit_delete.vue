<template>
  <span class="p-buttonset">
    <PvButton severity="success" @click.prevent="btnEdit" icon="pi pi-pen-to-square" />
    <PvButton severity="danger" @click.prevent="btnDelete" icon="pi pi-trash" class="ml-1" />
  </span>
</template>

<script>
export default {
  props: {},
  data: () => {
    return {};
  },
  computed: {},
  methods: {
    btnEdit() {
      this.$nextTick(() => {
        this.$emit("edit");
      });
    },
    btnDelete() {
      this.$nextTick(() => {
        this.$emit("delete");
      });
    },
  },
};
</script>

<style lang="scss" scoped></style>
