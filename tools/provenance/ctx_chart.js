  /* ---------- context chart (an illustrative shape, not measured data) ---------- */
  // Made-up but plausible values: the single session fills its window, is compacted at
  // step 9 and loses early detail; the lead only takes in each helper's short summary.
  var solo = [4,14,26,38,50,61,72,84,95,46,57];
  var lead = [4,7,10,12,15,17,20,22,25,27,30];
  var CX0 = 64, CX1 = 640, CY0 = 40, CY1 = 236;
  function sx(i){ return CX0 + i*(CX1-CX0)/10; }
  function sy(v){ return CY1 - v*(CY1-CY0)/100; }
  function about(v){ return 'about ' + Math.round(v/10)*10 + '%'; }
  var c = '';
  c += '<text x="16" y="18" class="d-sub">Context used (share of the window)</text>';
  c += '<text x="'+CX1+'" y="18" text-anchor="end" class="d-band-text">ILLUSTRATIVE · NOT MEASURED</text>';
  [[0,'empty'],[50,'half'],[100,'full']].forEach(function(t){
    c += '<line x1="'+CX0+'" y1="'+sy(t[0])+'" x2="'+CX1+'" y2="'+sy(t[0])+'" class="d-grid"/>';
    c += '<text x="'+(CX0-10)+'" y="'+(sy(t[0])+4)+'" text-anchor="end" class="d-small">'+t[1]+'</text>';
  });
  [0,2,4,6,8,10].forEach(function(i){
    c += '<text x="'+sx(i)+'" y="'+(CY1+18)+'" text-anchor="middle" class="d-small">'+i+'</text>';
  });
  c += '<text x="'+((CX0+CX1)/2)+'" y="'+(CY1+40)+'" text-anchor="middle" class="d-sub">steps into a long task</text>';
  function pts(arr){ return arr.map(function(v,i){ return sx(i)+','+sy(v); }).join(' '); }
  c += '<polyline points="'+pts(solo)+'" fill="none" stroke="var(--ink-2)" stroke-width="2.5" stroke-dasharray="7 5" stroke-linejoin="round" stroke-linecap="round"/>';
  c += '<polyline points="'+pts(lead)+'" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-dasharray="7 5" stroke-linejoin="round" stroke-linecap="round"/>';
  c += '<text x="'+(sx(9)-10)+'" y="'+(sy(46)+4)+'" text-anchor="end" class="d-label">compacted: early details summarized away</text>';
  c += '<circle cx="'+sx(10)+'" cy="'+sy(solo[10])+'" r="4.5" fill="var(--ink-2)" stroke="var(--surface)" stroke-width="2"/>';
  c += '<circle cx="'+sx(10)+'" cy="'+sy(lead[10])+'" r="4.5" fill="var(--accent)" stroke="var(--surface)" stroke-width="2"/>';
  c += '<text x="'+(sx(10)+12)+'" y="'+(sy(solo[10])+4)+'" class="d-label">One long session</text>';
  c += '<text x="'+(sx(10)+12)+'" y="'+(sy(lead[10])+4)+'" class="d-label">Lead + helpers</text>';
  c += '<line id="ctx-x" x1="0" y1="'+CY0+'" x2="0" y2="'+CY1+'" stroke="var(--ink-3)" stroke-width="1" visibility="hidden"/>';
  c += '<circle id="ctx-d1" r="5" fill="var(--ink-2)" stroke="var(--surface)" stroke-width="2" visibility="hidden"/>';
  c += '<circle id="ctx-d2" r="5" fill="var(--accent)" stroke="var(--surface)" stroke-width="2" visibility="hidden"/>';
  c += '<rect id="ctx-hit" x="'+(CX0-20)+'" y="'+CY0+'" width="'+(CX1-CX0+40)+'" height="'+(CY1-CY0)+'" fill="transparent"/>';
  var chart = document.getElementById('ctx-chart');
  chart.innerHTML = c;
  var tbody = document.querySelector('#ctx-table tbody');
  tbody.innerHTML = solo.map(function(v,i){ return '<tr><th scope="row">'+i+'</th><td>'+about(v)+'</td><td>'+about(lead[i])+'</td></tr>'; }).join('');
  var hit = document.getElementById('ctx-hit'), xl = document.getElementById('ctx-x'),
      d1 = document.getElementById('ctx-d1'), d2 = document.getElementById('ctx-d2'),
      tip = document.getElementById('ctx-tip'), wrap = document.getElementById('ctx-wrap');
  function hide(){ xl.setAttribute('visibility','hidden'); d1.setAttribute('visibility','hidden'); d2.setAttribute('visibility','hidden'); tip.hidden = true; }
  function readout(i){
    var m = chart.getScreenCTM(); if(!m) return;
    xl.setAttribute('x1', sx(i)); xl.setAttribute('x2', sx(i)); xl.setAttribute('visibility','visible');
    d1.setAttribute('cx', sx(i)); d1.setAttribute('cy', sy(solo[i])); d1.setAttribute('visibility','visible');
    d2.setAttribute('cx', sx(i)); d2.setAttribute('cy', sy(lead[i])); d2.setAttribute('visibility','visible');
    tip.innerHTML = '<b>Step '+i+' · illustrative</b><br><span class="sw" style="background:var(--ink-2)"></span>One long session: '+about(solo[i])+'<br><span class="sw" style="background:var(--accent)"></span>Lead + helpers: '+about(lead[i]);
    tip.hidden = false;
    var anchor = chart.createSVGPoint(); anchor.x = sx(i); anchor.y = sy(Math.max(solo[i], lead[i]));
    var sc = anchor.matrixTransform(m);
    var wr = wrap.getBoundingClientRect();
    var left = sc.x - wr.left, half = tip.offsetWidth/2 + 4;
    left = Math.max(half, Math.min(wr.width - half, left));
    tip.style.left = left + 'px';
    tip.style.top = Math.max(tip.offsetHeight + 4, sc.y - wr.top - 6) + 'px';
  }
  // Pointer, touch and keyboard all move the same readout.
  function fromPointer(e){
    var m = chart.getScreenCTM(); if(!m) return;
    var pt = chart.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
    var p = pt.matrixTransform(m.inverse());
    readout(Math.max(0, Math.min(10, Math.round((p.x - CX0) / ((CX1-CX0)/10)))));
  }
  hit.addEventListener('pointermove', fromPointer);
  hit.addEventListener('pointerdown', fromPointer);
  hit.addEventListener('pointerleave', hide);
  var step = 0;
  chart.addEventListener('focus', function(){ readout(step); });
  chart.addEventListener('blur', hide);
  chart.addEventListener('keydown', function(e){
    if(e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    e.preventDefault();
    step = Math.max(0, Math.min(10, step + (e.key === 'ArrowRight' ? 1 : -1)));
    readout(step);
  });
