<template>
  <div class="inline">
    <PvButton
      v-if="part.stock_qty >= part.stock_qty_min || kind !== 'qty'"
      @click.prevent="showPartQtyEditorModal($event)"
      variant="text"
      severity="secondary"
      :size="size"
      >{{ kind === "qty" ? part.stock_qty : part.stock_qty_min }}</PvButton
    >
    <PvButton
      v-else
      severity="warn"
      variant="text"
      :size="size"
      @click.prevent="showPartQtyEditorModal($event)"
      v-tooltip.top="`Current stock is below minimum ${part.stock_qty_min} stock quantity or exhausted`"
      >{{ kind === "qty" ? part.stock_qty : part.stock_qty_min }} <i class="fa fa-circle"></i
    ></PvButton>

    <Popover ref="poQty">
      <label
        for="qty"
        :class="{
          'pb-3': true,
          block: true,
        }"
        >Change quantity from {{ kind === "qty" ? part.oldQty : part.oldQtyMin }} to:</label
      >
      <div class="flex gap-2" v-if="kind === 'qty'">
        <InputNumber
          v-model="part.stock_qty"
          inputId="qty"
          mode="decimal"
          showButtons
          buttonLayout="horizontal"
          :min="0"
          @keyup.enter.prevent="updateInplaceBothQty($event)"
        />
        <PvButton label="save" severity="success" @click.prevent="updateInplaceBothQty($event)" />
      </div>
      <div class="flex gap-2" v-else>
        <InputNumber
          v-model="part.stock_qty_min"
          inputId="qty"
          mode="decimal"
          showButtons
          buttonLayout="horizontal"
          :min="0"
          @keyup.enter.prevent="updateInplaceBothQty($event)"
        />
        <PvButton label="save" severity="success" @click.prevent="updateInplaceBothQty($event)" />
      </div>

      <InputGroup class="mt-3">
        <PvButton label="-10" severity="success" size="small" @click.prevent="updateSelectedPartQty(-10)" />
        <PvButton label="-50" severity="info" size="small" @click.prevent="updateSelectedPartQty(-50)" />
        <PvButton label="-100" severity="help" size="small" @click.prevent="updateSelectedPartQty(-100)" />
        <PvButton disabled severity="secondary" size="small" />
        <PvButton label="+100" severity="help" size="small" @click.prevent="updateSelectedPartQty(+100)" />
        <PvButton label="+50" severity="info" size="small" @click.prevent="updateSelectedPartQty(+50)" />
        <PvButton label="+10" severity="success" size="small" @click.prevent="updateSelectedPartQty(+10)" />
      </InputGroup>
    </Popover>
  </div>
</template>

<script>
import logger from "@/logging";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";

export default {
  components: {},
  props: {
    part: Object,
    kind: {
      type: [String, null],
      default: null,
    },
    size: String,
  },
  setup: () => ({
    toast: useToast(),
  }),
  mounted() {
    console.log("Instancing QtyPopoverEditor for", this.kind);
  },
  methods: {
    showPartQtyEditorModal(event) {
      this.$refs.poQty.hide();

      this.part.oldQty = this.part.stock_qty;
      this.part.oldQtyMin = this.part.stock_qty_min;

      this.$nextTick(() => {
        this.$refs.poQty.show(event);
      });
    },
    updateSelectedPartQty(quantity) {
      if (this.kind === "qty") {
        if (this.part.stock_qty + quantity < 0) {
          this.part.stock_qty = 0;
          return;
        }
        this.part.stock_qty += quantity;
      } else {
        if (this.part.stock_qty_min + quantity < 0) {
          this.part.stock_qty_min = 0;
          return;
        }
        this.part.stock_qty_min += quantity;
      }
    },
    updateInplaceBothQty(event) {
      logger.default.info("update inplace qtys", this.part.id, this.part.stock_qty, this.part.stock_qty_min);
      apiService
        .updatePartialPart(this.part.id, { stock_qty: this.part.stock_qty, stock_qty_min: this.part.stock_qty_min })
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: `Updating part quantities`,
            detail: "Success",
            life: 5000,
          });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: `Updating part quantities`,
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with quantity part update", err);
        });
      // hide popover and reset the selected part
      this.$refs.poQty.hide();
    },
  },
};
</script>
