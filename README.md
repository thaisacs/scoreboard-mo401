# scoreboard-mo401

Este é um simulador de execução fora de ordem com a técnica de scoreboarding, desenvolvido na disciplina MO401.

### Entradas

Os casos de testes foram armazenados na pasta inputs/, onde é possível observar que todos os casos possuem dois arquivos: arquivo.s e arquivo.in.

Onde arquivo.s são nomeados com "example" + número do caso de teste + ".s". Além disso, arquivo.in são nomeados com "cfg" + número do caso de teste + ".in".

### Uso 

Um exemplo de utilização do simulador considerando o caso de teste 10 seria o seguinte comando.

```
python main.py -p inputs/example10.s -c inputs/cfg10.in
```

Ademais, é possível verificar detalhes da configuração de execução utilizando o seguinte comando

```
python main.py -h
```
