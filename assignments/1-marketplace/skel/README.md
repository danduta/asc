Nume: Duta Dan-Stefan
Grupă: 332CA

# Tema 2

Organizare
-
Nu am implementat nicio alta clasa/alt modul in afara de cele deja prezente in schelet.
M-am bazat pe implementarea de Queue pentru a implementa cerinta. Fiecare producator
are un Queue asociat + fiecare produs are un Queue asociat cu capacitate nelimitata.
Astfel, accesul la resurse este atomic si fiecare producator e limitat la dimensiunea
initiala a Queue-ului. Exista doua Lock-uri in Marketplace: unul pentru inregistrarea
producatorilor (sa nu existe 2 cu acelasi ID) si unul pentru crearea unui Queue pentru
un anume produs. Marketplace-ul tine un dictionar cu toate carucioarele consumatorilor
iar cand acest dictionar se goleste, se seteaza un event care anunta producatorii ca
nu mai trebuie sa produca. Acest lucru poate fi redundant deoarece thread-urile
sunt create ca daemoni.

Git
-
1. https://github.com/danduta/asc.git
