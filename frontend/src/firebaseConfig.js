import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyBfduMuZYinYKipD9lx6AnydPKtKgdzBwg",
    authDomain: "lvlhubfinal.firebaseapp.com",
    projectId: "lvlhubfinal",
    storageBucket: "lvlhubfinal.firebasestorage.app",
    messagingSenderId: "553876578787",
    appId: "1:553876578787:web:13d278f8124cc7deb940d6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };
