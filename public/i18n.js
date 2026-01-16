// 多言語対応の翻訳データ
const translations = {
    ja: {
        title: "AI チャットボット",
        subtitle: "Gemini AI を活用したチャットアプリ",
        welcomeTitle: "こんにちは！👋",
        welcomeMessage: "何でもお気軽に質問してください。",
        placeholder: "メッセージを入力...",
        errorMessage: "申し訳ございません。エラーが発生しました。もう一度お試しください。",
        language: "Language"
    },
    en: {
        title: "AI Chatbot",
        subtitle: "Chat app powered by Gemini AI",
        welcomeTitle: "Hello! 👋",
        welcomeMessage: "Feel free to ask me anything.",
        placeholder: "Type a message...",
        errorMessage: "Sorry, an error occurred. Please try again.",
        language: "言語"
    }
};

// 現在の言語を取得（デフォルトは日本語）
let currentLanguage = localStorage.getItem('language') || 'ja';

// 言語を設定する関数
function setLanguage(lang) {
    currentLanguage = lang;
    localStorage.setItem('language', lang);
    updateUILanguage();
}

// UIの言語を更新する関数
function updateUILanguage() {
    const t = translations[currentLanguage];

    // タイトルと説明
    document.querySelector('header h1').textContent = `🤖 ${t.title}`;
    document.querySelector('.subtitle').textContent = t.subtitle;

    // ウェルカムメッセージ
    const welcomeTitle = document.querySelector('.welcome-message h2');
    const welcomeMsg = document.querySelector('.welcome-message p');
    if (welcomeTitle) welcomeTitle.textContent = t.welcomeTitle;
    if (welcomeMsg) welcomeMsg.textContent = t.welcomeMessage;

    // プレースホルダー
    document.getElementById('userInput').placeholder = t.placeholder;

    // 言語ボタンのテキスト更新
    updateLanguageButton();
}

// 言語ボタンのテキストを更新
function updateLanguageButton() {
    const langButton = document.getElementById('langButton');
    if (langButton) {
        langButton.textContent = currentLanguage === 'ja' ? 'EN' : 'JP';
        langButton.setAttribute('aria-label', translations[currentLanguage].language);
    }
}

// 翻訳を取得する関数
function t(key) {
    return translations[currentLanguage][key] || key;
}

// ページ読み込み時に言語を適用
document.addEventListener('DOMContentLoaded', () => {
    updateUILanguage();
});
