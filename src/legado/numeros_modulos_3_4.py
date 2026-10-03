"""Numeros usados nos modulos 3 (probabilidade) e 4 (amostragem) do material de aula. Semente fixa."""
import os
import duckdb, numpy as np
from scipy import stats
con = duckdb.connect()
P = os.environ.get("MQ_DADOS", "dados").replace("\\", "/") + "/enem2023.parquet"
rng = np.random.default_rng(2023)

d = con.sql(f"select NU_NOTA_CN cn, NU_NOTA_CH ch, NU_NOTA_LC lc, NU_NOTA_MT mt, NU_NOTA_REDACAO red from '{P}' where TP_PRESENCA_CN=1 and TP_PRESENCA_CH=1 and TP_PRESENCA_LC=1 and TP_PRESENCA_MT=1 and NU_NOTA_REDACAO is not null").df()
print("n com 4 provas + redacao:", len(d))
for c in d.columns:
    x = d[c].to_numpy(); m, s = x.mean(), x.std(ddof=0)
    z = (x - m) / s
    print(f"{c}: media={m:.1f} dp={s:.1f} assimetria={stats.skew(x):.2f} curtose_excesso={stats.kurtosis(x):.2f} "
          f"|z|<1:{(abs(z)<1).mean()*100:.1f}% <2:{(abs(z)<2).mean()*100:.1f}% <3:{(abs(z)<3).mean()*100:.1f}%")

mt = con.sql(f"select NU_NOTA_MT from '{P}' where TP_PRESENCA_MT=1").df()["NU_NOTA_MT"].to_numpy()
mu, sig = mt.mean(), mt.std(ddof=0)
print(f"\nMT presentes: N={len(mt)} mu={mu:.2f} sigma={sig:.2f} mediana={np.median(mt):.1f}")
for lim in (600, 700, 800):
    print(f"P(MT>{lim}) empirico={(mt>lim).mean()*100:.2f}%  normal={(1-stats.norm.cdf(lim, mu, sig))*100:.2f}%")
print("percentis 1,5,25,50,75,95,99:", np.percentile(mt, [1,5,25,50,75,95,99]).round(1))

print("\nTCL: medias de amostras de MT (5000 amostras)")
for n in (2, 5, 30, 100, 400):
    means = np.array([rng.choice(mt, n).mean() for _ in range(5000)])
    print(f"n={n}: media das medias={means.mean():.2f} dp das medias={means.std(ddof=1):.2f} (teorico sigma/raiz(n)={sig/np.sqrt(n):.2f}) assimetria={stats.skew(means):.2f}")

print("\nCobertura do IC95% (z, 1000 amostras)")
for n in (30, 100, 400, 1600):
    cov = 0; larg = []
    for _ in range(1000):
        a = rng.choice(mt, n); se = a.std(ddof=1)/np.sqrt(n); lo, hi = a.mean()-1.96*se, a.mean()+1.96*se
        cov += lo <= mu <= hi; larg.append(hi-lo)
    print(f"n={n}: cobertura={cov/10:.1f}% largura media={np.mean(larg):.1f}")

print("\nTamanho de amostra p/ media de MT, erro +-5 pontos, 95%, sigma amostral:", int(np.ceil((1.96*mt.std(ddof=1)/5)**2)))
print("... erro +-10:", int(np.ceil((1.96*mt.std(ddof=1)/10)**2)))

print("\nConveniencia x aleatoria (n=400, 1000 reps)")
q = con.sql(f"select SG_UF_PROVA uf, NU_NOTA_MT mt from '{P}' where TP_PRESENCA_MT=1").df()
df_ = q[q.uf=='DF'].mt.to_numpy()
print(f"media DF={df_.mean():.1f} vs Brasil={mu:.1f}; n_DF={len(df_)}")
est = [rng.choice(df_, 400).mean() for _ in range(1000)]
print(f"amostras so do DF: media das estimativas={np.mean(est):.1f} (vies={np.mean(est)-mu:+.1f})")
print("\nMT media por UF (top e base):")
t = q.groupby('uf').mt.agg(['count','mean']).sort_values('mean'); print(t.head(3).round(1).to_string()); print(t.tail(3).round(1).to_string())

print("\nPresenca em MT por faixa de renda Q006 (todos os inscritos)")
r = con.sql(f"select Q006, count(*) n, round(100.0*avg((TP_PRESENCA_MT=1)::int),1) pct_presente from '{P}' group by 1 order by 1").df()
print(r.to_string(index=False))

print("\nBinomial: P(>=8 presentes em 10 inscritos), p=presenca geral")
pp = con.sql(f"select avg((TP_PRESENCA_MT=1)::int) from '{P}'").fetchone()[0]
print(f"p={pp:.4f}  P(X>=8)={1-stats.binom.cdf(7,10,pp):.4f}  E[X]={10*pp:.2f}")
print(f"chute: n=45 p=0.2: E={45*0.2:.1f} dp={np.sqrt(45*0.2*0.8):.2f} P(X>=15)={1-stats.binom.cdf(14,45,0.2):.4f} P(X>=18)={1-stats.binom.cdf(17,45,0.2):.6f}")

print("\nBayes/taxa de base: P(MT>=700 | renda K-Q) e P(renda K-Q | MT>=700)")
b = con.sql(f"""select count(*) n, avg((Q006 in ('K','L','M','N','O','P','Q'))::int) p_rico,
   avg((NU_NOTA_MT>=700)::int) p_top,
   avg((NU_NOTA_MT>=700)::int) filter(where Q006 in ('K','L','M','N','O','P','Q')) p_top_dado_rico,
   avg((Q006 in ('K','L','M','N','O','P','Q'))::int) filter(where NU_NOTA_MT>=700) p_rico_dado_top
   from '{P}' where TP_PRESENCA_MT=1""").df()
print(b.to_string(index=False))

print("\nBootstrap: uma amostra de n=400 de MT (semente 2023)")
amostra = rng.choice(mt, 400)
print(f"media={amostra.mean():.1f} mediana={np.median(amostra):.1f} dp={amostra.std(ddof=1):.1f}")
se_f = amostra.std(ddof=1)/np.sqrt(400)
print(f"IC95% z para a media: [{amostra.mean()-1.96*se_f:.1f}; {amostra.mean()+1.96*se_f:.1f}]  (verdadeira={mu:.1f})")
bm = np.array([rng.choice(amostra, 400).mean() for _ in range(5000)])
bmed = np.array([np.median(rng.choice(amostra, 400)) for _ in range(5000)])
print(f"bootstrap EP media={bm.std(ddof=1):.2f} (formula {se_f:.2f}); IC95% percentil media=[{np.percentile(bm,2.5):.1f}; {np.percentile(bm,97.5):.1f}]")
print(f"bootstrap EP mediana={bmed.std(ddof=1):.2f}; IC95% mediana=[{np.percentile(bmed,2.5):.1f}; {np.percentile(bmed,97.5):.1f}] (mediana verdadeira={np.median(mt):.1f})")
print("\nProporcao: IC95% de P(MT>700) com n=400 e n=2000")
for n in (400, 2000):
    a = rng.choice(mt, n); p = (a>700).mean(); se = np.sqrt(p*(1-p)/n)
    print(f"n={n}: p_hat={p:.3f} IC=[{p-1.96*se:.3f}; {p+1.96*se:.3f}] verdadeira={(mt>700).mean():.3f}")
print("n para proporcao +-3 pontos percentuais, p=0,5:", int(np.ceil(1.96**2*0.25/0.03**2)))
