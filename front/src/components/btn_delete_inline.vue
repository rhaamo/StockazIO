<template>
  <div>
    <span class="p-buttonset">
      <Button
        :class="(clicked ? 'p-button-secondary' : btnVariantMain) + ' ' + size"
        :disabled="clicked"
        @click.prevent="btnClicked"
        :label="clicked ? btnMainTextDisabled : btnMainText"
      >
      </Button>
      <template v-if="clicked">
        <Button
          :class="btnVariantOk + ' ' + size"
          @click.prevent="actionConfirmed"
          :label="btnOkText"
        >
        </Button>
        <Button
          :class="btnVariantCancel + ' ' + size"
          @click.prevent="actionCancelled"
          :label="btnCancelText"
        >
        </Button>
      </template>
    </span>
  </div>
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
