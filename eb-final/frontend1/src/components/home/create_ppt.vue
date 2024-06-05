<template>
  <div v-show="contentType == 3">
    <div class="Reupload-section">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      <span class="section-title">請選擇要執行的動作</span>
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
      <button class="action-btn" @click="viewRecentPDF">
        開啟pdf
      </button>
    </div>
  </div>

  <div v-show="contentType == 4">
    <div class="Reupload-section">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      下載中...
    </div>
  </div>

  <div v-show="contentType == 5">
    <div class="Reupload-section">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      下載完成！
    </div>
    <button class="pdf-input" @click="emitChangeContentType(2)">
      重新匯入PDF
    </button>
  </div>

  <div v-show="contentType == 6">
    <div class="Reupload-section">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      下載失敗！
    </div>
    <button class="pdf-input" @click="emitChangeContentType(2)">
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
    emitChangeContentType(4);
    const response = await axios.post('http://testeb-env.eba-3tf5iadp.us-east-1.elasticbeanstalk.com/api/create_ppt', {
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
    emitChangeContentType(5);
  } catch (error) {
    console.error('Error generating file:', error);
    emitChangeContentType(6);
  }
};

const viewRecentPDF = async () => {
  try {
    const response = await axios.get('http://testeb-env.eba-3tf5iadp.us-east-1.elasticbeanstalk.com/api/recent_file');
    if (response.data.filename) {
      const fileUrl = `http://testeb-env.eba-3tf5iadp.us-east-1.elasticbeanstalk.com/api/display_file?file=${response.data.filename}`;
      window.open(fileUrl, '_blank');
    } else {
      alert('沒有找到最近的PDF文件');
    }
  } catch (error) {
    console.error('Error fetching recent file:', error);
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
  font-size: 15px;
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
  justify-content: center;
  margin-bottom: 20px;

  .option-item {
    margin: 0 5px;
    display: flex;
    align-items: center;
    .action-btn {
      background-color: white;
      border: 1px solid white;
      padding: 0px 10px;
      cursor: pointer;
      margin: 0 5px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      border-radius: 4px;
    }
  }
}

.buttons {
  display: flex;
  justify-content: flex-left;
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
    font-size: 15px;
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
  font-size: 15px;
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
  font-size: 15px;
}
</style>