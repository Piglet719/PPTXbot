// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, collection, getDocs,getDoc, setDoc , doc} from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDuF4cljN9EPkNLRRHLOjfqEEByFdPPAL8",
  authDomain: "cookielife-de262.firebaseapp.com",
  projectId: "cookielife-de262",
  storageBucket: "cookielife-de262.appspot.com",
  messagingSenderId: "92600885191",
  appId: "1:92600885191:web:4e2175538c90866f9743e2"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

const db = getFirestore(app);

async function getUser(username) {

  const docRef = doc(db, "user", username);
  const docSnap = await getDoc(docRef);
  
  if (docSnap.exists()) {
    console.log("Document data:", docSnap.data());
    return docSnap;
  } else {
    // doc.data() will be undefined in this case
    console.log("No such document!");
    return null;
  }
}


async function getUsers() {
  const user = collection(db, 'user');

  const userName = await getDocs(user);

  // const results = []
  // for(var i=0; i<userName.docs.length; i++){
  //     results.push(userName.docs[i].data())
  // }
  // var a =   ['student1','student2',...,'student100']; 
  // var b = [];
  // for(var i=0; i<a.length; i++){
  //   b.push(a[i].substring(7))
  // }


  // var a =   ['student1','student2',...,'student100']; 
  // var b = a.map((e)=>e.substring(7))

  // [1, 2, 3, ..., 100]

  // return  userName.docs.map((e)=>e.data())
  return userName.docs;
}

async function createUser(userName, password) {
  await setDoc(doc(db, "user", userName), {
    password: password,
  });
}

async function createDiary(title,content) {
  await setDoc(doc(db, "diary", title), {
    text: content,
  });
}

async function getDiary() {
  const diary = collection(db, 'diary');
  const title = await getDocs(diary);
  return title.docs;
}

// todo delete
const a = 1;
const b = 3;


export default {
  getUsers,
  getUser,
  createUser,
  createDiary,
  getDiary
}