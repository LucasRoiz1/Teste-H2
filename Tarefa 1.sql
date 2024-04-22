-- Teste Engenheiro de dados H2.

-- Vamos falar do primeiro exercício! A tarefa era descobrir qual o Rake gerado por cada geração de jogadores.
-- Começamos separando os jogadores de acordo com o ano do nascimento e rotulando cada um deles com sua respectiva geração.
-- Para descobrir o valor basta SOMAR o valor total do Rake e agrupar os resultados por cada geração.

SELECT 
    CASE
        WHEN data_nascimento <= '1924-12-31' THEN 'Data Invalida'
        WHEN data_nascimento <= '1940-12-31' THEN 'Veteranos'
        WHEN data_nascimento <= '1959-12-31' THEN 'Baby Boomers'
        WHEN data_nascimento <= '1979-12-31' THEN 'Geração X'
        WHEN data_nascimento <= '1995-12-31' THEN 'Geração Y'
        WHEN data_nascimento <= '2010-12-31' THEN 'Geração Z'
        WHEN data_nascimento >= '2011-01-01' THEN 'Geração Alpha'
    END AS geracao,
    SUM(rake) AS total_rake
FROM clientes c
LEFT JOIN resultado r ON r.Clientes_id = c.id
GROUP BY geracao
ORDER BY geracao;
-- FIM 


-- A segunda tarefa era descobrir o Rake gerado por mês. Numa análise de contexto padrão, não podemos considerar apenas o mês mas também devemos considerar o ano.
-- Então usei a função SUBSTRING para coletar o ano e o mês de cada acesso a ficou no formato YYYYMM.
-- Com o ano e o mês separado, podemos SOMAR o Rake e depois Agrupar por "AnoMes".
SELECT CONCAT(SUBSTRING(data_acesso, 1, 4),SUBSTRING(data_acesso, 6, 2)) as 'AnoMes', SUM(rake) FROM resultado group by AnoMes
-- FIM


-- E chegamos na terceira tarefa. Aqui a missão era descobrir a porcentagem de ganhadores agrupando por Sexo.
-- Calculei a quantidade de Eventos Win * 100 dividindo pela quantidade total de eventos, e depois agrupa por sexo.
SELECT 
    sexo,
    ((COUNT(CASE WHEN(winning > 0) THEN 1 END) * 100) / COUNT(*)) AS "Win Rate"
FROM 
    clientes
JOIN 
    resultado ON clientes.id = resultado.Clientes_id
GROUP BY 
    sexo;
--FIM


