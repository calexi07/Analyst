import numpy as np, soundfile as sf
from scipy import signal
SR=48000; D=7.2; N=int(D*SR); rng=np.random.default_rng(3); t=np.arange(N)/SR
def lp(x,f,o=2): b,a=signal.butter(o,f/(SR/2),'low'); return signal.lfilter(b,a,x)
def hp(x,f,o=2): b,a=signal.butter(o,f/(SR/2),'high'); return signal.lfilter(b,a,x)
out=np.zeros(N); mf=lambda m:440*2**((m-69)/12)
# riser 0-1.25
n=int(1.25*SR); x=rng.standard_normal(n); r=np.zeros(n)
for i in range(0,n,512):
    f=300+6000*(i/n)**2; b,a=signal.butter(2,[max(80,f*0.6)/(SR/2),min(SR/2-100,f*1.4)/(SR/2)],'band'); r[i:i+512]=signal.lfilter(b,a,x[i:i+512])[:len(r[i:i+512])]
r*= (np.arange(n)/n)**2*0.6; out[:n]+=r
# impact at 1.3
i0=int(1.3*SR); tt=np.arange(int(1.6*SR))/SR
imp=np.sin(2*np.pi*np.cumsum(42+140*np.exp(-tt*18))/SR)*np.exp(-tt*2.8)*0.9+lp(rng.standard_normal(len(tt)),3000)*np.exp(-tt*14)*0.35
out[i0:i0+len(imp)]+=imp[:N-i0]
# warm chord pad from 1.3 (Fmaj9: F A C E G)
pad=np.zeros(N)
for m in [53,57,60,64,67]:
    for det in (-0.07,0.07):
        f=mf(m)*2**(det/12); pad+=signal.sawtooth(2*np.pi*f*t)*0.04
env=np.clip((t-1.3)/0.8,0,1)*np.clip((D-t)/1.2,0,1); out+=lp(pad*env,1800)
# e-piano plucks (arpeggio) from 2.3
def ep(f,L):
    tt=np.arange(L)/SR; return np.sin(2*np.pi*f*tt+1.1*np.sin(2*np.pi*f*tt)*np.exp(-tt*3))*np.exp(-tt*2.2)
for k,(m,tm) in enumerate([(72,2.3),(76,2.55),(79,2.8),(84,3.05),(83,3.6),(79,4.1)]):
    i=int(tm*SR); L=int(1.8*SR); x=ep(mf(m),L)*0.13; out[i:i+L]+=x[:N-i]
# shimmer at sweep 4.2
i=int(4.2*SR); L=int(2*SR); tt=np.arange(L)/SR; sh=sum(np.sin(2*np.pi*f*tt)*np.exp(-tt*k) for f,k in [(2093,3),(3136,4),(4186,5)])*0.05; out[i:i+L]+=sh[:N-i]
# soft sub pulse
for tm in (1.3,3.0,4.7):
    i=int(tm*SR); tt=np.arange(int(0.5*SR))/SR; k=np.sin(2*np.pi*np.cumsum(45+60*np.exp(-tt*25))/SR)*np.exp(-tt*7)*0.35; out[i:i+len(k)]+=k[:N-i]
# reverb-ish
ir=np.zeros(int(1.2*SR)); ir[0]=1
for d in range(1,40): ir[int(d*0.028*SR)]=0.55*np.exp(-d/9)*(1 if d%2 else -1)
out=signal.fftconvolve(out,lp(ir,6000))[:N]
out*=np.clip(t/0.05,0,1)*np.clip((D-t)/0.6,0,1)
out/=np.max(np.abs(out))/0.85
sf.write('intro.wav',np.stack([out,out*0.98],1),SR); print('ok')
