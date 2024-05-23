<template>
  <div v-show="contentType == 3">
    <div class="Reupload-section">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      <span class="section-title">請選擇/輸入要輸出的頁面</span>
    </div>
    <div class="buttons">
      <button class="action-btn" @click="emitChangeContentType(0)">
        重新匯入PDF
      </button>
      <button class="action-btn" @click="emitChangeContentType(2)">
        重新匯入PPT檔案
      </button>
      <button class="action-btn" @click="generateFile">
        產生檔案
      </button>
    </div>
  </div>

  <div v-show="contentType == 4">
    <div class="Reupload-section">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      已轉檔完成！
    </div>
    <div class="actions">
      <button class="download-btn" @click="downloadPPT">下載Power Point</button>
    </div>
    <button class="pdf-input" @click="emitChangeContentType(0)">
      重新匯入PDF
    </button>
  </div>
</template>

<script setup>
import { ref, defineEmits, defineProps } from "vue";
import axios from 'axios';

const props = defineProps({
  contentType: Number
});

const emit = defineEmits(['changeContentType']);

const selectedOptions = ref([]);

const emitChangeContentType = (type) => {
  console.log(`Changing content type to ${type}`);
  emit('changeContentType', type);
};

const generateFile = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/create_ppt', {
      selectedOptions: selectedOptions.value
    }, {
      responseType: 'blob'
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'presentation.pptx');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error('Error generating file:', error);
  }
};
</script>


<style scoped lang="scss">
.Reupload-section {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 10px;
}

.section-title {
  margin-left: 10px; /* Adjusted to add some space between image and text */
}

.robot-img {
  height: 30px;
  padding: 10px 10px 10px 10px;
}

.actions {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20px;

  .option-item {
    margin: 0 5px;
    display: flex;
    align-items: center;
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
}

.buttons {
  display: flex;
  justify-content: flex-end;
  .action-btn {
    background-color: #4285f4;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    margin-left: 10px;
    margin: 0 20px;
    display: flex;
    align-items: right;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    font-size: 10px;
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
</style>