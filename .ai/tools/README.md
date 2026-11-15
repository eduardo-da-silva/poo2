# Ferramentas de revisao

Regra do curso: o leitor deve chegar ao codigo **lendo o texto**. O codigo em `code/` serve para consulta e para itens repetitivos.

- `auditar_codigo_no_texto.py` — lista classes/funcoes novas ou alteradas em cada snapshot que **nao aparecem** nos blocos de codigo do capitulo (`resumo` ou `detalhe`).
- `conferir_texto_x_codigo.py` — mostra onde o codigo do texto **difere** do codigo real (revise a mao: trechos intermediarios e elisoes sao normais).
- `extrair_codigo.py` — `seg(arquivo, "Classe", "Classe.metodo")` devolve o fonte exato, para inserir nos capitulos.

Ficam legitimamente so no codigo: a maioria dos testes e getters triviais (o texto deve dizer onde estao).
