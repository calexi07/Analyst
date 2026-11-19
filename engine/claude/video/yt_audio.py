import json, numpy as np, soundfile as sf
from scipy import signal
SR=48000; rng=np.random.default_rng(7)
J=json.load(open('tim.json')); TIM=J['TIM']; total=J['total']; off=J['off']; IDS=J['IDS']
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
SFX['swish']=swish
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
# --- Music: lo-fi electric piano, 74 BPM, Dm9 G13 Cmaj9 Am9, swung brushes, vinyl
bpm=74; beat=60/bpm; bar=4*beat
chords=[[50,53,57,60,64],[43,53,57,59,64],[48,52,55,59,62],[45,52,55,60,59+12]]
roots=[38,31,36,33]
mf=lambda m:440*2**((m-69)/12)
ep=np.zeros(N); bass=np.zeros(N); drums=np.zeros(N); bell=np.zeros(N)
nb=int(total/bar)+2
def epiano(f,L):
    t=np.arange(L)/SR; mod=np.sin(2*np.pi*f*t)*1.2*np.exp(-t*3)
    x=np.sin(2*np.pi*f*t+mod)*np.exp(-t*1.6)+0.25*np.sin(4*np.pi*f*t)*np.exp(-t*4)
    return x*(1+0.12*np.sin(2*np.pi*4.5*t))
for b in range(nb):
    ci=b%4; s0=int(b*bar*SR)
    if s0>=N: break
    for hit,(bt,vel) in enumerate([(0,1.0),(2.5,0.6)]):
        i=s0+int(bt*beat*SR); L=int(2.2*SR)
        if i>=N: continue
        x=sum(epiano(mf(m),L)*(0.9 if k else 0.6) for k,m in enumerate(chords[ci]))*0.05*vel
        for k in range(len(chords[ci])):
            pass
        ep[i:i+L]+=x[:N-i]
    for bt,l in ((0,1.4),(1.5,0.5),(2,1.2),(3.5,0.4)):
        i=s0+int(bt*beat*SR); L=int(l*SR); t2=np.arange(L)/SR
        if i<N:
            x=(np.sin(2*np.pi*mf(roots[ci])*t2)+0.15*np.sin(4*np.pi*mf(roots[ci])*t2))*np.minimum(1,t2/0.01)*np.exp(-t2*2.2)*0.32
            bass[i:i+L]+=x[:N-i]
    sw=0.62
    for e8 in range(8):
        pos=(e8//2)*beat+(0 if e8%2==0 else sw*beat); i=s0+int(pos*SR)
        if i>=N: continue
        l=int(0.3*SR); t2=np.arange(l)/SR
        if e8 in (0,5):
            k=np.sin(2*np.pi*np.cumsum(48+70*np.exp(-t2*35))/SR)*np.exp(-t2*8)*0.38; drums[i:i+l]+=k[:N-i]
        if e8 in (2,6):
            sn=lp(bp(rng.standard_normal(l),900,4000),3500)*np.exp(-t2*14)*0.16; drums[i:i+l]+=sn[:N-i]
        hl=int(0.06*SR); h=hp(rng.standard_normal(hl),6000)*np.exp(-np.arange(hl)/SR*60)*(0.05 if e8%2 else 0.08); drums[i:i+hl]+=h[:N-i]
    if b%2==1:
        mel=[chords[ci][-1]+12,chords[ci][-2]+12,chords[ci][2]+12]
        for n,(bt) in enumerate((1,1.75,3)):
            i=s0+int(bt*beat*SR); L=int(1.2*SR); t2=np.arange(L)/SR
            if i<N:
                f=mf(mel[n]); x=(np.sin(2*np.pi*f*t2)+0.4*np.sin(2*np.pi*f*3.01*t2)*np.exp(-t2*6))*np.exp(-t2*3)*0.05
                bell[i:i+L]+=x[:N-i]
ep=lp(ep,3200)
crack=np.zeros(N); idx=rng.integers(0,N,int(total*25)); crack[idx]=rng.uniform(-1,1,len(idx))*0.25
crack=hp(crack,1500)+lp(rng.standard_normal(N),400)*0.004
mus=ep+bass+drums+bell+crack*0.6
mus=lp(mus,7000,1)
mus/=np.max(np.abs(mus))+1e-9
# intro: drums drop in at the hook impact (start full), fade out last 2.5s
fo=int(2.5*SR); end=int(total*SR); mus[end-fo:end]*=np.linspace(1,0,fo); mus[end:]=0
# ducking under voice
venv=lp(np.abs(vo),8)*6; venv=np.minimum(1,venv); duck=1-0.55*venv
mix=0.95*vo+0.26*mus*duck+0.38*fx
mix=mix[:int(total*SR)]
mix/=np.max(np.abs(mix))/0.89
sf.write('mix.wav',np.stack([mix,mix],1),SR)
print('ok',len(mix)/SR)
