<template>
    <div class="container">
        <h5>{{ title }}</h5>
        <span>{{ message }}</span>
    </div>
</template>

<script>
    export default {
      props: {
        title: String,
        message: String
      }
    }
</script>