media = 10
valor_compra = 12
valor_venda = media + (media *1.1)

if busca_Preco > valor_venda:
    decisao = "vende"

elif busca_Preco < valor_compra:
    decisao = "compra"

else:
    decisao = "Sem operações"
