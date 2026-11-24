"use strict";
let state, dirty = false, busy = false, presentation = "detailed";
const $ = id => document.getElementById(id);
async function api(path, data) {
  const options = data === undefined ? {} : {method:"POST", headers:{"Content-Type":"application/json","X-Local-Review":"1"}, body:JSON.stringify(data)};
  const response = await fetch(path, options), result = await response.json();
  if (!response.ok) throw new Error(result.error || "The request could not be completed.");
  return result;
}
function text(tag, value, className) {const n = document.createElement(tag); n.textContent = value; if(className)n.className=className; return n;}
function displayFile(){const f = state.files[$("file").value]; $("classification").textContent="Fixture classification: "+f.classification; $("file-content").textContent=f.text;}
function enableApproval(){
  const advisory = state.issues.some(i=>!i.blocking);
  const open = ["review","failed"].includes(state.stage);
  $("approve").disabled=busy || !open || dirty || state.blocking || (advisory && !state.acknowledgement) || !$("checked").checked;
  $("cancel").disabled=busy || !open;
  $("gate-note").textContent=dirty ? "Apply changes to rerun checks before approval." : state.blocking ? "Resolve all blocking issues. Approval is unavailable." : advisory && !state.acknowledgement ? "Review the advisory and record a one-time correction first." : "Approval applies only to this displayed draft. Any edit requires a fresh review.";
}
function render(){
  dirty=false; $("checked").checked=false;
  $("scenario").value=state.scenario; $("request").textContent=state.request; $("stage").textContent=state.stage;
  $("prepare").hidden=state.stage!=="request"; $("draft").hidden=state.stage==="request";
  $("recipient").replaceChildren(text("option","Choose the intended contact…")); $("recipient").options[0].value="";
  for(const [id,c] of Object.entries(state.contacts)){const o=text("option",c.name+" · "+c.email);o.value=id;$("recipient").append(o);}
  $("file").replaceChildren(); for(const [id,f] of Object.entries(state.files)){const o=text("option",f.name);o.value=id;$("file").append(o);}
  $("recipient").value=state.draft.recipient; $("file").value=state.draft.file; $("subject").value=state.draft.subject;$("message").value=state.draft.body; displayFile();
  const open=["review","failed"].includes(state.stage);
  for(const id of ["recipient","file","subject","message","apply"])$(id).disabled=!open;
  $("version").textContent="Draft version "+state.revision;
  $("review-title").textContent=state.stage==="sent"?"Decision recorded":state.stage==="cancelled"?"Interaction cancelled":state.stage==="failed"?"Send failed safely":state.stage==="request"?"You stay in control":state.blocking?"Pause and resolve the risks":state.issues.length?"A warning needs your judgement":state.stage==="sent"?"Decision recorded":"Ready for your review";
  $("review-note").textContent=state.stage==="request"?"Prepare a draft to inspect its recipient, attachment and planned action.":state.blocking?"Each concern has its own evidence and recovery action.":state.issues.length?"A keyword is not proof. Inspect the document and decide for this action only.":"No fixture rule raised a concern. This is not a guarantee that a real document is safe.";
  $("issues").replaceChildren();
  for(const i of state.issues){
    const card=text("div","","issue");card.append(text("div",i.blocking?"Blocking issue":"Advisory · may be incorrect","kind"));
    if($("explanation").value==="generic"){card.append(text("h3","Possible risk detected"),text("p","This email may contain sensitive information. Review before continuing."));}
    else{card.append(text("h3",i.title),text("p","Evidence: "+i.evidence),text("p","Why it matters: "+i.consequence),text("p","Next step: "+i.action));}
    $("issues").append(card);
  }
  $("ack-panel").hidden=!open || !state.issues.some(i=>i.id==="budget"); $("reason").value=state.acknowledgement;$("ack-status").textContent=state.acknowledgement?"Recorded for this draft only. No future permission was granted.":"";
  $("decision").hidden=!open; $("cancel").disabled=busy; $("fail").checked=state.fail_next;
  $("result").hidden=!state.result;$("result").textContent=state.result;
  $("events").replaceChildren();
  const labels={scenario_loaded:"Scenario loaded",fixture_draft_prepared:"Scripted draft prepared",draft_edited_and_rechecked:"Draft changed; approval invalidated; checks rerun",one_time_correction:"One-time warning correction recorded",exact_draft_reviewed:"Exact draft reviewed",mock_send_recorded:"Mock send recorded; no email sent",mock_send_failed:"Mock send failed; no success claimed",cancelled:"Cancelled without sending",failure_fixture_set:"Failure demonstration configured"};
  for(const e of state.events)$("events").append(text("li",(labels[e.event]||e.event)+" · v"+e.revision));
  enableApproval();
}
async function act(fn){if(busy)return;busy=true;$("error").hidden=true;enableApproval();try{await fn();}catch(e){$("error").textContent=e.message;$("error").hidden=false;}finally{busy=false;enableApproval();}}
$("load").onclick=()=>act(async()=>{state=await api("/api/scenario",{scenario:$("scenario").value});render();});
$("prepare").onclick=()=>act(async()=>{state=await api("/api/prepare",{});render();});
$("draft-form").onsubmit=e=>{e.preventDefault();act(async()=>{state=await api("/api/draft",{recipient:$("recipient").value,file:$("file").value,subject:$("subject").value,body:$("message").value});render();});};
for(const id of ["recipient","file","subject","message"])$(id).addEventListener("input",()=>{dirty=true;$("checked").checked=false;if(id==="file")displayFile();enableApproval();});
$("checked").onchange=enableApproval;
$("explanation").onchange=()=>{if(dirty){$("explanation").value=presentation;$("error").textContent="Apply draft changes before switching the warning presentation.";$("error").hidden=false;return;}presentation=$("explanation").value;render();};
$("ack").onclick=()=>act(async()=>{if(dirty)throw new Error("Apply draft changes before recording a correction.");state=await api("/api/acknowledge",{reason:$("reason").value});render();});
$("cancel").onclick=()=>act(async()=>{state=await api("/api/cancel",{});render();});
$("fail").onchange=()=>act(async()=>{state=await api("/api/failure",{fail:$("fail").checked});render();});
$("approve").onclick=()=>act(async()=>{if(dirty)throw new Error("Apply edits before approval.");const reviewed=await api("/api/review",{revision:state.revision,checked:$("checked").checked});state=await api("/api/send",{token:reviewed.token});render();});
api("/api/state").then(s=>{state=s;render();}).catch(e=>{$("error").textContent=e.message;$("error").hidden=false;});

