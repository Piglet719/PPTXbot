<template>
  <div id="home-root">
    <div id="top-tab-region">
      <img class="logo" src="@/components/home/content/assets/logo.png" alt="Power Paper Logo"/>
      <span class="title">Power Paper : 死線戰士小幫手</span>
      <div class="diamod">
        <div>wowowowo</div>
      </div>
    </div>
    <div class="content-region">
      <div v-show="selectedTabIndex == 0">
        <div class="upload-section" v-show="contentType == 0">
          <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
          請匯入論文PDF完整檔案
          <input type="file" @change="handleFileUpload" ref="fileInput" style="display: none;" />
          <button class="pdf-input" @click="triggerFileInput">
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
      </div>
    </div>
    <footer id="bottom-tab-region">
      <div class="input-section">
        <input type="text" placeholder="Input here..." />
        <button class="send-btn">
          <img src="@/components/home/content/assets/send_msg.png" />
        </button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const selectedTabIndex = ref(0);
const contentType = ref(0);

function changeContentType(type) {
  contentType.value = type;
}

const fileInput = ref(null);

function triggerFileInput() {
  fileInput.value.click();
}

function handleFileUpload(event) {
  const file = event.target.files[0];
  if (file) {
    console.log('File selected:', file);
    // 在這裡處理文件上傳邏輯
    // 例如，你可以使用 FormData 將文件發送到服務器
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/upload', {
      method: 'POST',
      body: formData,
    }).then(response => {
      if (response.ok) {
        changeContentType(1);
      } else {
        console.error('File upload failed');
      }
    }).catch(error => {
      console.error('Error uploading file:', error);
    });
  }
}
</script>

<style scoped lang="scss">
#home-root {
  width: 100%;
  height: 100%;

  #top-tab-region {
    background-color: #A5C2BB;
    height: 100px;
    width: 100%;
    .logo {
      height: 45px;
    }
    .title {
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
      background: #A5C2BB;
    }
  }

  #bottom-tab-region {
    width: 100%;
    .input-section {
      display: flex;
      align-items: center;
      justify-content: center;
      input {
        font-family: "Noto Sans TC-Bold", Helvetica;
        width: 100px;
        border: none;
        border-width: 0px;
        border-bottom: 2px solid #A5C2BB;
        outline: none;
        padding: 10px;
        border-radius: 4px;
        margin-right: 10px;
        width: calc(100% - 800px);
      }
      .send-btn {
        border: none;
        background-color: white;
        cursor: pointer;
        img {
          height: 25px;
        }
      }
    }
  }

  .content-region {
    width: 100%;
    height: calc(100% - 200px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: end;

    .upload-section,
    .Reupload-section,
    .outside-Reupload-section {
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #ffffff;
      padding: 20px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      border-radius: 8px;
      margin-bottom: 20px;
      font-size: 10px;
    }

    .robot-img {
      height: 30px;
      padding: 10px 10px 10px 10px;
    }

    .pdf-input {
      background-color: #4285f4;
      color: white;
      border: none;
      padding: 10px 20px;
      cursor: pointer;
      margin-left: 500px;
      display: flex;
      align-items: center;
      border-radius: 10;
      font-size: 10px;
    }

    .robot-section {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .actions {
      display: flex;
      justify-content: center;
      margin-bottom: 20px;
      .action-btn {
        background-color: white;
        border: 1px solid white;
        padding: 10px 20px;
        cursor: pointer;
        margin: 0 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-radius: 4px;
      }
    }

    .download-btn {
      background-color: #91c5b5;
      border: 1px solid white;
      padding: 10px 20px;
      cursor: pointer;
      margin: 0 5px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      border-radius: 4px;
    }
  }
}
</style>
