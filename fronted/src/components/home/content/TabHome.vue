<template>
  
  <div class="upload-section" v-show="contentType == 0">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      請匯入論文PDF完整檔案
    <button class="pdf-input" @click="changeContentType(1)">
      匯入 PDF
    </button>
  </div>

  <div class="outside-Reupload-section" v-show="contentType == 1">
  <div class="Reupload-section">
    <div class="robot-section">
        <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
        資料分析中......
    </div>
  </div>
    <button class="pdf-input" @click="changeContentType(2)">
        重新匯入PDF
    </button>
  <!-- </div> -->
</div>

  <div v-show="contentType == 2">
    <div class="Reupload-section">
        <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
        請選擇是否要匯入PPT模板
    </div>
    <div class="actions">
          <button class="action-btn" @click="changeContentType(3)">Yes</button>
          <button class="action-btn" @click="changeContentType(3)">No</button>
    </div>
    <button class="pdf-input" @click="changeContentType(0)">
        重新匯入PDF
    </button>
  </div>

  <div v-show="contentType == 3">
    <div class="Reupload-section">
        <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
        請選擇/輸入要輸出的頁面
    </div>
    <div class="actions">
          <button class="action-btn" @click="changeContentType(4)">Introduction</button>
          <button class="action-btn" @click="changeContentType(4)">Related Work</button>
          <button class="action-btn" @click="changeContentType(4)">Methdology</button>
          <button class="action-btn" @click="changeContentType(4)">Conclusion</button>
        </div>
    <button class="pdf-input" @click="changeContentType(0)">
        重新匯入PDF
    </button>
  </div>

  <div v-show="contentType == 4">
    <div class="Reupload-section">
        <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
        已轉檔完成！
    </div>
    <div class="actions">
          <button class="download-btn">下載Power Point</button>
        </div>
    <button class="pdf-input" @click="changeContentType(0)">
        重新匯入PDF
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from "vue";
const contentType = ref(0);

// export default {
//   name: 'UploadPage',
//   methods: {
//     selectFile() {
//       this.$refs.fileInput.click();
//     },
//     handleFileUpload(event) {
//       const file = event.target.files[0];
//       if (file) {
//         console.log('File selected:', file);
//         // 在這裡處理文件上傳邏輯
//       }
//     },
//   },
// };

function changeContentType(type) {
  //轉換登入和註冊頁面
  contentType.value = type;
}
</script>

<style>
.upload-section {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color:#FFFFFF;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 10px;
  /* width: calc(100% - 700px); */
  
}
.robot-img{
  height: 30px;
  padding: 10px 10px 10px 10px;
}
.pdf-input{
  background-color: #4285F4;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  /* margin-right: 10px; */
  margin-left: 500px;
  display: flex;
  align-items: center;
  border-radius: 10;
  font-size: 10px;
}

.Reupload-section {
    display: flex;
    align-items: center;
    justify-content: left; 
    /* background-color: red; */
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 10px;
  }

  .ouside-Reupload-section {
    background-color: blue;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 10px;
    width: calc(100% - 500px);
  }
  .robot-section{
    display: flex;
    align-items: center;
    justify-content: center;
    /* background-color: yellow; */
  }
  .actions {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
.action-btn {
  background-color: white;
  border: 1px solid white;
  padding: 10px 20px;
  cursor: pointer;
  margin: 0 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.download-btn {
  background-color: #91C5B5;
  border: 1px solid white;
  padding: 10px 20px;
  cursor: pointer;
  margin: 0 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

</style>
