import { createRouter, createWebHistory } from "vue-router";
import { useOauthStore } from "@/stores/oauth";

import LoginForm from "@/components/login_form/login_form.vue";

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
    // Auth
    { path: "/login", name: "login_form", component: LoginForm },
  ],
});

export default router;
