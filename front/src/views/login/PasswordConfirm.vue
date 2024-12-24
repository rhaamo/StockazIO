<template>
  <div>
    <div class="mt-4 grid align-items-center justify-content-center">
      <div class="surface-card p-4 shadow-2 border-round col-4">
        <div class="text-center mb-5">
          <div class="text-900 text-3xl font-medium mb-3">Password Reset</div>
        </div>

        <form @submit.prevent="submit(!v$.$invalid)" class="text-center">
          <div>
            <div class="field">
              <small v-if="v$.form.token.$invalid || v$.form.token.$pending.$response" class="p-error">Token invalid or expired.</small>
            </div>

            <div class="field">
              <Password
                id="password"
                type="password"
                v-model="form.password"
                :class="{
                  'p-invalid': v$.form.password.$invalid && submitted,
                  'w-7': true,
                }"
                toggleMask
                :feedback="false"
                placeholder="Enter password"
              />
              <small v-if="(v$.form.password.$invalid && submitted) || v$.form.password.$pending.$response" class="p-error"
                ><br />{{ v$.form.password.required.$message }}</small
              >
            </div>

            <div class="field">
              <Password
                id="password_confirm"
                type="password"
                v-model="form.password_confirm"
                :class="{
                  'p-invalid': v$.form.password_confirm.$invalid && submitted,
                  'w-7': true,
                }"
                toggleMask
                :feedback="false"
                placeholder="And confirm it again"
              />
              <small v-if="(v$.form.password_confirm.$invalid && submitted) || v$.form.password_confirm.$pending.$response" class="p-error"
                ><br />
                {{ v$.form.password_confirm.required.$message }}
                <template v-if="v$.form.password_confirm.required && v$.form.password_confirm.sameAs"><br /></template>
                {{ v$.form.password_confirm.sameAs.$message }}
              </small>
            </div>

            <PvButton label="Change password" icon="pi pi-user" class="w-7" type="submit"></PvButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, sameAs } from "@vuelidate/validators";
import { useOauthStore } from "@/stores/oauth";
import { useUserStore } from "@/stores/user";
import logger from "@/logging";
import { usePreloadsStore } from "@/stores/preloads";
import { useToast } from "primevue/usetoast";
import apiService from "@/services/api/api.service";

export default {
  data: () => ({
    form: {
      token: "",
      password: "",
      password_confirm: "",
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
  validations() {
    return {
      form: {
        token: { required },
        password: { required },
        password_confirm: { sameAs: sameAs(this.form.password) },
      },
    };
  },
  computed: {
    token() {
      return this.$route.params.token;
    },
  },
  mounted() {
    this.checkToken();
  },
  methods: {
    checkToken() {
      apiService
        .userPasswordResetValidate({ token: this.token })
        .then((res) => {
          this.form.token = this.token;
        })
        .catch((error) => {
          this.form.token = null;
          logger.default.error("invalid token:", error);
          this.toast.add({
            severity: "error",
            summary: "Password Reset",
            detail: "Invalid token or expired",
            life: 5000,
          });
        });
    },
    submit(isFormValid) {
      this.submitted = true;

      if (!isFormValid) {
        return;
      }

      apiService
        .userPasswordResetConfirm({
          token: this.form.token,
          password: this.form.password,
        })
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Password Reset",
            detail: "Changed with success",
            life: 5000,
          });

          if (this.oauthStore.loggedIn) {
            this.userStore.logout().then(() => {
              this.$router.replace({ name: "login_form" });
            });
          } else {
            this.$router.replace({ name: "login_form" });
          }
        })
        .catch((error) => {
          logger.default.error("cannot change password:", error);
          this.toast.add({
            severity: "error",
            summary: "Password Reset",
            detail: "An error occured, please try again later",
            life: 5000,
          });
        });
    },
  },
};
</script>
