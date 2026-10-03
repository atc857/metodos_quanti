"""Numeros do modulo 6 (correlacao e regressao) com os microdados do ENEM 2023. Semente fixa."""
import os
import duckdb, numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm
con = duckdb.connect(); P = os.environ.get("MQ_DADOS", "dados").replace("\\", "/") + "/enem2023.parquet"
rng = np.random.default_rng(2023)
d = con.sql(f"""select NU_NOTA_CN cn, NU_NOTA_CH ch, NU_NOTA_LC lc, NU_NOTA_MT mt, NU_NOTA_REDACAO red, Q006 q6, Q005 moradores,
  TP_ESCOLA esc, TP_SEXO sexo, Q002 q2 from '{P}'
  where TP_PRESENCA_CN=1 and TP_PRESENCA_CH=1 and TP_PRESENCA_LC=1 and TP_PRESENCA_MT=1 and NU_NOTA_REDACAO is not null""").df()
print("n =", len(d))
print("\n== Matriz de correlacao de Pearson (5 notas)")
print(d[['cn','ch','lc','mt','red']].corr().round(3))
print("Spearman CN x MT:", round(stats.spearmanr(d.cn.sample(200000, random_state=1), d.mt.sample(200000, random_state=1))[0],3), "(amostras independentes -> ~0, so como teste de sanidade)")
x, y = d.cn.to_numpy(), d.mt.to_numpy()
rs = stats.spearmanr(x[:300000], y[:300000]); print("Spearman CN x MT (300k pares):", round(rs[0],3))

print("\n== r em subamostras de n=10, 30, 100 (CN x MT): variabilidade de r")
for n in (10, 30, 100, 1000):
    rr = [np.corrcoef(*(d[['cn','mt']].iloc[rng.choice(len(d), n)].to_numpy().T))[0,1] for _ in range(1000)]
    print(f"n={n}: r medio={np.mean(rr):.3f} intervalo 2,5%-97,5% = [{np.percentile(rr,2.5):.2f}; {np.percentile(rr,97.5):.2f}]")

print("\n== Regressao simples MT ~ CN")
X = sm.add_constant(d.cn); m = sm.OLS(d.mt, X).fit()
print(m.params.round(4).to_dict(), "R2=", round(m.rsquared,3), "RSE=", round(np.sqrt(m.scale),1), "IC95% inclinacao:", m.conf_int().loc['cn'].round(4).tolist())
print("predicao CN=500:", round(m.params['const']+m.params['cn']*500,1), " CN=700:", round(m.params['const']+m.params['cn']*700,1))
print("residuos: media", round(m.resid.mean(),3), "dp", round(m.resid.std(),1))
# heterocedasticidade: dp dos residuos por faixa de CN
d['faixa_cn'] = pd.cut(d.cn, [0,400,450,500,550,600,650,1000])
print(d.assign(res=m.resid).groupby('faixa_cn', observed=True).res.agg(['count','mean','std']).round(1))

print("\n== Regressao simples MT ~ Redacao e CH ~ LC")
for yv, xv in (('mt','red'),('ch','lc')):
    mm = sm.OLS(d[yv], sm.add_constant(d[xv])).fit(); print(yv, '~', xv, mm.params.round(3).to_dict(), 'R2=', round(mm.rsquared,3))

print("\n== Renda (Q006 ordinal A..Q como 1..17) x MT")
ordv = {c:i+1 for i,c in enumerate("ABCDEFGHIJKLMNOPQ")}
d['q6n'] = d.q6.map(ordv)
print("Pearson r (codigo 1-17):", round(d[['q6n','mt']].corr().iloc[0,1],3), " Spearman:", round(stats.spearmanr(d.q6n, d.mt)[0],3))
med = d.groupby('q6').mt.mean().round(1); print(med.to_dict())
# ponto medio das faixas (R$) - aproximacao
mid = dict(zip("ABCDEFGHIJKLMNOPQ",[0,660,1650,2310,2970,3630,4620,5940,7260,8580,9900,11220,12540,14520,17820,23100,30000]))
d['renda_mid'] = d.q6.map(mid); d['lrenda'] = np.log(d.renda_mid.clip(lower=330))
print("r(renda_mid, MT)=", round(d[['renda_mid','mt']].corr().iloc[0,1],3), " r(log renda, MT)=", round(d[['lrenda','mt']].corr().iloc[0,1],3))
m2 = sm.OLS(d.mt, sm.add_constant(d.q6n)).fit(); print("MT ~ codigo renda: b=", round(m2.params['q6n'],2), "R2=", round(m2.rsquared,3))

print("\n== Regressao multipla: MT ~ renda (cod) + escola(priv) + sexo(F) + CN? (sem CN)")
dd = d[d.esc.isin([2,3])].copy(); dd['priv'] = (dd.esc==3).astype(int); dd['fem'] = (dd.sexo=='F').astype(int)
mm1 = sm.OLS(dd.mt, sm.add_constant(dd[['q6n']])).fit()
mm2 = sm.OLS(dd.mt, sm.add_constant(dd[['q6n','priv']])).fit()
mm3 = sm.OLS(dd.mt, sm.add_constant(dd[['q6n','priv','fem']])).fit()
for nome, mo in (('renda',mm1),('renda+privada',mm2),('renda+privada+mulher',mm3)):
    print(nome, mo.params.round(2).to_dict(), 'R2=', round(mo.rsquared,3), 'n=', int(mo.nobs))

print("\n== Validacao treino/teste (ponte para IA): MT ~ renda+privada+mulher, 70/30")
idx = rng.permutation(len(dd)); ntr = int(0.7*len(dd)); tr, te = dd.iloc[idx[:ntr]], dd.iloc[idx[ntr:]]
mo = sm.OLS(tr.mt, sm.add_constant(tr[['q6n','priv','fem']])).fit()
pred = mo.predict(sm.add_constant(te[['q6n','priv','fem']]))
rmse = np.sqrt(((te.mt-pred)**2).mean()); base = np.sqrt(((te.mt-tr.mt.mean())**2).mean())
print(f"RMSE teste={rmse:.1f} ; RMSE do modelo 'sempre a media'={base:.1f} ; R2 teste={1-((te.mt-pred)**2).sum()/((te.mt-te.mt.mean())**2).sum():.3f}")

print("\n== Anscombe (confirmacao numerica)")
ax = np.array([10,8,13,9,11,14,6,4,12,7,5]); ay = [np.array([8.04,6.95,7.58,8.81,8.33,9.96,7.24,4.26,10.84,4.82,5.68]), np.array([9.14,8.14,8.74,8.77,9.26,8.10,6.13,3.10,9.13,7.26,4.74]), np.array([7.46,6.77,12.74,7.11,7.81,8.84,6.08,5.39,8.15,6.42,5.73])]
for yv in ay: print(round(np.corrcoef(ax,yv)[0,1],3), round(np.polyfit(ax,yv,1)[0],3), round(np.polyfit(ax,yv,1)[1],2))
