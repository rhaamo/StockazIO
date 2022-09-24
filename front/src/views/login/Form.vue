<template>
  <div>
    <div class="mt-4 grid align-items-center justify-content-center">
      <div class="surface-card p-4 shadow-2 border-round col-3">
        <div class="text-center mb-5">
          <div class="text-900 text-3xl font-medium mb-3">Welcome Back</div>
        </div>

        <form @submit.prevent="submit(!v$.$invalid)" class="text-center">
          <div>
            <div class="field">
              <label
                for="username"
                :class="{
                  'p-error': v$.user.username.$invalid && submitted,
                  block: true,
                  'font-medium': true,
                }"
                >Username</label
              >
              <InputText
                id="username"
                v-model="user.username"
                :class="{
                  'p-invalid': v$.user.username.$invalid && submitted,
                  'w-7': true,
                }"
              />
              <small
                v-if="
                  (v$.user.username.$invalid && submitted) ||
                  v$.user.username.$pending.$response
                "
                class="p-error"
                ><br />{{ v$.user.username.required.$message }}</small
              >
            </div>

            <div class="field">
              <label
                for="password"
                :class="{
                  'p-error': v$.user.username.$invalid && submitted,
                  block: true,
                  'font-medium': true,
                }"
                >Password</label
              >
              <Password
                id="password"
                type="password"
                v-model="user.password"
                :class="{
                  'p-invalid': v$.user.password.$invalid && submitted,
                  'w-7': true,
                }"
                toggleMask
                :feedback="false"
              />
              <small
                v-if="
                  (v$.user.password.$invalid && submitted) ||
                  v$.user.password.$pending.$response
                "
                class="p-error"
                ><br />{{ v$.user.password.required.$message }}</small
              >
            </div>

            <div class="mb-5 mt-5">
              <router-link
                class="font-medium no-underline text-blue-500 text-center cursor-pointer"
                :to="{ name: 'password-reset-request' }"
                >Forgot password ?</router-link
              >
            </div>

            <Button
              label="Login"
              icon="pi pi-user"
              class="w-4"
              type="submit"
            ></Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";
import { useOauthStore } from "@/stores/oauth";
import { useUserStore } from "@/stores/user";
import logger from "@/logging";
import { usePreloadsStore } from "@/stores/preloads";
import { useToast } from "primevue/usetoast";

export default {
  data: () => ({
    user: {
      username: "",
      password: "",
    },
    submitted: false,
  }),
  setup: () => ({
    v$: useVuelidate(),
    oauthStore: useOauthStore(),
    userStore: useUserStore(),
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
  }),
  validations: {
    user: {
      username: { required, maxLength: maxLength(250) },
      password: { required, maxLength: maxLength(250) },
    },
  },
  mounted() {
    if (this.oauthStore.loggedIn) {
      logger.default.info("already logged in, redirecting...");
      this.$router.push({ name: "home" });
    }
  },
  methods: {
    submit(isFormValid) {
      this.submitted = true;

      if (!isFormValid) {
        return;
      }

      this.oauthStore.getOrCreateApp().then((app) => {
        this.oauthStore
          .getTokenWithCredentials(
            app.clientId,
            app.clientSecret,
            this.user.username,
            this.user.password
          )
          .then((result) => {
            if (result.data.error) {
              logger.default.error(
                "Error getting token with creds:",
                result.data.error
              );
              return;
            }
            this.userStore.login(result.data).then(() => {
              Promise.allSettled([
                this.preloadsStore.preloadSidebar(),
                this.preloadsStore.preloadFootprints(),
                this.preloadsStore.preloadStorages(),
                this.preloadsStore.preloadParametersUnits(),
                this.preloadsStore.preloadPartUnits(),
                this.preloadsStore.preloadManufacturers(),
                this.preloadsStore.preloadDistributors(),
                this.preloadsStore.preloadLabelTemplates(),
                this.preloadsStore.preloadPartParametersPresets(),
              ]).then(() => {
                logger.default.info("post-login preloading finished");
                this.$router.push({ name: "home" });
              });
            });
          })
          .catch((error) => {
            logger.default.error("Login error:", error);
            this.toast.add({
              severity: "error",
              summary: "Login",
              detail: "An error occured, please try again later",
              life: 5000,
            });
          });
      });
    },
  },
};
</script>
