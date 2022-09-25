<template>
  <div>
    <div class="grid">
      <div class="col-4">
        <div>
          <template v-if="items && items.length === 1">
            <template v-if="kind === 'storage'"
              >Storage location infos:<br
            /></template>
            <template v-else>Item infos:<br /></template>
            <ul>
              <li>Name: {{ items[0].name }}</li>
              <li>Description: {{ items[0].description || "none" }}</li>
              <li>UUID: {{ items[0].uuid }}</li>
              <li>qrCode content: {{ qrCodeUri(items[0]) }}</li>
            </ul>
          </template>
          <template v-else>
            Multiple items choosen for label generation.
            <ul>
              <li v-for="item in items" :key="item.id">
                {{ item.name }}
              </li>
            </ul>
          </template>
        </div>

        <div class="mt-5">
          Template:<br />
          <Dropdown
            v-model="template"
            class="p-column-filter mt-1"
            placeholder="Please select a template"
            :options="choicesTemplates"
            optionLabel="name"
            optionValue="tpl"
            :filter="true"
          />
        </div>

        <div class="mt-5 text-sm">
          <p>You can use the PDF on the right to print corresponding labels.</p>
          <p>
            Do not hesitate to download the PDF and open it natively if the
            print preview is showing a bad layout.
          </p>
          <p>
            When printing, make sure to select the right template for the used
            label paper.
          </p>
        </div>
      </div>

      <div class="col-8">
        <div v-if="template && pdf">
          <Button @click.prevent="printPdf" label="Print Labels PDF"></Button
          ><br />
          <VuePdfEmbed ref="pdfViewer" :source="pdf" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { mapState } from "pinia";
import { generate } from "@pdfme/generator";

export default {
  inject: ["dialogRef"],
  data: () => ({
    items: [],
    template: null,
    pdf: null,
    kind: "part",
  }),
  setup: () => ({
    preloadsStore: usePreloadsStore(),
  }),
  created() {
    this.kind = this.dialogRef.data.kind || "part";
    this.items = this.dialogRef.data.items;
    if (this.choicesTemplates && this.choicesTemplates.length) {
      this.template = this.choicesTemplates[0].tpl;
    }
  },
  watch: {
    template: function () {
      this.pdf = null;
      this.generatePdf();
    },
  },
  computed: {
    ...mapState(usePreloadsStore, {
      choicesTemplates: (store) => {
        return store.label_templates.map((x) => {
          return { name: x.name, tpl: x };
        });
      },
    }),
  },
  methods: {
    doSubstitutions(item) {
      let text = this.template.text_template;
      text = item && item.name ? text.replace("{name}", item.name) : text;
      text =
        item && item.description
          ? text.replace("{description}", item.description)
          : text.replace("{description}", ""); // description is optional
      text =
        item && item.uuid
          ? text.replace("{qrcode}", this.qrCodeUri(item))
          : text;
      text =
        item && item.category_name
          ? text.replace("{category_name}", item.category_name)
          : text.replace("{category_name}", ""); // category_name is optional
      return text;
    },
    qrCodeUri(item) {
      if (this.kind === "storage") {
        // location
        return `web+stockazio:storageLocation,${item.uuid}`;
      } else {
        // part
        return `web+stockazio:part,${item.uuid}`;
      }
    },
    generatePdf() {
      const template = {
        basePdf: this.template.base_pdf,
        schemas: Array(this.items.length).fill(
          JSON.parse(this.template.template)
        ),
      };
      let inputs = [];
      this.items.forEach((cb) => {
        inputs.push({
          qrcode: this.qrCodeUri(cb),
          text: this.doSubstitutions(cb),
        });
      });
      generate({ template, inputs }).then((pdf) => {
        let blob = new Blob([pdf.buffer], { type: "application/pdf" });
        this.pdf = URL.createObjectURL(blob);
      });
    },
    printPdf() {
      this.$refs.pdfViewer.print();
    },
  },
};
</script>
