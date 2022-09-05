<template>
  <template v-if="isLoaded">
    <header>my super app</header>

    <RouterView />
  </template>
  <template v-else>oh no no preloaded stuff :(</template>
</template>

<script>
import { useOauthStore } from "@/stores/oauth";
import { useUserStore } from "@/stores/user";
import { useServerStore } from "@/stores/server";
import { usePreloadsStore } from "@/stores/preloads";

export default {
  setup() {
    const oauthStore = useOauthStore();
    const userStore = useUserStore();
    const serverStore = useServerStore();
    const preloadsStore = usePreloadsStore();
    return { oauthStore, userStore, serverStore, preloadsStore };
  },
  created() {
    // doesn't work...
    this.preloadsStore.preloadStuff().then(() => {
      console.log("preloading finished");
      this.isLoaded = true;
    });
  },
  mounted() {},
  data() {
    return {
      isLoaded: false,
    };
  },
};
</script>
