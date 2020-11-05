#SELECT c.preco, c.data_importacao FROM cotacao c WHERE equipe_id = 2 AND acao_id = 4 ORDER BY data_importacao;
#SELECT c.preco, c.data_importacao FROM cotacao c WHERE equipe_id = 2 AND acao_id = 5 ORDER BY data_importacao;
#SELECT c.preco, c.data_importacao FROM cotacao c WHERE equipe_id = 2 AND acao_id = 6 ORDER BY data_importacao;

SELECT c.preco, c.data_importacao, a.nome FROM cotacao c  JOIN acao a ON a.id = c.acao_id WHERE equipe_id = 2 AND a.nome = 'BBSE3.SA' ORDER BY data_importacao