/*
 * Practica 3 - Sistemas Operativos
 * Cuenta los numeros primos en el intervalo [1, N]
 */
#include <stdio.h>
#include <stdlib.h>

#define N_DEFECTO 2000000

int es_primo(long n)
{
    long d;
    if (n < 2) return 0;
    for (d = 2; d * d <= n; d++) {
        if (n % d == 0) return 0;
    }
    return 1;
}

int main(int argc, char *argv[])
{
    long n = N_DEFECTO;
    long i;
    long total = 0;

    if (argc > 1) n = atol(argv[1]);

    /* recorremos todo el intervalo */
    for (i = 1; i <= n; i++) {
        if (es_primo(i)) total++;
    }

    printf("Primos entre 1 y %ld: %ld\n", n, total);
    return 0;
}
