# SECURE CRYPTO SPACE

## Introducció

Secure Crypto Space és una aplicació d'escriptori desenvolupada en Python dissenyada per proporcionar un entorn segur per a l'emmagatzematge i gestió d'arxius sensibles. Utilitza criptografia avançada per xifrar documents, assegurant que només els usuaris autoritzats amb la contrasenya de sessió correcta puguin accedir al contingut.

L'aplicació combina seguretat amb una interfície moderna i fàcil d'usar, permetent operacions de xifratge, desxifratge i esborrat segur de manera intuïtiva.

## Característiques Principals

*   **Autenticació Segura**: Sistema de Login i Registre amb emmagatzematge segur de credencials (hashing i salting).
*   **Gestió de Vaults**: Cada usuari té el seu propi espai segur ("Vault") aïllat.
*   **Xifratge AES-256**: Els arxius es xifren utilitzant l'estàndard AES en mode CBC amb derivació de claus PBKDF2HMAC.
*   **Importació Automàtica**: Facilitat per importar arxius des del sistema a l'entorn segur.
*   **Exportació Segura**: Desxifratge i exportació d'arxius a una ubicació externa, amb eliminació automàtica de l'arxiu xifrat al vault.
*   **Esborrat Segur (Wipe)**: Eliminació definitiva d'arxius sobrescrivint el seu contingut amb dades aleatòries abans d'esborrar-los, impedint la seva recuperació.
*   **Interfície Moderna**: Desenvolupada amb `customtkinter` per a una experiència visual neta i mode fosc per defecte.

## Requisits

El projecte requereix **Python 3.x** i les següents llibreries llistades a `requeriments.txt`:

*   `customtkinter`: Per a la interfície gràfica.
*   `cryptography`: Per a les funcions de xifratge i seguretat.
*   `Pillow`: Per a la gestió d'imatges i icones.

## Instal·lació

1.  Clona el repositori o descarrega el codi font.
2.  Instal·la les dependències executant:

```
pip install -r requeriments.txt
```

## Ús

Per iniciar l'aplicació, executa l'arxiu principal:

```
python main.py
```

### Flux de Treball

1.  **Inici**: En obrir l'app, inicia sessió o registra't si ets un usuari nou.
2.  **Dashboard**: Un cop dins, veuràs els teus arxius.
    *   **Importar**: Afegeix arxius des del teu ordinador al Vault.
    *   **Encriptar**: Selecciona un arxiu visible i prem "Encriptar". L'original s'esborrarà de forma segura.
    *   **Exportar**: Selecciona un arxiu xifrat (.enc) i prem "Exportar" per guardar-lo desxifrat fora del Vault.
    *   **Eliminar**: Esborra arxius permanentment usant l'esborrat segur.
3.  **Navegació**: Fes doble clic a les carpetes per navegar.

## Estructura del Projecte

*   `src/core/`: Mòduls del nucli (seguretat, gestió d'arxius, autenticació).
*   `src/ui/`: Interfície gràfica (Login, Dashboard, Sidebar).
*   `src/logic/`: Lògica de negoci (Importador).
*   `data/`: Emmagatzematge de vaults i usuaris.
