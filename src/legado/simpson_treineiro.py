"""Paradoxo de Simpson nos microdados do ENEM 2023: treineiros x demais, nota de Matematica."""
import os
import duckdb
con = duckdb.connect()
P = os.environ.get("MQ_DADOS", "dados").replace("\\", "/") + "/enem2023.parquet"
print("Geral")
print(con.sql(f"""select IN_TREINEIRO, count(*) n, round(avg(NU_NOTA_MT),1) media_mt
    from '{P}' where TP_PRESENCA_MT=1 group by 1 order by 1""").df().to_string(index=False))
print("\nPor faixa etaria agrupada")
print(con.sql(f"""
 with b as (select *, case when TP_FAIXA_ETARIA<=2 then '1) ate 17 anos' when TP_FAIXA_ETARIA<=3 then '2) 18 anos'
   when TP_FAIXA_ETARIA<=5 then '3) 19-20 anos' when TP_FAIXA_ETARIA<=10 then '4) 21-25 anos' else '5) 26+ anos' end faixa
   from '{P}' where TP_PRESENCA_MT=1)
 select faixa, IN_TREINEIRO, count(*) n, round(avg(NU_NOTA_MT),1) media_mt
 from b group by 1,2 order by 1,2""").df().to_string(index=False))
print("\nComposicao etaria")
print(con.sql(f"""
 with b as (select *, case when TP_FAIXA_ETARIA<=2 then '1) ate 17 anos' when TP_FAIXA_ETARIA<=3 then '2) 18 anos'
   when TP_FAIXA_ETARIA<=5 then '3) 19-20 anos' when TP_FAIXA_ETARIA<=10 then '4) 21-25 anos' else '5) 26+ anos' end faixa
   from '{P}' where TP_PRESENCA_MT=1)
 select IN_TREINEIRO, faixa, round(100.0*count(*)/sum(count(*)) over(partition by IN_TREINEIRO),1) pct
 from b group by 1,2 order by 1,2""").df().to_string(index=False))
