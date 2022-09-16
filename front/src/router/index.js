import { createRouter, createWebHistory } from "vue-router";
import { useOauthStore } from "@/stores/oauth";

import LoginForm from "@/components/login_form/login_form.vue";
import About from "@/views/About.vue";
import PublicPartsList from "@/views/About.vue";
import UrlHandler from "@/views/About.vue";
import PartsAddFull from "@/views/parts/AddFull.vue";
import PartsAddQuick from "@/views/parts/AddQuick.vue";
import PartsList from "@/views/parts/List.vue";
import PartsDetails from "@/views/parts/View.vue";
import PartsEdit from "@/views/parts/Edit.vue";
import PartUnitsList from "@/views/About.vue";
import ParametersUnitsList from "@/views/About.vue";
import ParametersPresetsList from "@/views/About.vue";
import ParametersPresetsDetails from "@/views/About.vue";
import ParametersPresetsEdit from "@/views/About.vue";
import ParametersPresetsAdd from "@/views/About.vue";
import Distributors from "@/views/About.vue";
import Manufacturers from "@/views/About.vue";
import ViewInfos from "@/views/About.vue";
import ViewStorageTree from "@/views/About.vue";
import OrdersCategoryMatchers from "@/views/About.vue";
import OrdersImporter from "@/views/About.vue";
import OrdersImporterDetails from "@/views/About.vue";
import ProjectsList from "@/views/About.vue";
import ProjectsAdd from "@/views/About.vue";
import ProjectsEdit from "@/views/About.vue";
import ProjectsDetails from "@/views/About.vue";
import StoragesList from "@/views/About.vue";
import LabelTemplatesList from "@/views/About.vue";

const validateAuthenticatedRoute = (to, from, next) => {
  const oauthStore = useOauthStore();
  if (oauthStore.loggedIn) {
    next();
  } else {
    next("/");
  }
};

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Main stuff
    {
      path: "/",
      name: "home",
      redirect: (_to) => {
        const oauthStore = useOauthStore();
        return oauthStore.loggedIn ? "/parts" : "/login";
      },
    },
    // Url Handler
    {
      path: "/urlhandler",
      name: "urlhandler",
      component: UrlHandler,
      beforeEnter: validateAuthenticatedRoute,
    },
    // Parts
    {
      path: "/parts/new",
      name: "parts-new",
      component: PartsAddFull,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/parts/quick-new",
      name: "parts-quick-new",
      component: PartsAddQuick,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/parts/category/:categoryId",
      name: "parts-category-list",
      component: PartsList,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/parts",
      name: "parts-list",
      component: PartsList,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/parts/:partId",
      name: "parts-details",
      component: PartsDetails,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/parts/:partId/edit",
      name: "parts-edit",
      component: PartsEdit,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    // PartUnits
    {
      path: "/part/units",
      name: "part-units-list",
      component: PartUnitsList,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    // Parameters Units
    {
      path: "/part/parameters/units",
      name: "parameters-units-list",
      component: ParametersUnitsList,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    // Parameters Presets
    {
      path: "/part/parameters/presets",
      name: "parameters-presets-list",
      component: ParametersPresetsList,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/part/parameters/presets/:presetId",
      name: "parameters-presets-details",
      component: ParametersPresetsDetails,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/part/parameters/presets/:presetId/edit",
      name: "parameters-presets-edit",
      component: ParametersPresetsEdit,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/part/parameters/presets/new",
      name: "parameters-presets-add",
      component: ParametersPresetsAdd,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    // Distributors
    {
      path: "/distributors",
      name: "distributors-list",
      component: Distributors,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    // Manufacturers
    {
      path: "/manufacturers",
      name: "manufacturers-list",
      component: Manufacturers,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    // Views
    {
      path: "/view/infos",
      name: "view-infos",
      component: ViewInfos,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/views/storage-tree",
      name: "view-storage-tree",
      component: ViewStorageTree,
      beforeEnter: validateAuthenticatedRoute,
    },
    // OrdersImporter
    {
      // this one needs to be before orders-importer-details for props reasons
      path: "/orders/importer/category_matcher",
      name: "orders-importer-category-matcher",
      component: OrdersCategoryMatchers,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/orders/importer",
      name: "orders-importer",
      component: OrdersImporter,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/orders/importer/:id",
      name: "orders-importer-details",
      component: OrdersImporterDetails,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    // Public
    {
      path: "/public/parts",
      name: "public-parts",
      component: PublicPartsList,
      props: true,
    },
    {
      path: "/public/parts/category/:categoryId",
      name: "public-parts-category-list",
      component: PublicPartsList,
      props: true,
    },
    // Projects
    {
      path: "/projects",
      name: "projects-list",
      component: ProjectsList,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/projects/new",
      name: "projects-new",
      component: ProjectsAdd,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/projects/:projectId/edit",
      name: "projects-edit",
      component: ProjectsEdit,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    {
      path: "/projects/:projectId",
      name: "projects-details",
      component: ProjectsDetails,
      props: true,
      beforeEnter: validateAuthenticatedRoute,
    },
    // Storages
    {
      path: "/storages",
      name: "storages-list",
      component: StoragesList,
      beforeEnter: validateAuthenticatedRoute,
    },
    // Label Templates
    {
      path: "/labeltemplates",
      name: "label-templates-list",
      component: LabelTemplatesList,
      beforeEnter: validateAuthenticatedRoute,
    },
    // Other
    {
      path: "/about",
      name: "about",
      component: About,
    },
    // Auth
    { path: "/login", name: "login_form", component: LoginForm },
    { name: "password-reset", path: "/password-reset" },
    // Parts
    { path: "/parts", name: "parts", beforeEnter: validateAuthenticatedRoute },
  ],
});

export default router;
