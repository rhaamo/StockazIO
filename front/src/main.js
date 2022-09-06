import { createApp } from "vue";
import { createPinia } from "pinia";
import { createPersistedState } from "pinia-plugin-persistedstate";
import axios from "axios";
import { useOauthStore } from "@/stores/oauth";

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

const oauthStore = useOauthStore();

axios.interceptors.request.use(
  function (config) {
    if (oauthStore.userToken) {
      console.log("Axios interceptor set");
      config.headers["Authorization"] = `Bearer ${oauthStore.userToken}`;
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

app.mount("#app");
