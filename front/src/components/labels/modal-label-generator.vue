<template>
  <b-modal
    id="modalLabelGenerator" ref="modalLabelGenerator"
    size="xl" hide-footer
    @show="modalLabelGeneratorShow"
    @cancel="modalLabelGeneratorClose"
    @close="modalLabelGeneratorClose" @hidden="modalLabelGeneratorClose"
  >
    <template #modal-header="{ close }">
      <h5 id="modalPartTitle">
        QrCode Label Generator
      </h5>
      <button
        type="button" class="close" data-dismiss="modal"
        aria-label="Close" @click="close()"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </template>

    <div class="container">
      <div class="row">
        <div class="col-md-5 mx-auto">
          <template v-if="item">
            <template v-if="item.category">
              Storage location infos:<br>
              <ul>
                <li>Name: {{ item.name }}</li>
                <li>Description: {{ item.description }}</li>
                <li>UUID: {{ item.uuid }}</li>
              </ul>
            </template>
            <template v-else>
              Part infos:<br>
              <ul>
                <li>Name: {{ item.name }}</li>
                <li>Description: {{ item.description }}</li>
                <li>UUID: {{ item.uuid }}</li>
              </ul>
            </template>
          </template>
        </div>
        <div class="col-md-7 mx-auto">
          <vue-pdf-app
            v-if="pdf" :pdf="pdf" :config="pdfJsConfig"
            style="min-height: 30em;"
          />
        </div>
      </div>
    </div>
  </b-modal>
</template>

<script>
import { generate } from '@pdfme/generator'
import VuePdfApp from 'vue-pdf-app'
import 'vue-pdf-app/dist/icons/main.css'

export default {
  components: {
    VuePdfApp
  },
  props: {
    item: {
      type: Object
    }
  },
  data: () => ({
    templates: '{ "field1": { "type": "qrcode", "position": { "x": 1, "y": 1 }, "width": 36, "height": 36 }, "field2": { "type": "text", "position": { "x": 39.39, "y": 1 }, "width": 44.61, "height": 34, "alignment": "left", "fontSize": 12 } }',
    basePdf: 'data:application/pdf;base64,JVBERi0xLjMKMyAwIG9iago8PC9UeXBlIC9QYWdlCi9QYXJlbnQgMSAwIFIKL1Jlc291cmNlcyAyIDAgUgovQ29udGVudHMgNCAwIFI+PgplbmRvYmoKNCAwIG9iago8PC9GaWx0ZXIgL0ZsYXRlRGVjb2RlIC9MZW5ndGggMTk+PgpzdHJlYW0KeJwzUvDiMtAzNVco5wIAC/wCEgplbmRzdHJlYW0KZW5kb2JqCjEgMCBvYmoKPDwvVHlwZSAvUGFnZXMKL0tpZHMgWzMgMCBSIF0KL0NvdW50IDEKL01lZGlhQm94IFswIDAgMjU1LjEyIDEwNy43Ml0KPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1Byb2NTZXQgWy9QREYgL1RleHQgL0ltYWdlQiAvSW1hZ2VDIC9JbWFnZUldCi9Gb250IDw8Cj4+Ci9YT2JqZWN0IDw8Cj4+Cj4+CmVuZG9iago1IDAgb2JqCjw8Ci9Qcm9kdWNlciAoUHlGUERGIDEuNy4yIGh0dHA6Ly9weWZwZGYuZ29vZ2xlY29kZS5jb20vKQovQ3JlYXRpb25EYXRlIChEOjIwMjIwMjEzMTUyNzUzKQo+PgplbmRvYmoKNiAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMSAwIFIKL09wZW5BY3Rpb24gWzMgMCBSIC9GaXRIIG51bGxdCi9QYWdlTGF5b3V0IC9PbmVDb2x1bW4KPj4KZW5kb2JqCnhyZWYKMCA3CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDE3NSAwMDAwMCBuIAowMDAwMDAwMjYyIDAwMDAwIG4gCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA4NyAwMDAwMCBuIAowMDAwMDAwMzU2IDAwMDAwIG4gCjAwMDAwMDA0NjUgMDAwMDAgbiAKdHJhaWxlcgo8PAovU2l6ZSA3Ci9Sb290IDYgMCBSCi9JbmZvIDUgMCBSCj4+CnN0YXJ0eHJlZgo1NjgKJSVFT0YK',
    pdf: null,
    pdfJsConfig: {
      sidebar: false,
      secondaryToolbar: {
        secondaryPresentationMode: true,
        secondaryOpenFile: true,
        secondaryPrint: true,
        secondaryDownload: true,
        secondaryViewBookmark: true,
        firstPage: true,
        lastPage: true,
        pageRotateCw: true,
        pageRotateCcw: true,
        cursorSelectTool: true,
        cursorHandTool: true,
        scrollVertical: true,
        scrollHorizontal: true,
        scrollWrapped: true,
        spreadNone: false,
        spreadOdd: false,
        spreadEven: false,
        documentProperties: false
      },
      toolbar: {
        toolbarViewerLeft: {
          findbar: false,
          previous: true,
          next: true,
          pageNumber: true
        },
        toolbarViewerRight: {
          presentationMode: false,
          openFile: false,
          print: true,
          download: true,
          viewBookmark: false
        },
        toolbarViewerMiddle: {
          zoomOut: true,
          zoomIn: true,
          scaleSelectContainer: true
        }
      },
      errorWrapper: true
    }
  }),
  computed: {
  },
  methods: {
    modalLabelGeneratorShow () {
      const template = {
        basePdf: this.basePdf,
        schemas: [
          // JSON.parse(this.templates)
          {
            'qrcode': {
              'type': 'qrcode',
              'position': {
                'x': 1,
                'y': 1
              },
              'width': 36,
              'height': 36
            },
            'text': {
              'type': 'text',
              'position': {
                'x': 39.39,
                'y': 1
              },
              'width': 44.61,
              'height': 34,
              'alignment': 'left',
              'fontSize': 12,
              'characterSpacing': 0,
              'lineHeight': 1
            }
          }
        ]
      }
      let inputs = [{
        'qrcode': 'uwu',
        'text': 'owo'
      }]
      console.log(template)
      generate({ template, inputs })
        .then((pdf) => {
          let blob = new Blob([pdf.buffer], { type: 'application/pdf' })
          this.pdf = URL.createObjectURL(blob)
          console.log(this.pdf)
        })
    },
    modalLabelGeneratorClose () {
    }
  }
}
</script>

<style>
</style>
