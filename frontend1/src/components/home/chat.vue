<template>
  <div id="app">
    <footer id="bottom-tab-region">
      <div class="input-section">
        <input type="text" placeholder="Input here..." v-model="inputText" @keyup.enter="sendMessage" />
        <button class="send-btn" @click="sendMessage">
          <img src="@/components/home/content/assets/send_msg.png" />
        </button>
      </div>
    </footer>

    <div v-show="showQuestionHistory" class="question-history-container">
      <div class="question-history">
        <div v-for="(question, index) in questions" :key="index" class="question" :style="{ width: '400px', height: getHeight(question) + 'px' }">
          {{ question }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const inputText = ref('');
const questions = ref([]);
const showQuestionHistory = ref(false);

function sendMessage() {
  const question = inputText.value.trim();
  if (question !== '') {
    questions.value.push(question);
    inputText.value = '';
    showQuestionHistory.value = true;

    // 發送 POST 請求
    fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // 在收到回覆後，您可以將回覆消息添加到聊天框中
    })
    .catch(error => {
      console.error('Error sending message:', error);
    });

    nextTick(() => {
      adjus
    })
  }
}

function getHeight(question) {
  const maxWidth = 400; // 固定宽度 200px
  const lineHeight = 20; // 假设每行高度为 20px

  // 创建一个临时的隐藏元素用于测量实际高度
  const tempDiv = document.createElement('div');
  tempDiv.style.position = 'absolute';
  tempDiv.style.visibility = 'hidden';
  tempDiv.style.width = `${maxWidth}px`;
  tempDiv.style.fontSize = '14px';
  tempDiv.style.lineHeight = `${lineHeight}px`;
  tempDiv.style.whiteSpace = 'pre-wrap'; // 保持空白和换行符
  tempDiv.style.wordWrap = 'break-word'; // 自动换行
  tempDiv.innerText = question;

  document.body.appendChild(tempDiv);
  const height = tempDiv.scrollHeight; // 获取内容的高度
  document.body.removeChild(tempDiv);

  return height;
}
</script>

<style scoped lang="scss">
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

.question-history-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 50px; /* 為了避免問題被覆蓋住，給足夠的上偏移 */
}

.question-history {
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.question {
  font-size: 14px;
  word-wrap: break-word;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  margin-bottom: 5px;
}
</style>
