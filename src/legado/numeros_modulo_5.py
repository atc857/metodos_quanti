"""Numeros do modulo 5 (testes de hipoteses) com os microdados do ENEM 2023. Semente fixa."""
import os
import duckdb, numpy as np, pandas as pd
from scipy import stats
con = duckdb.connect(); P = os.environ.get("MQ_DADOS", "dados").replace("\\", "/") + "/enem2023.parquet"
rng = np.random.default_rng(2023)

def d_cohen(a, b):
    na, nb = len(a), len(b)
    sp = np.sqrt(((na-1)*a.var(ddof=1) + (nb-1)*b.var(ddof=1)) / (na+nb-2))
    return (a.mean()-b.mean())/sp

print("== Moeda: 8 caras em 10 (slides 48-53)")
r = stats.binomtest(8, 10, 0.5, alternative='two-sided'); print("bilateral p=", round(r.pvalue,4))
print("unilateral p=", round(stats.binomtest(8, 10, 0.5, alternative='greater').pvalue,4))
print("alfa=0.05: rejeita se k<=1 ou k>=9; P(erro I) =", round(2*stats.binom.cdf(1,10,0.5),4))

mt = con.sql(f"select TP_SEXO sexo, TP_ESCOLA esc, Q006 q6, TP_COR_RACA cor, NU_NOTA_MT mt, NU_NOTA_CH ch, NU_NOTA_LC lc, NU_NOTA_CN cn, NU_NOTA_REDACAO red, SG_UF_PROVA uf from '{P}' where TP_PRESENCA_MT=1").df()

print("\n== t independente: MT, homens x mulheres")
m, f = mt[mt.sexo=='M'].mt.to_numpy(), mt[mt.sexo=='F'].mt.to_numpy()
print(f"nM={len(m)} mediaM={m.mean():.1f} dpM={m.std(ddof=1):.1f} | nF={len(f)} mediaF={f.mean():.1f} dpF={f.std(ddof=1):.1f}")
print("razao de variancias:", round(max(m.var(ddof=1),f.var(ddof=1))/min(m.var(ddof=1),f.var(ddof=1)),2))
t = stats.ttest_ind(m, f, equal_var=False); print(f"Welch t={t.statistic:.1f} p={t.pvalue:.3g} dif={m.mean()-f.mean():.1f} d={d_cohen(m,f):.2f}")
se = np.sqrt(m.var(ddof=1)/len(m)+f.var(ddof=1)/len(f)); print(f"IC95% dif = [{m.mean()-f.mean()-1.96*se:.1f}; {m.mean()-f.mean()+1.96*se:.1f}]")
print("Mann-Whitney (amostra 100k cada):", stats.mannwhitneyu(rng.choice(m,100000), rng.choice(f,100000)).pvalue)

print("\n== Subamostras (efeito do n sobre o valor-p), 1000 repeticoes por n")
for n in (10, 30, 100, 300, 1000):
    rej = 0
    for _ in range(1000):
        a, b = rng.choice(m, n), rng.choice(f, n)
        rej += stats.ttest_ind(a, b, equal_var=False).pvalue < 0.05
    print(f"n por grupo={n}: poder empirico (rejeita H0) = {rej/10:.1f}%")

print("\n== Erro tipo I: sorteio de dois grupos da MESMA populacao (H0 verdadeira)")
for n in (30, 300):
    rej = sum(stats.ttest_ind(rng.choice(mt.mt.to_numpy(), n), rng.choice(mt.mt.to_numpy(), n), equal_var=False).pvalue < 0.05 for _ in range(2000))
    print(f"n={n}: rejeicoes = {rej/20:.1f}% (esperado ~5%)")

print("\n== Comparacoes multiplas: 100 'testes' com rotulos aleatorios (n=500 por grupo)")
x = mt.mt.to_numpy(); ps = []
for _ in range(100):
    idx = rng.choice(len(x), 1000, replace=False); a, b = x[idx[:500]], x[idx[500:]]
    ps.append(stats.ttest_ind(a, b, equal_var=False).pvalue)
ps = np.array(ps); print("p<0.05:", int((ps<0.05).sum()), "de 100; menor p =", round(ps.min(),4), "; com Bonferroni (alfa=0.05/100) rejeita:", int((ps<0.0005).sum()))

print("\n== t independente: escola publica x privada (so quem informou escola)")
pu, pr = mt[mt.esc==2].mt.to_numpy(), mt[mt.esc==3].mt.to_numpy()
t = stats.ttest_ind(pr, pu, equal_var=False)
print(f"n_pub={len(pu)} media={pu.mean():.1f} dp={pu.std(ddof=1):.1f} | n_priv={len(pr)} media={pr.mean():.1f} dp={pr.std(ddof=1):.1f}")
print(f"dif(priv-pub)={pr.mean()-pu.mean():.1f} Welch t={t.statistic:.1f} p={t.pvalue:.3g} d={d_cohen(pr,pu):.2f}")

print("\n== t pareado: CH x LC no mesmo participante")
pp = mt.dropna(subset=['ch','lc'])
dd = (pp.ch-pp.lc).to_numpy(); tt = stats.ttest_rel(pp.ch, pp.lc)
print(f"n={len(pp)} media CH={pp.ch.mean():.1f} LC={pp.lc.mean():.1f} dif media={dd.mean():.2f} dp dif={dd.std(ddof=1):.1f} t={tt.statistic:.1f} p={tt.pvalue:.3g} d_z={dd.mean()/dd.std(ddof=1):.3f}")

print("\n== Qui-quadrado: presenca em MT x faixa de renda agrupada (todos inscritos)")
all_ = con.sql(f"select Q006 q6, (TP_PRESENCA_MT=1)::int pres from '{P}'").df()
g = {'A':'1 ate R$1.320','B':'1 ate R$1.320','C':'2 R$1.320-3.300','D':'2 R$1.320-3.300','E':'2 R$1.320-3.300','F':'3 R$3.300-6.600','G':'3 R$3.300-6.600','H':'3 R$3.300-6.600'}
all_['renda'] = all_.q6.map(lambda x: g.get(x, '4 acima de R$6.600'))
ct = pd.crosstab(all_.renda, all_.pres); print(ct)
chi2, p, dof, exp = stats.chi2_contingency(ct)
V = np.sqrt(chi2/(ct.values.sum()*(min(ct.shape)-1)))
print(f"chi2={chi2:.0f} gl={dof} p={p:.3g} Cramer V={V:.3f} min esperado={exp.min():.0f}")
print((ct.div(ct.sum(1), axis=0)*100).round(1))
sub = all_.sample(1000, random_state=1); ct2 = pd.crosstab(sub.renda, sub.pres); c2, p2, d2, e2 = stats.chi2_contingency(ct2)
print(f"subamostra n=1000: chi2={c2:.1f} p={p2:.3g} V={np.sqrt(c2/(1000*(min(ct2.shape)-1))):.3f}")

print("\n== ANOVA: MT por faixa de renda agrupada (presentes)")
mt['renda'] = mt.q6.map(lambda x: g.get(x, '4 acima de R$6.600'))
grp = [mt[mt.renda==k].mt.to_numpy() for k in sorted(mt.renda.unique())]
for k, a in zip(sorted(mt.renda.unique()), grp): print(f"{k}: n={len(a)} media={a.mean():.1f} dp={a.std(ddof=1):.1f}")
F, pF = stats.f_oneway(*grp); allv = np.concatenate(grp)
ssb = sum(len(a)*(a.mean()-allv.mean())**2 for a in grp); sst = ((allv-allv.mean())**2).sum()
print(f"F={F:.0f} p={pF:.3g} eta2={ssb/sst:.3f}")
print("razao max/min variancias:", round(max(a.var(ddof=1) for a in grp)/min(a.var(ddof=1) for a in grp),2))
tk = stats.tukey_hsd(*grp); print("Tukey p-valores (matriz):"); print(np.array2string(tk.pvalue, precision=3))
print("Kruskal-Wallis p:", stats.kruskal(*[rng.choice(a, 50000) for a in grp]).pvalue)
