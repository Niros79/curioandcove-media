import glob
MARK = '<!-- kit-ajax -->'
JS = MARK + '''<script>
document.querySelectorAll('form[action*="app.kit.com/forms/"]').forEach(function(f){
  f.addEventListener('submit',function(e){
    if(f.dataset.native)return; e.preventDefault();
    var b=f.querySelector('button'); if(b){b.disabled=true;b.textContent='Sending...';}
    fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}})
      .then(function(r){return r.json();})
      .then(function(d){ if(d&&d.status==='success'){location.href='/thank-you/';} else {throw 0;} })
      .catch(function(){ f.dataset.native=1; f.submit(); });
  });
});
</script>
'''
n=0
for p in glob.glob('/home/claude/site_out/**/index.html', recursive=True):
    s=open(p).read()
    if 'app.kit.com/forms/10059486' in s and MARK not in s:
        s=s.replace('</body>', JS+'</body>',1); open(p,'w').write(s); n+=1
print(n)
