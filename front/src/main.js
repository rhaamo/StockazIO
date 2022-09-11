import { createApp } from "vue";
import { createPinia } from "pinia";
import { createPersistedState } from "pinia-plugin-persistedstate";
import axios from "axios";
import { useOauthStore } from "@/stores/oauth";
import PrimeVue from "primevue/config";
import ProgressSpinner from "primevue/progressspinner";
import Menubar from "primevue/menubar";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Password from "primevue/password";
import ToastService from "primevue/toastservice";
import ConfirmationService from "primevue/confirmationservice";
import ConfirmDialog from "primevue/confirmdialog";
import Tree from "primevue/tree";
import Breadcrumb from "primevue/breadcrumb";
import InputNumber from "primevue/inputnumber";
import Checkbox from "primevue/checkbox";
import MultiSelect from "primevue/multiselect";
import TreeSelect from "primevue/treeselect";
import Toast from "primevue/toast";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import TabView from "primevue/tabview";
import TabPanel from "primevue/tabpanel";
import VueQrcode from "@chenfengyuan/vue-qrcode";
import OverlayPanel from "primevue/overlaypanel";
import Image from "primevue/image";
import Tooltip from "primevue/tooltip";
import Inplace from "primevue/inplace";
import Card from "primevue/card";
import DialogService from "primevue/dialogservice";
import DynamicDialog from "primevue/dynamicdialog";
import Galleria from "primevue/galleria";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

const pinia = createPinia();
pinia.use(
  createPersistedState({
    storage: localStorage,
  })
);

app.use(pinia);
app.use(router);
app.use(PrimeVue);
app.use(ToastService);
app.use(ConfirmationService);
app.use(DialogService);

const oauthStore = useOauthStore();

axios.interceptors.request.use(
  function (config) {
    if (oauthStore.userToken.access_token) {
      console.log("Axios interceptor set");
      config.headers[
        "Authorization"
      ] = `Bearer ${oauthStore.userToken.access_token}`;
    } else {
      console.log("No Axios interceptor to set");
    }
    return config;
  },
  function (error) {
    console.log("Cannot set Axios Interceptor for Auth token");
    return Promise.reject(error);
  }
);

app.component(VueQrcode.name, VueQrcode);
app.component("ProgressSpinner", ProgressSpinner);
app.component("Menubar", Menubar);
app.component("InputText", InputText);
app.component("InputNumber", InputNumber);
app.component("Button", Button);
app.component("Password", Password);
app.component("ConfirmDialog", ConfirmDialog);
app.component("Tree", Tree);
app.component("Breadcrumb", Breadcrumb);
app.component("Checkbox", Checkbox);
app.component("MultiSelect", MultiSelect);
app.component("TreeSelect", TreeSelect);
app.component("Toast", Toast);
app.component("DataTable", DataTable);
app.component("Column", Column);
app.component("TabView", TabView);
app.component("TabPanel", TabPanel);
app.component("OverlayPanel", OverlayPanel);
app.component("Image", Image);
app.component("Inplace", Inplace);
app.component("Card", Card);
app.component("DynamicDialog", DynamicDialog);
app.component("Galleria", Galleria);

app.directive("tooltip", Tooltip);

// Register a global custom directive called `v-focus`
app.directive("focus", {
  // When the bound element is mounted into the DOM...
  mounted(el) {
    // Focus the element
    el.focus();
  },
});

app.mount("#app");
