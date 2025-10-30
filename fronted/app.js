const base = ''; // set backend URL when deployed (e.g. https://your-backend.onrender.com)
const promptEl = document.getElementById('prompt');
const responseEl = document.getElementById('response');
const imageInput = document.getElementById('imageInput');
const askTextBtn = document.getElementById('askText');
const askImageBtn = document.getElementById('askImage');

async function postJSON(url, data){
  const res = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
  return res.json();
}

askTextBtn.addEventListener('click', async ()=>{
  const prompt = promptEl.value.trim();
  if(!prompt){alert('Type a question'); return;}
  responseEl.textContent = 'Thinking...';
  try{
    const data = await postJSON(base + '/api/chat', {prompt});
    if(data.ok) responseEl.textContent = data.text;
    else responseEl.textContent = 'Error: ' + (data.error||JSON.stringify(data));
  }catch(e){ responseEl.textContent = 'Network error: '+e; }
});

askImageBtn.addEventListener('click', async ()=>{
  const file = imageInput.files[0];
  const prompt = promptEl.value || 'Solve or explain the question in the image step-by-step:';
  if(!file){ alert('Choose an image'); return; }
  responseEl.textContent = 'Uploading...';
  const fd = new FormData();
  fd.append('image', file);
  fd.append('prompt', prompt);
  try{
    const res = await fetch(base + '/api/image', {method:'POST', body:fd});
    const data = await res.json();
    if(data.ok) responseEl.textContent = data.text;
    else responseEl.textContent = 'Error: '+(data.error||JSON.stringify(data));
  }catch(e){ responseEl.textContent = 'Network error: '+e; }
});