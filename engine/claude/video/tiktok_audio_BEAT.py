import json, numpy as np, soundfile as sf
from scipy import signal
SR=48000; rng=np.random.default_rng(7)
J=json.load(open('tim.json')); TIM=J['TIM']; total=J['total']; off=J['off']; IDS=['hook','q1','r1','r2','outro']
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
def swell():
    t=t_(1.4); x=lp(rng.standard_normal(len(t)),900,2); return x*np.sin(np.pi*np.minimum(1,t/1.4))**2*0.35
SFX={'swell':swell,'hit':hit,'swish':swish,'rumble':rumble,'thud':thud,'impact2':impact2,'click':click,'whoosh':lambda:whoosh(0.6),'impact':impact,'riserhit':riserhit,'pop':pop,'tick':tick,'tick2':tick2,'ding':ding,'whoosh2':whoosh2}
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
# --- Music: catchy original trap/pop beat, 140 BPM half-time, A minor pluck hook, 808, claps, hat rolls
bpm=140; beat=60/bpm; bar=4*beat
mf=lambda m:440*2**((m-69)/12)
mus=np.zeros(N)
def put(x,i):
    if i<N: mus[i:i+len(x)]+=x[:N-i]
def kick():
    t=np.arange(int(0.45*SR))/SR; return np.sin(2*np.pi*np.cumsum(45+160*np.exp(-t*28))/SR)*np.exp(-t*7)*0.9
def b808(f,L):
    t=np.arange(int(L*SR))/SR; x=np.tanh(2.2*np.sin(2*np.pi*f*t))*np.exp(-t*1.8)*np.minimum(1,t/0.005); return x*0.45
def clap():
    t=np.arange(int(0.25*SR))/SR; n=bp(rng.standard_normal(len(t)),900,5000)
    e=sum(np.exp(-np.maximum(0,t-d)*60)*(t>=d) for d in (0,0.012,0.024))*0.6+np.exp(-t*14)*0.5
    return n*e*0.35
def hat(o=False):
    L=int((0.12 if o else 0.035)*SR); t=np.arange(L)/SR; return hp(rng.standard_normal(L),7500)*np.exp(-t*(25 if o else 140))*0.12
def pluck(f,L=0.35):
    t=np.arange(int(L*SR))/SR; x=sum(np.sin(2*np.pi*f*h*t)/h for h in (1,2,3,4))*np.exp(-t*9)
    return lp(x,4200)*0.16
# chords Am F C G (roots)
roots=[45,41,48,43]
# 2-bar catchy hook (16ths index, midi)
hook=[(0,69),(3,72),(6,76),(8,74),(10,72),(12,69),(14,67),(16,69),(19,72),(22,76),(24,79),(26,76),(28,74),(30,72)]
nb=int(total/bar)+2
for b in range(nb):
    s0=int(b*bar*SR); r=roots[b%4]; s16=beat/4
    if s0>=N: break
    for st in (0,10,11) if b%2==0 else (0,6,10):
        put(kick(),s0+int(st*s16*SR))
    put(b808(mf(r-12),bar*0.95),s0)
    put(clap(),s0+int(2*beat*SR))
    for k in range(8):
        put(hat(o=(k==7)),s0+int(k*beat/2*SR))
    if b%2==1:
        for k in range(6): put(hat()*0.8,s0+int((3*beat+k*beat/6)*SR))
    for st,m in hook:
        if (b%2)*16<=st<(b%2+1)*16:
            put(pluck(mf(m)),s0+int((st-(b%2)*16)*s16*SR))
    # soft pad
    L=int(bar*SR); t=np.arange(L)/SR
    pad=sum(np.sin(2*np.pi*mf(r+12+iv)*t) for iv in (0,3,7))*0.02*np.minimum(1,t/0.3)*np.minimum(1,(bar-t)/0.3)
    put(pad,s0)
mus=lp(mus,9000,1); mus/=np.max(np.abs(mus))+1e-9

# intro: drums drop in at the hook impact (start full), fade out last 2.5s
fo=int(0.5*SR); end=int(total*SR); mus[end-fo:end]*=np.linspace(1,0,fo); mus[end:]=0
# ducking under voice
venv=lp(np.abs(vo),8)*6; venv=np.minimum(1,venv); duck=1-0.55*venv
mix=0.95*vo+0.34*mus*duck+0.45*fx
mix=mix[:int(total*SR)]
mix/=np.max(np.abs(mix))/0.89
sf.write('mix_beat.wav',np.stack([mix,mix],1),SR)
print('ok',len(mix)/SR)
