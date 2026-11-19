"""Own simplified AN60 sample/hold sensitivity model. Not manufacturer silicon model. See electrical-checks.json limitations."""
import math
def screen(vout=110.0, R=33.2, L=0.003, vac=230.0, f=66000.0, ilim=0.375, vth=1.65, C=2.2e-05, tmin=5e-07, duration=0.4):
    T = 1 / f
    tau = R * C
    cf = 0.0
    i = 0.0
    q = qin = q2 = 0.0
    pk = 0.0
    nstart = int(duration * f / 2)
    count = int(duration * f)
    for n in range(count):
        vin = max(0, math.sqrt(2) * vac * abs(math.sin(2 * math.pi * 50 * n * T)) - 1.6)
        ton = qa = qa2 = 0.0
        if cf < vth and vin > vout:
            a = (vin - vout) / L
            ton = min(0.69 * T, max(tmin, (ilim - i) / a))
            j = i + a * ton
            qa = (i + j) * ton / 2
            qa2 = (i * i + i * j + j * j) * ton / 3
            i = j
            cf *= math.exp(-ton / tau)
        a = (vout + 1 + max(cf, 0)) / L
        tf = min(T - ton, i / a)
        j = max(0, i - a * tf)
        qb = (i + j) * tf / 2
        qb2 = (i * i + i * j + j * j) * tf / 3
        cf = (cf - R * i - R * a * tau) * math.exp(-tf / tau) + R * (i - a * tf + a * tau)
        cf *= math.exp(-(T - ton - tf) / tau)
        if n >= nstart:
            q += qa + qb
            qin += qa
            q2 += qa2 + qb2
            pk = max(pk, i)
        i = j
    dur = (count - nstart) * T
    return dict(Iout=q / dur, Iinavg=qin / dur, ILrms=math.sqrt(q2 / dur), Ipeak=pk)
