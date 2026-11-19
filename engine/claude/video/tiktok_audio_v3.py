import json, numpy as np, soundfile as sf
from scipy import signal
SR=48000; rng=np.random.default_rng(7)
J=json.load(open('tim.json')); TIM=J['TIM']; total=J['total']; off=J['off']; IDS=['hook','monday','overnight','verdict','outro']
N=int(total*SR)+SR
def env(n,a,d):
    e=np.ones(n); A=int(a*SR); 
    if A: e[:A]=np.linspace(0,1,A)
    e*=np.exp(-np.arange(n)/(d*SR)); return e
def lp(x,f,o=2): b,a=signal.butter(o,f/(SR/2),'low'); return signal.lfilter(b,a,x)
def hp(x,f,o=2): b,a=signal.butter(o,f/(SR/2),'high'); return signal.lfilter(b,a,x)
def bp(x,lo,hi): b,a=signal.butter(2,[lo/(SR/2),hi/(SR/2)],'band'); return signal.lfilter(b,a,x)
t_=lambda d: np.arange(int(d*SR))/SR
# --- SFX
def whoosh(d=0.6):
    n=int(d*SR); x=rng.standard_normal(n); out=np.zeros(n); seg=512
    for i in range(0,n,seg):
        f=300+5000*np.sin(np.pi*i/n)**2; out[i:i+seg]=bp(x[i:i+seg],max(100,f*0.5),min(SR/2-100,f*1.5))[:len(out[i:i+seg])]
    return out*np.sin(np.pi*np.arange(n)/n)**1.5*0.5
def impact():
    t=t_(1.2); boom=np.sin(2*np.pi*(55*t+40*np.exp(-t*12)/12*0)+0)*np.exp(-t*3.5)
    sub=np.sin(2*np.pi*np.cumsum(45+120*np.exp(-t*20))/SR)*np.exp(-t*3)
    noise=lp(rng.standard_normal(len(t)),2500)*np.exp(-t*18)
    return (0.9*sub+0.2*boom+0.5*noise)*0.8
def riserhit():
    return impact()
def pop():
    t=t_(0.18); return np.sin(2*np.pi*np.cumsum(900-500*t/0.18)/SR)*np.exp(-t*30)*0.35
def tick():
    t=t_(0.05); return hp(rng.standard_normal(len(t)),3000)*np.exp(-t*120)*0.25
def tick2():
    t=t_(0.03); return np.sin(2*np.pi*2400*t)*np.exp(-t*200)*0.10
def ding():
    t=t_(1.5); return sum(np.sin(2*np.pi*f*t)*np.exp(-t*k)*a for f,k,a in [(1046.5,3,0.25),(1568,4,0.15),(2093,6,0.08)])
def whoosh2(): return whoosh(0.8)*0.8
def hit():
    t=t_(0.5); return (np.sin(2*np.pi*np.cumsum(80+200*np.exp(-t*25))/SR)*np.exp(-t*9)*0.7+hp(rng.standard_normal(len(t)),1500)*np.exp(-t*30)*0.25)
def swish(): return whoosh(0.35)*0.45
def rumble():
    t=t_(1.1); x=lp(rng.standard_normal(len(t)),180,2)*8; return x*np.minimum(1,t/0.9)*np.exp(-np.maximum(0,t-0.95)*25)*0.5
def thud():
    t=t_(0.4); return np.sin(2*np.pi*np.cumsum(60+80*np.exp(-t*30))/SR)*np.exp(-t*10)*0.6
def impact2(): return impact()*0.7
def click():
    t=t_(0.04); return hp(rng.standard_normal(len(t)),2000)*np.exp(-t*150)*0.5
SFX={'hit':hit,'swish':swish,'rumble':rumble,'thud':thud,'impact2':impact2,'click':click,'whoosh':lambda:whoosh(0.6),'impact':impact,'riserhit':riserhit,'pop':pop,'tick':tick,'tick2':tick2,'ding':ding,'whoosh2':whoosh2}
fx=np.zeros(N)
for c in json.load(open('cues.json')):
    s=SFX[c['type']](); i=int(max(0,c['t']-(0.15 if c['type'] in('whoosh','whoosh2') else 0))*SR); fx[i:i+len(s)]+=s[:N-i]
# --- Voice
vo=np.zeros(N)
for k,id in enumerate(IDS):
    a,sr=sf.read(f'vo_{id}.wav'); a=signal.resample_poly(a,2,1) if sr==24000 else a
    i=int((off[k]+TIM[id]['lead'])*SR); vo[i:i+len(a)]+=a
# warmth: low shelf-ish boost, gentle high cut
vo=vo+0.35*lp(vo,250); vo=lp(vo,9000,1); vo=hp(vo,70)
# room
ir=np.zeros(int(0.35*SR)); 
for d,g in [(0.021,0.18),(0.033,0.12),(0.047,0.09),(0.071,0.06),(0.11,0.04)]: ir[int(d*SR)]=g
ir[0]=1; vo=signal.fftconvolve(vo,ir)[:N]
vo/=np.max(np.abs(vo))+1e-9
# --- Music: 92 BPM, Am F C G
bpm=112; beat=60/bpm; bar=4*beat
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G (midi)
roots=[45,41,48,43]
mf=lambda m:440*2**((m-69)/12)
mus=np.zeros(N); pad=np.zeros(N); bass=np.zeros(N); drums=np.zeros(N); arp=np.zeros(N)
nb=int(total/bar)+2
for b in range(nb):
    ci=b%4; s0=int(b*bar*SR); L=int(bar*SR); tt=np.arange(L)/SR
    if s0>=N: break
    seg=np.zeros(L)
    for m in chords[ci]:
        for det in (-0.08,0.08):
            f=mf(m+12)*2**(det/12); seg+=signal.sawtooth(2*np.pi*f*tt)*0.05
    e=np.minimum(1,tt/0.6)*np.minimum(1,(bar-tt)/0.3); seg=lp(seg*e,1400)
    pad[s0:s0+L]+=seg[:N-s0]
    # bass on beats 1 and 3 (+&)
    for bt in (0,1.5,2,3.5):
        i=s0+int(bt*beat*SR); l=int(0.5*SR); t2=np.arange(l)/SR
        if i<N: x=np.sin(2*np.pi*mf(roots[ci])*t2)*np.exp(-t2*4)*0.35; bass[i:i+l]+=x[:N-i]
    # drums
    for bt in range(8):
        i=s0+int(bt*beat/2*SR)
        if i>=N: continue
        l=int(0.25*SR); t2=np.arange(l)/SR
        if bt in (0,4,5):  # kick
            k=np.sin(2*np.pi*np.cumsum(50+90*np.exp(-t2*30))/SR)*np.exp(-t2*9)*0.55; drums[i:i+l]+=k[:N-i]
        if bt in (2,6):    # snare/clap soft
            sn=bp(rng.standard_normal(l),1200,5000)*np.exp(-t2*22)*0.22; drums[i:i+l]+=sn[:N-i]
        h=hp(rng.standard_normal(int(0.05*SR)),7000)*np.exp(-np.arange(int(0.05*SR))/SR*90)*0.07; drums[i:i+len(h)]+=h[:N-i]
    # pluck arp 16ths
    notes=chords[ci]+[chords[ci][1]+12]
    for st in range(16):
        i=s0+int(st*beat/4*SR); l=int(0.3*SR); t2=np.arange(l)/SR
        if i>=N: continue
        f=mf(notes[st%4]+12); x=(np.sin(2*np.pi*f*t2)+0.3*np.sin(4*np.pi*f*t2))*np.exp(-t2*14)*0.06
        arp[i:i+l]+=x[:N-i]
mus=pad+bass+drums+lp(arp,4000)
mus/=np.max(np.abs(mus))+1e-9
# intro: drums drop in at the hook impact (start full), fade out last 2.5s
fo=int(2.5*SR); end=int(total*SR); mus[end-fo:end]*=np.linspace(1,0,fo); mus[end:]=0
# ducking under voice
venv=lp(np.abs(vo),8)*6; venv=np.minimum(1,venv); duck=1-0.55*venv
mix=0.95*vo+0.34*mus*duck+0.6*fx
mix=mix[:int(total*SR)]
mix/=np.max(np.abs(mix))/0.89
sf.write('mix.wav',np.stack([mix,mix],1),SR)
print('ok',len(mix)/SR)
