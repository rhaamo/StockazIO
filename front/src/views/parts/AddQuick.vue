<template>
  <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
  <div class="card ml-5">
    <h2>Basic parts informations</h2>
    <div class="formgrid grid">
      <div class="field col-12 md:col-6">
        <label for="Name" class="block">Name*</label>
        <InputText type="text" placeholder="PIC42ACHU" class="w-10" />
      </div>
      <div class="field col-12 md:col-6">
        <label for="part_unit" class="block">Part unit</label>
        <MultiSelect placeholder="Centimeters ? Pieces ?" class="w-7" />
      </div>

      <div class="field col-12 md:col-6">
        <label for="Name" class="block">Description</label>
        <InputText type="text" placeholder="A cute little mcu" class="w-10" />
      </div>
      <div class="field col-12 md:col-6">
        <label for="part_unit" class="block">Category</label>
        <TreeSelect placeholder="Film resistors ? MCUs ?" class="w-7" />
      </div>

      <div class="field col-12 md:col-6">
        <label for="Name" class="block">Comment</label>
        <InputText
          type="text"
          placeholder="Any comment about this part ?"
          class="w-10"
        />
      </div>
      <div class="field col-12 md:col-6">
        <label for="part_unit" class="block">Storage Location</label>
        <TreeSelect
          placeholder="A box under the bench or some drawer ?"
          class="w-7"
        />
      </div>

      <div class="field col-12 md:col-3">
        <label for="Name" class="block">Stock Qty*</label>
        <InputNumber
          inputId="minmax-buttons"
          mode="decimal"
          showButtons
          :min="0"
          class="w-8"
        />
      </div>
      <div class="field col-12 md:col-3">
        <label for="Name" class="block">Stock Qty Min*</label>
        <InputNumber
          inputId="minmax-buttons"
          mode="decimal"
          showButtons
          :min="0"
          class="w-8"
        />
      </div>

      <div class="field col-12 md:col-6">
        <label for="part_unit" class="block">Footprint</label>
        <MultiSelect placeholder="PDIP, BGA, SOIC, who knows" class="w-7" />
      </div>

      <div class="field col-12 md:col-6">
        <label for="Name" class="block">Sheet status</label>
        <InputText type="text" class="w-10" />
      </div>

      <div class="field col-12 md:col-6">
        <!-- save and save add another-->
        <Button label="Save and view" class="p-button-primary" />
        <Button label="Save and add another" class="ml-2 p-button-secondary" />
      </div>

      <div class="field col-12 md:col-12">
        <label for="Name" class="block">Part Condition</label>
        <InputText
          type="text"
          placeholder="Condition of the part"
          class="w-5"
        />
      </div>

      <div class="field col-12 md:col-12">
        <label for="Name" class="block">Production Remarks</label>
        <InputText type="text" class="w-5" />
      </div>

      <div class="field col-12 md:col-12">
        <label for="Name" class="block">Internal Part Number</label>
        <InputText type="text" class="w-5" />
      </div>

      <div class="field-checkbox col-12 md:col-2">
        <Checkbox inputId="binary" :binary="true" />
        <label for="Name">This sheet needs review</label>
      </div>
      <div class="field-checkbox col-12 md:col-2">
        <Checkbox inputId="binary" :binary="true" />
        <label for="Name">That part can be sold</label>
      </div>
      <div class="field-checkbox col-12 md:col-2">
        <Checkbox inputId="binary" :binary="true" />
        <label for="Name">That part is private</label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [{ label: "Quick add new part" }],
    },
  }),
};
</script>
