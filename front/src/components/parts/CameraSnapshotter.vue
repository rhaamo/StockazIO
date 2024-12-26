<template>
  <div class="camera">
    <div class="wrapper">
      <PvButton label="Close" class="mb-2 p-button-danger" @click.prevent="closeDialog()" />
      <PvButton v-if="isPlaying" label="Snap!" class="mb-2 ml-2" @click.prevent="takePhoto()" />
      <PvButton v-if="isPhotoTaken" label="save" class="mb-2 ml-2 p-button-success" @click.prevent="saveAndClose()" />

      <div class="grid">
        <div class="col-6">
          <div v-if="!isPlaying">Please wait while the camera initialize...</div>
          <video id="camera" ref="camera" autoplay playsinline></video>
          <canvas v-show="isPhotoTaken" id="photoTaken" ref="canvas" class="ml-2"> </canvas>
        </div>

        <div class="col-6">
          <img id="photo" ref="photo" class="vertical-align-middle" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  inject: ["dialogRef"],
  setup: () => ({}),
  data: () => ({
    isPhotoTaken: false,
    isPlaying: false,
    width: 320,
    height: 0,
  }),
  computed: {},
  created() {
    this.createCameraElement();
  },
  methods: {
    closeDialog() {
      this.stopCameraStream();
      this.dialogRef.close();
    },
    saveAndClose() {
      this.stopCameraStream();
      this.dialogRef.close({
        picture: document.getElementById("photoTaken").toDataURL("image/jpeg"),
      });
    },
    createCameraElement() {
      let constraints = (window.constraints = {
        audio: false,
        video: true,
      });

      navigator.mediaDevices
        .getUserMedia(constraints)
        .then((stream) => {
          this.$refs.camera.srcObject = stream;
          this.$refs.camera.play();

          this.height = this.$refs.camera.videoHeight / (this.$refs.camera.videoWidth / this.width);

          if (isNaN(this.height)) {
            this.height = this.width / (4 / 3);
          }

          this.$refs.camera.setAttribute("width", this.width);
          this.$refs.camera.setAttribute("height", this.height);

          this.$refs.canvas.setAttribute("width", this.width);
          this.$refs.canvas.setAttribute("height", this.height);

          this.isPlaying = true;
        })
        .catch((error) => {
          this.dialogRef.close({ error: error });
        });
    },
    stopCameraStream() {
      const tracks = this.$refs.camera.srcObject.getTracks();

      tracks.forEach((track) => {
        track.stop();
      });
      this.isPlaying = false;
    },
    takePhoto() {
      this.isPhotoTaken = !this.isPhotoTaken;

      const context = this.$refs.canvas.getContext("2d");

      this.$refs.canvas.width = this.$refs.camera.videoWidth;
      this.$refs.canvas.height = this.$refs.camera.videoHeight;

      context.translate(this.$refs.canvas.width, 0);
      context.scale(-1, 1);

      context.drawImage(this.$refs.camera, 0, 0);

      this.$refs.photo.setAttribute("src", this.$refs.canvas.toDataURL("image/jpeg"));
    },
    downloadImage() {
      const download = document.getElementById("downloadPhoto");
      const canvas = document.getElementById("photoTaken").toDataURL("image/jpeg").replace("image/jpeg", "image/octet-stream");
      download.setAttribute("href", canvas);
    },
  },
};
</script>

<style scoped>
canvas#photoTaken {
  display: none;
}

video#camera {
  width: 340px;
}

img#photo {
  width: 340px;
}
</style>
