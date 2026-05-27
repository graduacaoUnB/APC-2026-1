# lista de execícios de Python
- lista disponível em: https://github.com/jhcf/APCUnB2026.1/blob/main/python_cheatsheet_vs_c.md

## principais difetenças entre as linguagens C e Python:
#### tipagem
- em C, os tipos são das variáveis e são estáticos, ou seja, se uma variável for declarada como int, ela nunca poderá conter uma string.
- Já em Python os tipos são do objeto (que as variáveis referenciam) e são dinâmicos; neste caso é possível uma variável referenciar um um objeto do tipo `int` e depois referenciar um objeto do tipo `str`, pois a variável apenas referencia um objeto, e o tipo do objeto é do próprio objeto, não da variável.

#### gerenciamento de memória
- em C alocação e liberação de memória são gerenciadas manualmente, com as funções `malloc` e `free` respectivamente
- já em Python existe um garbage collector, que é executado automaticamente, sobre o qual o programador não tem controle; o garbage collector libera automaticamente a memória inacessível, isto é, que não é mais referenciada de nenhuma forma por nenhuma variável.

#### conceito de igualdade
- em C o operator `==` compara valores, de forma simples e intuitiva
- em Python, objetos têm identidade, isto é, mesmo que os valores de 2 objetos sejam iguais, isso não faz com que sejam o mesmo objeto
  - às vezes estaremos interessados apenas nos valores dos objetos, não em suas identidades; para isso pode-se usar o operador `==`
  - outras vezes queremos comparar identidades; para isso pode-se usar o operador `is`

#### boilerplate
- C requer uma estrutura maior para poder ser compilado, como `#include` e a definição da função `main`
- Python não requer "cerimônias" ou código de preparação para que o código seja executado.

#### tipos de dados
- strings
  - C possui um tipo específico para caractere, `char`, e não possui um tipo específico para strings (usa-se um `char[]` ou `char*`); usa-se o caractere `\0` para indicar o fim de strings
  - já Python não diferencia entre caracteres e strings; sendo usado o tipo `str`
- numerais inteiros
  - C possui vários tipos para representar números inteiros: `short`, `int`, `long`, etc, cada um com um tamanho definido
  - Python possui apenas o tipo `int`, que não possui um tamanho prédeterminado
- numerais de aritmética de ponto flutuante
  - C possui diferentes tipos, como `float` e `double`
  - já Python possui apenas 1 tipo, `float`, que ocupa 64 bits (4 bytes)

#### declaração e atribuição
- em C criação (declaração) e atribuição de variáveis são ações diferentes e separáveis, isto é, é possível em um momento fazer uma declaração e em um momento posterior realizar a atribuição da variável
- em Python, a variável é criada justamente com sua atribuição

## reatribuição e contagem de referências
- se duas variáveis referenciarem o memso objeto, pode-se usar qualquer das variáveis para alterar o objeto (mudanças serão acessíveis por abas variáveis)

#### operadores 4


