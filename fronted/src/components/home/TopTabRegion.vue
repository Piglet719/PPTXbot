<template>
  <div class="form-control">
    <img class="logo" src="@/components/home/content/assets/logo.png" alt="Power Paper Logo"/>
    <span class="title">Power Paper : 死線戰士小幫手</span>
  </div>
  <div class="diamod">
    <div>wowowowo</div>
  </div>
</template>

<script>
export default {
  name: 'UploadPage',
  methods: {
    selectFile() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        console.log('File selected:', file);
        // 在這裡處理文件上傳邏輯
      }
    },
  },
};
</script>

<style>
.logo{
  height: 45px;
}

.title{
  color: var(--textprimarygrey-1);
  font-family: "Noto Sans TC-Bold", Helvetica;
  font-weight: 800;
  font-size: 15px;
  padding: 5px 10px 10px 5px;
}

.form-control {
    position: relative;
    margin-top: 10px;
    margin-left: 10px;
}


.diamod {
    left: 50%;
    display: inline-block;
    height: 70px;
    width: 100%;
    color: #A5C2BB;
    background:	#A5C2BB;
  }
</style>
