```
                        _                         _
                       | |                       | |
 ___  ___ ___  _ __ ___| |__   ___   __ _ _ __ __| |
/ __|/ __/ _ \| '__/ _ \ '_ \ / _ \ / _` | '__/ _` |
\__ \ (_| (_) | | |  __/ |_) | (_) | (_| | | | (_| |
|___/\___\___/|_|  \___|_.__/ \___/ \__,_|_|  \__,_|

                                 by: thais camacho
                                 
```

Este é um simulador de execução fora de ordem com a técnica de scoreboarding, desenvolvido na disciplina [MO401](https://github.com/lfwanner/scoreboard-mo401).

## Entradas

Os casos de testes foram armazenados na pasta inputs/, onde é possível observar que todos os casos possuem dois arquivos: arquivo.s e arquivo.in.

Onde arquivos ".s" são nomeados com "example" + número do caso de teste + ".s". Além disso, arquivos ".in" são nomeados com "cfg" + número do caso de teste + ".in".

## Uso 

Para implementar este simulador, utilizou-se Python 3.9.2 e WSL 2 com Debian.
Um exemplo de utilização do simulador considerando o caso de teste 10 seria o seguinte comando.

```
python3 main.py -p inputs/example10.s -c inputs/cfg10.in
```

Ademais, é possível verificar detalhes da configuração de execução utilizando o seguinte comando.

```
python3 main.py -h
```

## LICENSE

You are free to use this code under the [MIT LICENSE](https://choosealicense.com/licenses/mit/).
