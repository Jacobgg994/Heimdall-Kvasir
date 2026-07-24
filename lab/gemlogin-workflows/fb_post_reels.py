#!/usr/bin/env python3
r"""
GemLogin: (Facebook) Post Reels
================================
สร้าง .gemlogin โพสต์ Facebook Reels — format ตรงตาม GemLogin export
Features: batch loop, media folder/custom, filename caption, audience, link collect

ใช้: python fb_post_reels.py && import เข้า GemLogin
"""

import json, random, string, argparse
from datetime import datetime, timezone
from pathlib import Path

NAME = "(Facebook) Post Reels"
AUTHOR = "GemLogin Team"
DESC = "Built by GemLogin Team: JACOB (CEO) | GEMMY (Automation Lead) | ARKA (Workflow Creator) | LUMI (Workflow Analyst) | HEIMDALL (QA Engineer) | JIMMY (COO)"

def gid(k=7):     return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))
def cid():        return ''.join(random.choices(string.ascii_letters + string.digits + "_-", k=21))
def iid():        return ''.join(random.choices(string.ascii_letters + string.digits + "_-", k=21))
def pid():        return ''.join(random.choices(string.ascii_letters + string.digits, k=4))

# ══════════════════════════════════════════════════════════════════════
#  NODES
# ══════════════════════════════════════════════════════════════════════

def nd(nid, typ, lbl, px, py, **data):
    return {"id":nid,"type":typ,"label":lbl,"initialized":False,
            "position":{"x":px,"y":py},"data":{"disableBlock":False,"description":"",**data}}

def T(nid,x,y,p):  return nd(nid,"BlockBasic","trigger",x,y,icon="riPlayLine",type="manual",interval=60,delay=5,date="",time="00:00",url="",shortcut="",activeInInput=False,isUrlRegex=False,days=[],contextMenuName="",contextTypes=[],parameters=p,preferParamsInTab=False,observeElement=False)
def E(nid,x,y):    return nd(nid,"BlockBasic","end",x,y,icon="riStopCircleLine")
def N(nid,x,y,t,c="green"): return nd(nid,"BlockNote","note",x,y,icon="riStickyNoteLine",note=t,drawing=False,width=1032,height=246,color=c,fontSize="large")
def JS(nid,x,y,d,c): return nd(nid,"BlockBasicWithFallback","javascript-code",x,y,icon="riCodeBoxLine",description=d,code=c,assignVariable=True,variableName="",delay=200,timeout=15000)
def CL(nid,px,py,d,s,w=15000,dl=1500):
    n = nd(nid,"BlockBasicWithFallback","event-click",px,py,icon="riCursorLine",description=d,
           findBy="xpath",waitForSelector=True,waitSelectorTimeout=w,selector=s,
           markEl=False,multiple=False,selectOption="leftClick",delay=dl,humanClick=True)
    n["data"]["x"] = ""; n["data"]["y"] = ""
    return n
def OU(nid,x,y,d,u): return nd(nid,"BlockBasicWithFallback","open-url",x,y,icon="riLink",description=d,url=u,userAgent="",waitTabLoaded=False,waitForNavigation="domcontentloaded",customUserAgent=False,newTab=False,active=True,delay="5000")
def TL(nid,x,y,d):   return nd(nid,"BlockBasicWithFallback","tab-loaded",x,y,icon="riCheckLine",description=d,delay=200,timeout=30000)
def DL(nid,x,y,d,ms=3000): return nd(nid,"BlockBasicWithFallback","delay",x,y,icon="riTimerLine",description=d,delay=ms)
def CN(nid,x,y,d,cs): return nd(nid,"BlockConditions","conditions",x,y,icon="riAB",description=d,conditions=cs,retryConditions=False,retryCount=10,retryTimeout=1000,delay=0)
def UP(nid,x,y,d,s,fv): return nd(nid,"BlockBasicWithFallback","upload-file",x,y,icon="riUploadLine",description=d,findBy="xpath",selector=s,filePath=fv,waitForSelector=True,waitSelectorTimeout=30000,delay=200)
def FM(nid,x,y,d,s,v):  return nd(nid,"BlockBasicWithFallback","forms",x,y,icon="riInputField",description=d,findBy="xpath",selector=s,value=v,fieldType="text",clearBefore=True,waitForSelector=True,waitSelectorTimeout=15000,delay=500)
def EX(nid,x,y,d,s,vn): return nd(nid,"BlockBasicWithFallback","element-exists",x,y,icon="riCheckboxCircleLine",description=d,findBy="xpath",selector=s,waitForSelector=True,waitSelectorTimeout=10000,delay=200,assignVariable=True,variableName=vn)
def FA(nid,x,y,d,fp,id_): return nd(nid,"BlockBasicWithFallback","file-action",x,y,icon="riFileTextLine",description=d,action="Write",filePath=fp,inputData=id_,delimiter="",selectorType="txt",writeMode="append",appendMode="newLine",deleteFileFolder="",delay=0)
def RT(nid,x,y,d):   return nd(nid,"BlockBasicWithFallback","reload-tab",x,y,icon="riRefreshLine",description=d,delay=200)
def LP(nid,x,y,d,lid,to="10000"): return nd(nid,"BlockBasicWithFallback","loop-data",x,y,icon="riRefreshLine",description=d,loopId=lid,maxLoop=0,toNumber=to,fromNumber=1,startIndex=0,loopData="[]",variableName="",referenceKey="",reverseLoop=False,elementSelector="",waitForSelector=False,waitSelectorTimeout=5000,resumeLastWorkflow=False,loopThrough="numbers",delay=0)
def LB(nid,x,y,lid): return nd(nid,"BlockLoopBreakpoint","loop-breakpoint",x,y,icon="riStopLine",loopId=lid,clearLoop=False)
def GF(nid,x,y,d,vn): return nd(nid,"BlockBasicWithFallback","get-file-path",x,y,icon="riFolderLine",description=d,assignVariable=True,variableName=vn,delay=200)
def RF(nid,x,y,d,p,vn=""): return nd(nid,"BlockBasicWithFallback","read-file-text",x,y,icon="riFileTextLine",description=d,path=p,delimiter="",assignVariable=True,variableName=vn,randomEnable=True,deleteLine=True,mode="aline",delay=0)
def PK(nid,x,y,d,k="Enter"): return nd(nid,"BlockBasicWithFallback","press-key",x,y,icon="riKeyboardLine",description=d,key=k,delay=500)
def RG(nid,x,y,d,vn,pat,rep=""): return nd(nid,"BlockBasicWithFallback","regex-variable",x,y,icon="riCodeLine",description=d,variableName=vn,regexPattern=pat,replacement=rep,delay=200)
def ID(nid,x,y,d,dl_): return nd(nid,"BlockBasicWithFallback","insert-data",x,y,icon="riDatabase2Line",description=d,dataList=dl_,delay=0,block="insertData",blockId=gid(7))

# ══════════════════════════════════════════════════════════════════════
#  EDGE
# ══════════════════════════════════════════════════════════════════════

def edge(src,tgt,handle=None,label=""):
    return {"id":f"vueflow__edge-{src}-{tgt}-{gid(7)}","type":"bezier",
            "source":src,"target":tgt,
            "sourceHandle":handle or f"{src}-output-1",
            "targetHandle":f"{tgt}-input-1",
            "updatable":True,"selectable":True,"data":{},
            "label":label,"markerEnd":"arrowclosed",
            "sourceX":0,"sourceY":0,"targetX":0,"targetY":0}

# ══════════════════════════════════════════════════════════════════════
#  CONDITION — ALL items have id (ตรงตาม reference)
# ══════════════════════════════════════════════════════════════════════

class Cond:
    """Track condition ID for edge handles."""
    def __init__(self, name, var, op, val):
        self.id = cid()
        self.name = name
        self.var = var
        self.op = op
        self.val = val
    def build(self):
        return {"id":self.id,"name":self.name,"conditions":[{
            "id":f"group-{self.id}","conditions":[{"id":f"rule-{self.id}","items":[
                {"type":"value","category":"value","data":{"value":f"{{{{variables.{self.var}}}}}"},"id":iid()},
                {"category":"compare","type":self.op,"id":iid()},
                {"type":"value","category":"value","data":{"value":self.val},"id":iid()},
            ]}]}]}

# ══════════════════════════════════════════════════════════════════════
#  PARAMS
# ══════════════════════════════════════════════════════════════════════

def D(label):     return {"id":pid(),"name":"","label":label,"type":"divider","description":"","defaultValue":"","placeholder":"","data":{"thickness":1,"marginTop":8,"marginBottom":8,"label":label}}
def L(text):      return {"id":pid(),"name":"","label":text,"type":"label","description":"","defaultValue":"","placeholder":"","data":{"text":text,"variant":"info"}}
def PN(name,label,desc="",default=""): return {"id":pid(),"name":name,"label":label,"type":"number","description":desc,"defaultValue":default,"placeholder":"","data":{"required":False,"min":1,"max":9999,"step":1}}
def PF(name,label,desc="",ph=""): return {"id":pid(),"name":name,"label":label,"type":"filepath","description":desc,"defaultValue":"","placeholder":ph,"data":{"required":True}}
def PS(name,label,desc="",ph=""): return {"id":pid(),"name":name,"label":label,"type":"string","description":desc,"defaultValue":"","placeholder":ph,"data":{"required":False}}
def PC(name,label,desc="",default=False): return {"id":pid(),"name":name,"label":label,"type":"checkbox","description":desc,"defaultValue":default,"placeholder":"","data":{"required":False}}

# ══════════════════════════════════════════════════════════════════════
#  BUILD
# ══════════════════════════════════════════════════════════════════════

def build():
    # ── All node IDs ──
    K = {}
    for k in ["trigger","loop_data","loop_break",
              "open_reels","wait_reels",
              "cond_cap","read_cap_video","read_cap_file",
              "click_create_post","press_caption",
              "cond_media","get_media_folder","upload_folder","upload_custom",
              "click_add_video","click_upload_btn",
              "click_share","wait_publish","check_confirm","cond_confirm","click_confirm",
              "reload_page","wait_reload","js_get_link","cond_link",
              "save_link","end"]:
        K[k] = gid(7)

    loopId = gid(6)

    # ── Conditions (track IDs for edges) ──
    C_cap = Cond("useVideoFilenameAsCaption","useVideoFilenameAsCaption","eq","true")
    C_media_folder = Cond("useMediaFromFolder","useMediaFromFolder","eq","true")
    C_media_custom = Cond("useCustomMedia","useCustomMedia","eq","true")
    C_confirm = Cond("need-confirm","state","eq","confirm")
    C_published = Cond("published","state","eq","published")
    C_link_found = Cond("link-found","found","eq","yes")
    C_link_missing = Cond("link-missing","found","eq","no")

    # ── Params ──
    P = [
        D("Post Reels"),
        PN("postCount","Post Count","Number of Reels to post","1"),
        D("Caption"),
        PC("useVideoFilenameAsCaption","Use Video Filename as Caption","Auto-use video filename as caption",True),
        PF("captionFolderPath","Caption Folder","Folder containing .txt files","D:\\captions\\"),
        D("Media Source"),
        L("Please select only one option"),
        PC("useMediaFromFolder","Use Media from Folder","Pick random video from folder",True),
        PS("mediaFolderPath","Media Folder","Folder containing video files","D:\\videos\\"),
        PC("useCustomMedia","Use Custom Media","Use a specific video file",False),
        PS("customMediaPath","Custom Media Path","Path to video file","D:\\video.mp4"),
        D("Output"),
        PF("output_link_path","Output Link File","Save posted Reel permalinks","D:\\output\\links.txt"),
    ]

    nodes, edges = [], []

    def A(src_key,tgt_key,handle=None,label=""):
        edges.append(edge(K[src_key],K[tgt_key],handle,label))

    # ═══ LAYOUT — grid spacing: 280px horizontal, 120px vertical ═══
    # Notes sit 440px left of their section

    def X(c): return c * 280
    def Y(r): return r * 120
    NX = -440  # note X offset from section

    # ROW MAP:
    # r0: trigger, loop
    # r1: open_reels, wait_reels
    # r2: cond_cap, read_cap*, click_create_post
    # r3: press_caption, cond_media
    # r4: get_media_folder, upload_folder, upload_custom
    # r5: click_add_video, click_upload_btn
    # r6: click_share, wait_publish
    # r7: check_confirm, cond_confirm, click_confirm
    # r8: reload_page, wait_reload
    # r9: js_get_link, cond_link, save_link
    # r10: loop_break, end

    # TRIGGER + LOOP (col 0-1, row 0)
    nodes.append(T(K["trigger"],X(0),Y(0),P))
    nodes.append(LP(K["loop_data"],X(1),Y(0),f"Loop {P[1]['name']}",loopId,"{{variables.postCount}}"))

    # NAVIGATE (col 1-2, row 1)
    nodes.append(OU(K["open_reels"],X(1),Y(1),"Open Reels creator","https://www.facebook.com/reels/create/"))
    nodes.append(TL(K["wait_reels"],X(2),Y(1),"Wait for Reels creator"))

    # CAPTION SOURCE (col 2-3, rows 2-3)
    nodes.append(CN(K["cond_cap"],X(2),Y(2),"",[C_cap.build()]))
    nodes.append(RF(K["read_cap_video"],X(3),Y(2),"Read video filename as caption","{{variables.mediaFile}}","caption"))
    nodes.append(RF(K["read_cap_file"],X(3),Y(3),"Read caption from file","{{variables.captionFolderPath}}","caption"))

    # COMPOSER (col 3-4, rows 3-4)
    nodes.append(CL(K["click_create_post"],X(3),Y(4),"Click Add video (VERIFIED)","//*[contains(text(),'Add video')]",w=10000,dl=2000))
    nodes.append(PK(K["press_caption"],X(4),Y(4),"Type caption","{{variables.caption}}"))

    # MEDIA SOURCE (col 4-5, rows 2-4)
    nodes.append(CN(K["cond_media"],X(4),Y(2),"",[C_media_folder.build(),C_media_custom.build()]))
    nodes.append(GF(K["get_media_folder"],X(5),Y(2),"Get random media from folder","mediaFile"))
    nodes.append(UP(K["upload_folder"],X(5),Y(3),"Upload from folder","//input[@type='file' and contains(@accept,'video')]","{{variables.mediaFile}}"))
    nodes.append(UP(K["upload_custom"],X(5),Y(4),"Upload custom media","//input[@type='file' and contains(@accept,'video')]","{{variables.customMediaPath}}"))

    # UPLOAD BUTTONS (col 6, rows 3-4)
    nodes.append(CL(K["click_add_video"],X(6),Y(3),"Click Add video","//*[contains(text(),'Add video')]",w=10000,dl=2000))
    nodes.append(CL(K["click_upload_btn"],X(6),Y(4),"Click Upload video for Reel","//div[@role='button' and @aria-label='Upload video for Reel']",w=10000,dl=2000))

    # SHARE + PUBLISH (col 7, rows 3-5)
    nodes.append(CL(K["click_share"],X(7),Y(3),"Click Share (VERIFIED)","//div[@role='button' and @aria-label='Share']",w=15000,dl=3000))
    nodes.append(DL(K["wait_publish"],X(7),Y(4),"Wait for publish",20000))

    # CONFIRMATION (col 7-8, rows 5-6)
    nodes.append(JS(K["check_confirm"],X(7),Y(5),"Detect confirmation","const c=document.querySelector('[aria-label=\"Share now\"]');return{state:c?'confirm':'published'};"))
    nodes.append(CN(K["cond_confirm"],X(8),Y(5),"",[C_confirm.build(),C_published.build()]))
    nodes.append(CL(K["click_confirm"],X(8),Y(6),"Click Share now","//div[@role='button' and @aria-label='Share now']",w=10000,dl=2000))

    # COLLECT LINK (col 9, rows 5-7)
    nodes.append(RT(K["reload_page"],X(9),Y(5),"Reload for new post"))
    nodes.append(DL(K["wait_reload"],X(9),Y(6),"Wait reload",5000))
    nodes.append(JS(K["js_get_link"],X(9),Y(7),"Get Reel permalink","let u='';if(location.href.includes('/reel/'))u=location.href;if(!u){const l=document.querySelector('a[href*=\"/reel/\"]');if(l)u='https://www.facebook.com'+l.getAttribute('href').split('?')[0]}return{reel_url:u,found:u?'yes':'no'};"))

    # COND LINK + SAVE (col 10, rows 7-8)
    nodes.append(CN(K["cond_link"],X(10),Y(7),"",[C_link_found.build(),C_link_missing.build()]))
    nodes.append(FA(K["save_link"],X(10),Y(8),"Save link","{{variables.output_link_path}}","{{variables.reel_url}}"))

    # LOOP BACK + END (col 11, rows 0, 6)
    nodes.append(LB(K["loop_break"],X(11),Y(0),loopId))
    nodes.append(E(K["end"],X(12),Y(0)))

    # ═══════════════════════════════════════════════════════════════
    # EDGES
    # ═══════════════════════════════════════════════════════════════

    # Trigger → Loop → Nav
    A("trigger","loop_data",label="Start")
    A("loop_data","open_reels",label="Post Reel")

    # Nav
    A("open_reels","wait_reels",label="Page loaded")
    A("wait_reels","cond_cap",label="Caption?")

    # Caption source → composer
    A("cond_cap","read_cap_video",f"{K['cond_cap']}-output-{C_cap.id}",label="Use filename")
    A("cond_cap","read_cap_file",f"{K['cond_cap']}-output-fallback",label="Use file")
    A("read_cap_video","click_create_post",label="Caption ready")
    A("read_cap_file","click_create_post",label="Caption ready")
    A("click_create_post","press_caption",label="Type")

    # Media source
    A("press_caption","cond_media",label="Media?")
    A("cond_media","get_media_folder",f"{K['cond_media']}-output-{C_media_folder.id}",label="Folder")
    A("cond_media","upload_custom",f"{K['cond_media']}-output-{C_media_custom.id}",label="Custom")
    A("get_media_folder","upload_folder",label="Upload folder")
    A("upload_folder","click_add_video",label="→ Upload flow")
    A("upload_custom","click_add_video",label="→ Upload flow")

    # Upload buttons
    A("click_add_video","click_upload_btn",label="Upload btn")
    A("click_upload_btn","click_share",label="→ Share")

    # Share → Confirm
    A("click_share","wait_publish",label="Publishing...")
    A("wait_publish","check_confirm",label="Check")
    A("check_confirm","cond_confirm",label="Route")
    A("cond_confirm","reload_page",f"{K['cond_confirm']}-output-{C_published.id}",label="Published")
    A("cond_confirm","click_confirm",f"{K['cond_confirm']}-output-{C_confirm.id}",label="Confirm needed")
    A("click_confirm","reload_page",label="→ Collect")

    # Collect → Save
    A("reload_page","wait_reload",label="Reloaded")
    A("wait_reload","js_get_link",label="Find link")
    A("js_get_link","cond_link",label="Route")
    A("cond_link","save_link",f"{K['cond_link']}-output-{C_link_found.id}",label="Found")
    A("cond_link","loop_break",f"{K['cond_link']}-output-{C_link_missing.id}",label="Not found")

    # Save → Loop back
    A("save_link","loop_break",label="Done ✓")

    # Loop break → back to loop for next iteration
    A("loop_break","loop_data",f"{K['loop_break']}-output-1",label="Next")
    # Loop complete → end (fallback from loop_data when postCount reached)
    A("loop_data","end",f"{K['loop_data']}-output-fallback",label="Done all")

    # ── Assemble ──
    return {
        "extVersion":2,"name":NAME,"icon":"riGlobalLine","table":[],"version":"1.0.0",
        "drawflow":{"nodes":nodes,"edges":edges},
        "settings":{"publicId":"","blockDelay":0,"saveLog":True,"debugMode":False,
                    "restartTimes":3,"notification":True,"execContext":"popup",
                    "reuseLastState":False,"inputAutocomplete":True,"onError":"stop-workflow",
                    "executedBlockOnWeb":False,"insertDefaultColumn":False,"defaultColumnName":"column"},
        "globalData":"","description":DESC,
        "trigger":{"icon":"riPlayLine","disableBlock":False,"description":"",
                   "type":"manual","interval":60,"delay":5,"date":"","time":"00:00","url":"","shortcut":"",
                   "activeInInput":False,"isUrlRegex":False,"days":[],"contextMenuName":"","contextTypes":[],
                   "parameters":P,"preferParamsInTab":False,"observeElement":False},
        "isProtected":False,"includedWorkflows":{},"author":AUTHOR}

# ══════════════════════════════════════════════════════════════════════
#  CLI
# ══════════════════════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(description=f"GemLogin: {NAME}")
    p.add_argument("-o","--output-dir",default=".",help="โฟลเดอร์ปลายทาง")
    p.add_argument("--dry-run",action="store_true")
    p.add_argument("--summary",action="store_true")
    a = p.parse_args()

    print(f"[generate] {NAME}")
    wf = build()
    nc,ec,pc = len(wf["drawflow"]["nodes"]),len(wf["drawflow"]["edges"]),len(wf["trigger"]["parameters"])
    print(f"  Nodes:{nc}  Edges:{ec}  Params:{pc}")

    if a.summary:
        for n in wf["drawflow"]["nodes"]:
            d = n['data'].get('description','') or n['data'].get('note','')
            if d: print(f"  [{n['type'][-15:]:15s}] {d[:80]}")

    if a.dry_run: return

    out = Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    fp = out / f"{NAME.replace(' ','_').replace('(','').replace(')','')}.gemlogin"
    with open(fp,"w",encoding="utf-8") as f:
        json.dump(wf,f,ensure_ascii=False,indent=2)
    print(f"  Saved: {fp} ({fp.stat().st_size/1024:.1f} KB)")

if __name__=="__main__":
    main()
