<template>
    <!-- <div id="footer"> -->
    <div class="input-section">
        <input type="text" placeholder="Input here..." />
        <button class="send-btn">
            <img src="@/components/home/content/assets/send_msg.png" />
        </button>
    </div>
    <!-- </div> -->
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
.input-section input {
    /* padding-left: 20%; */
    font-family: "Noto Sans TC-Bold", Helvetica;
    width: 100px;
    border: none;
    border-width: 0px;
    border-bottom: 2px solid #A5C2BB;
    outline: none;
    padding: 10px;
  /* border: 1px solid #ccc; */
    border-radius: 4px;
    margin-right: 10px;
    width: calc(100% - 800px);
}
.input-section {
  display: flex;
  align-items: center;
  justify-content: center;
}
.send-btn{
    border: none;
    background-color: white;
    cursor: pointer;
}
.send-btn img{
    height: 25px;
}


</style>
  