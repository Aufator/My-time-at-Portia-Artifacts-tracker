/* Вход в аккаунт для страниц без трекеров (жители). Тот же Firebase-проект, что и в трекерах:
   вход запоминается браузером и действует сразу на всех страницах сайта. */
(()=>{const g=i=>document.getElementById(i);if(!g('acct'))return;
const FB={apiKey:"AIzaSyAO2K5j9-KHNdW42eoAntao_Yri6jJ6UiU",authDomain:"portia-tracker.firebaseapp.com",projectId:"portia-tracker",storageBucket:"portia-tracker.firebasestorage.app",messagingSenderId:"1089028624050",appId:"1:1089028624050:web:a2193d2f83e95747a103ab"};
const FU='https://www.gstatic.com/firebasejs/10.14.1/';let user=null;
const sum=g('acctSum'),note=t=>{g('aNote').textContent=t};
function ferr(e){const m={'auth/invalid-credential':'Неверная почта или пароль','auth/wrong-password':'Неверный пароль','auth/user-not-found':'Такого аккаунта нет','auth/email-already-in-use':'Эта почта уже зарегистрирована, нажми «Войти»','auth/weak-password':'Пароль слишком короткий (нужно от 6 символов)','auth/invalid-email':'Почта введена неверно','auth/missing-password':'Введи пароль','auth/operation-not-allowed':'В Firebase не включён вход по почте и паролю','auth/network-request-failed':'Нет связи с интернетом','auth/too-many-requests':'Слишком много попыток, подожди немного','permission-denied':'Нет доступа к базе: проверь правила Firestore'};return m[e.code]||('Ошибка: '+(e.code||e.message))}
function ui(){const on=!!user;g('aFields').hidden=on;g('aBtns').hidden=on;g('alogout').hidden=!on;sum.textContent=on?user.email:'Войти'}
ui();
document.addEventListener('click',e=>{const b=g('acct');if(b.open&&!b.contains(e.target))b.open=false});
(async()=>{try{
 const [A,Fa]=await Promise.all([import(FU+'firebase-app.js'),import(FU+'firebase-auth.js')]);
 const app=A.initializeApp(FB),auth=Fa.getAuth(app);
 Fa.onAuthStateChanged(auth,u=>{user=u;ui()});
 const cr=()=>[auth,g('aemail').value.trim(),g('apass').value];
 g('alogin').onclick=async()=>{try{note('Входим…');await Fa.signInWithEmailAndPassword(...cr());g('apass').value='';note('Вы вошли. Прогресс трекеров подтянется на их страницах.')}catch(e){note('⚠ '+ferr(e))}};
 g('areg').onclick=async()=>{try{note('Создаём аккаунт…');await Fa.createUserWithEmailAndPassword(...cr());g('apass').value=''}catch(e){note('⚠ '+ferr(e))}};
 g('areset').onclick=async()=>{try{const em=g('aemail').value.trim();if(!em){note('Введите почту, на неё придёт письмо для сброса пароля');return}await Fa.sendPasswordResetEmail(auth,em);note('Письмо для сброса пароля отправлено на '+em)}catch(e){note('⚠ '+ferr(e))}};
 g('alogout').onclick=async()=>{await Fa.signOut(auth);note('Вы вышли.')};
}catch(e){note('Вход недоступен (нет интернета или страница открыта не с сайта).')}})();
})();
