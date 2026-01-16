// DOM要素の取得
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const langButton = document.getElementById('langButton');

// 会話履歴を保持
let conversationHistory = [];

// 言語切り替えボタンのイベントリスナー
langButton.addEventListener('click', () => {
    const newLang = currentLanguage === 'ja' ? 'en' : 'ja';
    setLanguage(newLang);
});

// メッセージを追加する関数
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    // ウェルカムメッセージを削除
    const welcomeMessage = chatContainer.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    // 自動スクロール
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// タイピングインジケーターを表示
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant';
    typingDiv.id = 'typing-indicator';

    const indicatorDiv = document.createElement('div');
    indicatorDiv.className = 'typing-indicator';
    indicatorDiv.innerHTML = '<span></span><span></span><span></span>';

    typingDiv.appendChild(indicatorDiv);
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// タイピングインジケーターを削除
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// メッセージを送信
async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) return;

    // ユーザーメッセージを表示
    addMessage(message, true);

    // 会話履歴に追加
    conversationHistory.push({
        role: 'user',
        content: message
    });

    // 入力欄をクリア
    userInput.value = '';
    userInput.style.height = 'auto';

    // 送信ボタンを無効化
    sendButton.disabled = true;

    // タイピングインジケーターを表示
    showTypingIndicator();

    try {
        // APIにリクエストを送信
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory,
                language: currentLanguage
            })
        });

        if (!response.ok) {
            throw new Error('APIリクエストに失敗しました');
        }

        const data = await response.json();

        // タイピングインジケーターを削除
        hideTypingIndicator();

        // AIの応答を表示
        addMessage(data.response, false);

        // 会話履歴に追加
        conversationHistory.push({
            role: 'assistant',
            content: data.response
        });

    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        addMessage(t('errorMessage'), false);
    } finally {
        // 送信ボタンを有効化
        sendButton.disabled = false;
        userInput.focus();
    }
}

// テキストエリアの自動リサイズ
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Enterキーで送信（Shift+Enterで改行）
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// 送信ボタンのクリックイベント
sendButton.addEventListener('click', sendMessage);

// ページ読み込み時に入力欄にフォーカス
window.addEventListener('load', () => {
    userInput.focus();
});
