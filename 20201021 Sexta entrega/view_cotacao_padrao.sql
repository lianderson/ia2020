#SELECT * FROM cotacao WHERE equipe_id = 2;
#SELECT * FROM noticias WHERE equipe_id = 2;


SELECT e.descricao,
	e.participantes,
	e.id,
	a.nome,
	c.preco,
	c.data_importacao
FROM cotacao c
JOIN acao a ON a.id = c.acao_id
JOIN equipe e ON e.id = c.equipe_id
WHERE equipe_id = 2
AND data_importacao BETWEEN '2020-10-27' AND '2020-10-28'
ORDER BY nome, data_importacao
