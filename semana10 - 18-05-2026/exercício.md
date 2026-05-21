exercício passado via WhatspApp:

analise e explique detalhadamente o que está ocorrendo

```c {.line-numbers}
#include <stdio.h>
#include <stdlib.h>

typedef struct Pilha {                // passo 0
    int topo;
    int dados[5];
} Pilha;

void init(Pilha *gean) {              // passo 5*
    gean->topo = 0;
    return 0;
}

int main() {                          // passo 1
    printf("%d\n", sizeof(Pilha));    // passo 2

    Pilha* p = malloc(sizeof(Pilha)); // passo 3
    printf("%d\n", p);                // passo 4

    init(p);                          // passo 5

    p->topo = 0xffffffff;             // passo 6
    printf("%d", p->topo);            // passo 7

    return 0;                         // passo 8
}
```
considerando uma arquitetura típica de 32 bits:

0) a estrutura `Pilha` é definido como um struct contendo os componentes `topo` (um número inteiro) e `dados (um array de 5 números inteiros)`

1) o programa inicia sua execução pela função main(), cujo registro de ativação fica na memória stack

2) em seguida é "impresso" no dispositivo padrão de saída de dados (no caso, o monitor) o tamanho (no formato de um número na base 10 (decimal)) da estrutura `Pilha`
    - o tamanho da estrutura `Pilha` é a soma dos tamanhos de seus componentes: tamanho do inteiro topo (4 bytes) + tamanho do array dados (5 * 4 bytes) = 4 + 20 bytes = 24 bytes

3) com a função `malloc` é alocada uma região de memória do tamanho da estrutura `Pilha` (calculada como sendo de 24 bytes);
o endereço inicial desta região de memória é retornado pela função `malloc` e atribuído à variável `p`; que é definida como uma variável do tipo `Pilha*` (ponteiro para objeto do tipo `Pilha`)

4) o valor da variável `p` (ou seja, o endereço de memória de um objeto do tipo `Pilha`) é impresso

5) em seguida a função `init` (declarada no passo 5*) é chamada (invocada), recebendo o valor da variável `p`

5*) definição da função `init`, que recebe um atributo que é um ponteiro para um objeto do tipo `Pilha`
    - o membro `topo` da `Pilha` `p` recebe o valor 0
    - a função encerra retornando 0, porém tal retorno é ignorado pois a função foi declarada como não tendo retorno (`void`)
    - percebe-se que a função `init` inicializa o objeto do tipo `Pilha` que recebe, setando como topo o início da pilha (índice 0)

6) o membro `topo` da `Pilha` `p` recebe o valor ffffffff<sub>16</sub>; como `topo` é um `int`, o valor de `p` será -1<sub>10</sub>

7) o valor de `p` em base 10 é impresso

8) o programa encerra, retornando o valor 0, que significa que a execução completou normalmente
