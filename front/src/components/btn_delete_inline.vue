<template>
  <span class="p-buttonset">
    <PvButton
      :class="(clicked ? 'p-button-secondary' : btnVariantMain) + ' ' + size"
      :disabled="clicked"
      :label="clicked ? btnMainTextDisabled : btnMainText"
      @click.prevent="btnClicked">
    </PvButton>
    <template v-if="clicked">
      <PvButton :class="'ml-1 ' + btnVariantOk + ' ' + size" :label="btnOkText" @click.prevent="actionConfirmed"> </PvButton>
      <PvButton :class="'ml-1 ' + btnVariantCancel + ' ' + size" :label="btnCancelText" @click.prevent="actionCancelled"> </PvButton>
    </template>
  </span>
</template>

<script>
export default {
  props: {
    size: {
      type: String,
      default: "p-button-sm",
    },
    btnVariantMain: {
      type: String,
      default: "p-button-danger",
    },
    btnVariantOk: {
      type: String,
      default: "p-button-success",
    },
    btnVariantCancel: {
      type: String,
      default: "p-button-danger",
    },
    btnMainText: {
      type: String,
      default: "remove item",
    },
    btnMainTextDisabled: {
      type: String,
      default: "Confirm ?",
    },
    btnOkText: {
      type: String,
      default: "Yes",
    },
    btnCancelText: {
      type: String,
      default: "No",
    },
  },
  data: () => {
    return {
      clicked: false,
    };
  },
  computed: {},
  methods: {
    btnClicked() {
      this.clicked = true;
    },
    actionConfirmed() {
      this.clicked = false;
      this.$nextTick(() => {
        this.$emit("action-confirmed");
      });
    },
    actionCancelled() {
      this.clicked = false;
      this.$emit("action-cancelled");
    },
  },
};
</script>

<style lang="scss" scoped>
.p-button {
  margin-right: 0.5rem;
}

.p-buttonset {
  .p-button {
    margin-right: 0;
  }
}

.sizes {
  .button {
    margin-bottom: 0.5rem;
    display: block;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

@media screen and (max-width: 640px) {
  .p-button {
    margin-bottom: 0.5rem;

    &:not(.p-button-icon-only) {
      display: flex;
      width: 100%;
    }
  }

  .p-buttonset {
    .p-button {
      margin-bottom: 0;
    }
  }
}
</style>
